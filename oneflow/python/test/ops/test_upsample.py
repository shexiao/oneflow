import os
from collections import OrderedDict

import numpy as np
import oneflow as flow
import tensorflow as tf
import test_global_storage
from test_util import GenArgList, type_name_to_flow_type

gpus = tf.config.experimental.list_physical_devices("GPU")
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)


def compare_with_tensorflow(
    device_type, input_shape, dtype, size, data_format, interpolation
):
    assert device_type in ["gpu", "cpu"]
    flow.clear_default_session()

    func_config = flow.FunctionConfig()
    func_config.default_data_type(flow.float)
    func_config.train.primary_lr(1e-4)
    func_config.train.model_update_conf(dict(naive_conf={}))

    @flow.global_function(func_config)
    def UpsampleJob():
        with flow.scope.placement(device_type, "0:0"):
            x = flow.get_variable(
                "input",
                shape=input_shape,
                dtype=type_name_to_flow_type[dtype],
                initializer=flow.random_uniform_initializer(minval=2, maxval=5),
                trainable=True,
            )

            loss = flow.layers.upsample_2d(
                x, size=size, data_format=data_format, interpolation=interpolation
            )
            flow.losses.add_loss(loss)

            flow.watch(x, test_global_storage.Setter("x"))
            flow.watch_diff(x, test_global_storage.Setter("x_diff"))
            flow.watch(loss, test_global_storage.Setter("loss"))
            flow.watch_diff(loss, test_global_storage.Setter("loss_diff"))

            return loss

    # OneFlow
    check_point = flow.train.CheckPoint()
    check_point.init()
    of_out = UpsampleJob().get()
    channel_pos = "channels_first" if data_format.startswith("NC") else "channels_last"
    # TensorFlow
    with tf.GradientTape(persistent=True) as tape:
        x = tf.Variable(test_global_storage.Get("x").astype(np.float32))
        tf_out = tf.keras.layers.UpSampling2D(
            size=size, data_format=channel_pos, interpolation=interpolation
        )(x)

    loss_diff = test_global_storage.Get("loss_diff").astype(np.float32)
    tf_x_diff = tape.gradient(tf_out, x, loss_diff)
    assert np.allclose(of_out.numpy(), tf_out.numpy(), rtol=1e-5, atol=1e-5)
    assert np.allclose(
        test_global_storage.Get("x_diff"), tf_x_diff.numpy(), rtol=1e-5, atol=1e-5
    )


def test_upsample(test_case):
    arg_dict = OrderedDict()
    arg_dict["device_type"] = ["gpu"]
    arg_dict["input_shape"] = [(2, 11, 12, 13)]
    arg_dict["dtype"] = ["float32", "double"]
    arg_dict["size"] = [(2, 2), 3, (1, 2)]
    arg_dict["data_format"] = ["NCHW", "NHWC"]
    arg_dict["interpolation"] = ["nearest", "bilinear"]
    for arg in GenArgList(arg_dict):
        compare_with_tensorflow(*arg)
