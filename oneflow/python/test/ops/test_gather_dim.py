"""
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from collections import OrderedDict
import numpy as np
import oneflow as flow
from test_util import GenArgList
import oneflow.typing as oft

g_samples = [{'input': [25, 42, 10, 17, 37, 24, 24, 6, 94], 'index': [7, 0, 0, 7, 1], 'dim': 0, 'out': [6, 25, 25, 6, 42], 'grad': [2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0]}, {'input': [[10, 5], [6, 2], [0, 7], [56, 53]], 'index': [[0, 
0], [0, 0], [0, 0], [0, 0]], 'dim': 1, 'out': [[10, 10], [6, 6], [0, 0], [56, 56]], 'grad': [[2.0, 0.0], [2.0, 0.0], [2.0, 0.0], [2.0, 0.0]]}, {'input': [[[76, 20, 38], [51, 36, 62], [34, 19, 17], [29, 74, 6], [29, 87, 74], [25, 32, 13], [58, 64, 25], [30, 78, 93], [43, 24, 87], [83, 64, 42]], [[63, 84, 84], [28, 20, 59], [87, 58, 80], [80, 73, 18], [62, 21, 35], [30, 15, 50], [20, 12, 68], [25, 24, 55], [15, 81, 5], [91, 0, 64]], [[94, 9, 27], [36, 43, 37], [57, 80, 68], [61, 70, 80], [22, 0, 96], [85, 31, 80], [9, 9, 35], [24, 4, 36], [12, 52, 4], [15, 97, 92]], [[42, 8, 97], [40, 77, 22], [38, 80, 29], [63, 64, 72], [92, 26, 44], [78, 34, 2], [4, 99, 96], [54, 13, 47], [43, 30, 97], [91, 29, 39]], [[23, 15, 70], [37, 41, 82], [43, 47, 31], [88, 84, 85], [5, 42, 40], [49, 54, 32], [81, 49, 5], [71, 55, 52], [28, 2, 0], [51, 37, 51]], [[28, 45, 44], [40, 6, 14], [76, 19, 80], [5, 61, 28], [65, 34, 
7], [99, 56, 24], [51, 11, 21], [86, 26, 53], [0, 79, 2], [63, 66, 19]], [[61, 34, 69], [9, 55, 2], [99, 87, 96], [34, 38, 61], [46, 34, 24], [5, 99, 17], [54, 5, 40], [69, 13, 16], [28, 0, 6], [63, 3, 63]], [[27, 48, 7], [1, 49, 40], [84, 26, 8], [24, 97, 68], [40, 72, 94], [95, 65, 95], [38, 46, 26], [67, 17, 39], [23, 26, 62], [61, 19, 90]]], 'index': [[[2, 1, 0], [2, 4, 2], [1, 6, 0], [4, 0, 2], [4, 1, 2], [2, 5, 4], [3, 2, 0], [1, 5, 5], [6, 2, 4], [1, 0, 1]], [[5, 4, 0], [4, 5, 5], [6, 4, 6], [6, 0, 3], [2, 6, 5], [0, 3, 5], [6, 1, 6], [5, 1, 1], [1, 2, 5], [2, 4, 4]]], 'dim': 0, 'out': [[[94, 84, 38], [36, 41, 37], [87, 87, 17], [88, 74, 80], [5, 21, 96], [85, 56, 32], [4, 9, 25], [25, 26, 53], [28, 52, 0], [91, 64, 64]], [[28, 15, 38], [37, 6, 14], [99, 47, 96], [34, 74, 72], [22, 34, 7], [25, 34, 24], [54, 12, 40], [86, 24, 55], [15, 52, 2], [15, 37, 51]]], 'grad': [[[0.0, 0.0, 2.0], [0.0, 
0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 2.0, 0.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0]], [[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 1.0, 
0.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 1.0], [1.0, 0.0, 0.0], [1.0, 0.0, 1.0]], [[1.0, 0.0, 0.0], [1.0, 0.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [0.0, 2.0, 0.0], [1.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [[0.0, 1.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 1.0]], [[1.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [1.0, 0.0, 1.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]]}, {'input': [[[[28, 93], [85, 45], [12, 68]], [[93, 33], [40, 25], [52, 35]], [[34, 85], [59, 84], [68, 18]], [[93, 13], [56, 36], [40, 26]], [[52, 36], [47, 83], [18, 35]], [[10, 35], [78, 78], [10, 83]], [[19, 94], [7, 65], [31, 92]], [[1, 48], [45, 34], [58, 80]]], [[[78, 74], [62, 63], [53, 72]], [[41, 2], [91, 4], [92, 79]], [[58, 91], [7, 43], [9, 83]], [[91, 43], [58, 40], [43, 47]], [[69, 35], [88, 45], [53, 69]], [[18, 79], [14, 57], [96, 15]], [[87, 6], [33, 41], [83, 72]], [[58, 79], [87, 40], [68, 11]]], [[[49, 9], [7, 52], [67, 52]], [[7, 3], [51, 93], [61, 22]], [[87, 79], [7, 6], [39, 20]], [[4, 91], [91, 83], [86, 54]], [[87, 51], [82, 25], [84, 66]], [[56, 87], [52, 13], [18, 94]], [[84, 78], [35, 69], [67, 16]], [[50, 60], [29, 32], [25, 6]]], [[[49, 1], [13, 56], [55, 93]], [[56, 90], [26, 0], [38, 80]], [[35, 1], [0, 27], [96, 77]], [[87, 99], [38, 26], [61, 82]], [[24, 25], [11, 23], [47, 65]], [[72, 90], [89, 35], [58, 14]], [[30, 60], [98, 55], [63, 88]], [[49, 20], [75, 43], [44, 18]]], [[[30, 97], [0, 45], [43, 17]], [[67, 0], [11, 57], [42, 95]], [[14, 91], [53, 55], [49, 48]], [[59, 92], [76, 99], [99, 4]], [[19, 37], [37, 18], [17, 45]], [[68, 64], [80, 26], [53, 73]], [[81, 94], [72, 60], [36, 62]], [[36, 63], [13, 8], [58, 64]]], [[[27, 84], [79, 71], [70, 0]], [[23, 87], [7, 67], [80, 65]], [[4, 12], [56, 49], [86, 4]], [[75, 55], 
[56, 21], [68, 45]], [[5, 23], [91, 30], [42, 76]], [[65, 18], [56, 61], [79, 7]], [[93, 75], [48, 72], [38, 74]], [[14, 83], [49, 30], [40, 22]]], [[[79, 26], [89, 2], [92, 95]], [[3, 88], [11, 2], [53, 7]], [[15, 57], [91, 61], [59, 94]], [[58, 9], [0, 56], [72, 44]], [[3, 8], [53, 15], [59, 4]], [[57, 42], [22, 75], [8, 42]], [[52, 7], [51, 57], [96, 58]], [[92, 21], [4, 13], [68, 59]]], [[[69, 7], [84, 49], [41, 85]], [[32, 92], [41, 10], [80, 21]], [[33, 60], [37, 51], [50, 17]], [[74, 82], [96, 74], [48, 26]], [[32, 84], [22, 90], [13, 54]], [[91, 10], [14, 55], [84, 57]], [[9, 41], [47, 76], [96, 43]], [[57, 94], [66, 24], [66, 39]]], [[[87, 83], [43, 42], [54, 22]], [[0, 92], [22, 45], [52, 58]], [[86, 3], [62, 55], [5, 5]], [[98, 56], [48, 23], [83, 24]], [[9, 76], [97, 43], [37, 7]], [[50, 72], [24, 28], [67, 66]], [[72, 19], [19, 92], [25, 32]], [[93, 7], [3, 54], [23, 4]]], [[[79, 71], [66, 30], [6, 55]], [[19, 44], [49, 30], [4, 75]], [[38, 85], [86, 75], [45, 33]], [[63, 34], [73, 0], [43, 62]], [[23, 49], [34, 47], [53, 56]], [[95, 40], [87, 69], [79, 15]], [[89, 40], [50, 32], [75, 38]], [[22, 63], [10, 2], [82, 31]]]], 'index': [[[[8, 6], [1, 3], [2, 1]], [[2, 7], [7, 0], [8, 2]], [[6, 0], [5, 2], [0, 1]], [[0, 8], [1, 3], [2, 2]], [[0, 7], [7, 1], [5, 8]], [[4, 5], [6, 6], [6, 3]], [[3, 6], [5, 8], [5, 5]], [[7, 1], [5, 5], [8, 
5]]], [[[7, 4], [2, 1], [0, 4]], [[3, 8], [5, 8], [0, 8]], [[8, 1], [2, 2], [3, 7]], [[1, 1], [6, 3], [4, 7]], [[4, 2], [3, 3], [2, 8]], [[3, 0], [1, 8], [0, 2]], [[0, 1], [0, 5], [0, 6]], [[4, 7], [0, 2], [7, 8]]], [[[2, 4], [8, 0], [8, 5]], [[2, 3], [2, 2], [2, 3]], [[2, 5], [1, 8], [2, 2]], [[0, 0], [2, 8], [6, 4]], [[3, 7], [7, 7], [7, 6]], [[3, 4], [8, 6], [7, 8]], [[4, 1], [8, 3], [0, 1]], [[8, 3], [5, 7], [1, 5]]], [[[3, 0], [1, 4], [7, 2]], [[2, 5], [7, 1], [7, 1]], [[0, 2], [3, 2], [7, 7]], [[6, 1], [2, 0], [3, 5]], [[6, 2], [2, 2], [3, 6]], [[5, 2], [5, 5], [2, 7]], [[0, 8], [7, 0], [8, 4]], [[6, 7], [8, 4], [1, 5]]], [[[8, 4], [2, 7], [4, 5]], [[8, 4], [7, 1], [5, 
0]], [[4, 6], [7, 3], [0, 8]], [[8, 6], [3, 7], [4, 5]], [[2, 7], [3, 8], [1, 0]], [[5, 2], [4, 4], [3, 6]], [[4, 0], [8, 5], [1, 6]], [[0, 2], [1, 2], [7, 0]]], [[[7, 5], [4, 7], [1, 5]], [[8, 0], [3, 8], [6, 2]], [[5, 7], [6, 
0], [2, 6]], [[8, 3], [6, 7], [3, 8]], [[1, 2], [6, 7], [2, 2]], [[7, 3], [0, 1], [7, 3]], [[2, 1], [6, 4], [6, 1]], [[1, 2], [0, 5], [2, 4]]], [[[8, 8], [5, 6], [3, 3]], [[0, 7], [0, 0], [2, 4]], [[4, 1], [8, 8], [8, 8]], [[7, 
1], [1, 2], [5, 8]], [[6, 8], [1, 0], [5, 1]], [[7, 5], [2, 4], [1, 5]], [[5, 1], [7, 3], [2, 8]], [[5, 0], [1, 1], [8, 6]]], [[[5, 2], [8, 0], [8, 3]], [[7, 4], [5, 6], [5, 4]], [[0, 5], [0, 7], [5, 0]], [[2, 3], [6, 7], [5, 6]], [[8, 5], [1, 1], [1, 3]], [[8, 2], [1, 4], [0, 1]], [[0, 6], [3, 7], [2, 4]], [[3, 8], [7, 1], [3, 8]]], [[[7, 5], [5, 7], [4, 4]], [[7, 5], [4, 6], [4, 6]], [[8, 8], [2, 0], [8, 6]], [[3, 4], [0, 8], [0, 8]], [[6, 5], [0, 5], [5, 8]], [[0, 0], [7, 2], [6, 2]], [[8, 2], [6, 0], [8, 3]], [[6, 5], [1, 5], [0, 0]]]], 'dim': 0, 'out': [[[[87, 26], [62, 56], [67, 72]], [[7, 92], [41, 25], [52, 22]], [[15, 85], [56, 6], [68, 83]], [[93, 56], [58, 26], [86, 54]], [[52, 84], [22, 45], [42, 7]], [[68, 18], [22, 75], [8, 14]], [[30, 7], [48, 92], [38, 74]], [[57, 79], [49, 30], [23, 22]]], [[[69, 97], [7, 63], [12, 17]], [[56, 92], [7, 45], [52, 58]], [[86, 91], [7, 6], [96, 17]], [[91, 43], [0, 26], [99, 26]], [[19, 51], [11, 23], [84, 7]], [[72, 35], [14, 28], [10, 94]], [[19, 6], [7, 72], [31, 58]], [[36, 94], [45, 32], [66, 4]]], [[[49, 97], [43, 45], [54, 0]], [[7, 90], [51, 93], [61, 80]], [[87, 12], [7, 55], [39, 20]], [[93, 13], [91, 23], [72, 4]], [[24, 84], [22, 90], [13, 4]], [[72, 64], [24, 75], [84, 66]], [[81, 6], [19, 55], [31, 72]], [[93, 20], [49, 24], [68, 22]]], [[[49, 93], [62, 45], [41, 52]], [[7, 87], [41, 4], [80, 79]], [[34, 79], [0, 6], [50, 17]], [[58, 43], [91, 36], [61, 45]], [[3, 51], [82, 25], [47, 4]], [[65, 87], [56, 61], [18, 57]], [[19, 19], [47, 65], [25, 62]], [[92, 94], [3, 8], [68, 22]]], [[[87, 97], [7, 49], [43, 0]], [[0, 0], [41, 4], [80, 35]], [[14, 57], [37, 27], [68, 5]], [[98, 9], [38, 74], [99, 45]], [[87, 84], [11, 43], [53, 35]], [[65, 87], [80, 26], [58, 42]], [[81, 94], [19, 72], [83, 58]], [[1, 60], [87, 32], [66, 80]]], [[[69, 84], [0, 49], [53, 0]], [[0, 33], [26, 45], [53, 22]], [[4, 60], [91, 84], [39, 94]], [[98, 99], [0, 74], [61, 24]], [[69, 51], [53, 90], [84, 66]], [[91, 90], [78, 57], [84, 14]], [[84, 6], [51, 60], [96, 72]], [[58, 60], [45, 30], [25, 64]]], [[[87, 83], [79, 2], [55, 93]], [[93, 92], [40, 25], [61, 95]], [[14, 91], [62, 55], [5, 5]], [[74, 43], [58, 83], [68, 24]], [[3, 76], [88, 83], [42, 69]], [[91, 18], [52, 26], [96, 7]], [[93, 6], [47, 55], [67, 32]], [[14, 48], [87, 40], [23, 59]]], [[[27, 9], [43, 45], [54, 93]], [[32, 0], [7, 2], [80, 95]], [[34, 12], [59, 51], [86, 18]], [[4, 99], [0, 74], [68, 44]], [[9, 23], [88, 45], [53, 65]], [[50, 87], [14, 26], [10, 15]], [[19, 7], [98, 76], [67, 62]], [[49, 7], [66, 40], [44, 4]]], [[[69, 84], [79, 49], [43, 17]], [[32, 87], [11, 2], [42, 7]], [[86, 3], [7, 84], [5, 94]], [[87, 92], [56, 23], [40, 24]], [[3, 23], [47, 30], [42, 7]], [[10, 35], 
[14, 13], [8, 94]], [[72, 78], [51, 65], [25, 88]], [[92, 83], [87, 30], [58, 80]]]], 'grad': [[[[0.0, 1.0], [0.0, 2.0], [1.0, 0.0]], [[1.0, 1.0], [1.0, 2.0], [1.0, 1.0]], [[2.0, 1.0], [1.0, 2.0], [2.0, 1.0]], [[2.0, 1.0], [1.0, 1.0], [1.0, 0.0]], [[1.0, 0.0], [1.0, 1.0], [0.0, 1.0]], [[1.0, 2.0], [1.0, 0.0], [2.0, 0.0]], [[3.0, 1.0], [1.0, 2.0], [2.0, 0.0]], [[1.0, 1.0], [2.0, 0.0], [1.0, 2.0]]], [[[0.0, 0.0], [2.0, 1.0], [1.0, 1.0]], [[0.0, 0.0], [0.0, 2.0], [0.0, 1.0]], [[0.0, 2.0], [1.0, 0.0], [0.0, 1.0]], [[1.0, 3.0], [2.0, 0.0], [0.0, 0.0]], [[1.0, 0.0], [2.0, 2.0], [2.0, 1.0]], [[0.0, 0.0], [2.0, 1.0], [1.0, 1.0]], [[0.0, 4.0], [0.0, 0.0], [1.0, 2.0]], [[1.0, 1.0], [3.0, 2.0], [2.0, 0.0]]], [[[1.0, 1.0], [2.0, 0.0], [1.0, 1.0]], [[3.0, 0.0], [1.0, 1.0], [2.0, 2.0]], [[1.0, 1.0], [2.0, 3.0], [2.0, 1.0]], [[1.0, 0.0], [2.0, 1.0], [1.0, 1.0]], [[1.0, 3.0], [1.0, 1.0], [2.0, 1.0]], [[0.0, 3.0], [1.0, 1.0], [1.0, 2.0]], [[1.0, 1.0], [0.0, 0.0], [2.0, 0.0]], [[0.0, 2.0], [0.0, 2.0], [1.0, 0.0]]], [[[1.0, 0.0], [0.0, 1.0], [1.0, 2.0]], [[1.0, 1.0], [1.0, 0.0], [0.0, 1.0]], [[0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [[1.0, 2.0], [1.0, 2.0], [2.0, 0.0]], [[1.0, 0.0], [2.0, 1.0], [1.0, 1.0]], [[2.0, 1.0], [0.0, 0.0], [1.0, 2.0]], [[1.0, 0.0], [1.0, 2.0], [0.0, 1.0]], [[1.0, 1.0], [0.0, 0.0], [1.0, 0.0]]], [[[0.0, 3.0], [1.0, 1.0], [2.0, 2.0]], [[0.0, 2.0], [1.0, 0.0], [1.0, 2.0]], [[2.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 1.0], [0.0, 0.0], [2.0, 1.0]], [[1.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[1.0, 1.0], [1.0, 3.0], [0.0, 0.0]], [[2.0, 0.0], [0.0, 1.0], [0.0, 2.0]], [[1.0, 0.0], [0.0, 1.0], [0.0, 1.0]]], [[[1.0, 2.0], [2.0, 0.0], [0.0, 3.0]], [[0.0, 2.0], [2.0, 0.0], [2.0, 0.0]], [[1.0, 2.0], [1.0, 0.0], [1.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [2.0, 2.0]], [[0.0, 2.0], [0.0, 1.0], [3.0, 0.0]], [[2.0, 2.0], [1.0, 1.0], [0.0, 1.0]], [[1.0, 0.0], [1.0, 2.0], [1.0, 1.0]], [[1.0, 1.0], [2.0, 3.0], [0.0, 3.0]]], [[[0.0, 1.0], [0.0, 1.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 2.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 0.0], [0.0, 2.0]], [[1.0, 1.0], [3.0, 0.0], [1.0, 1.0]], [[3.0, 0.0], [1.0, 0.0], [0.0, 2.0]], [[0.0, 0.0], [1.0, 2.0], [2.0, 1.0]], [[0.0, 2.0], [2.0, 0.0], [1.0, 2.0]], [[2.0, 0.0], [0.0, 0.0], [0.0, 1.0]]], [[[3.0, 0.0], [0.0, 3.0], [1.0, 0.0]], [[2.0, 2.0], [3.0, 0.0], [1.0, 0.0]], [[0.0, 1.0], [1.0, 1.0], [1.0, 2.0]], [[1.0, 0.0], [0.0, 3.0], [0.0, 1.0]], [[0.0, 3.0], [2.0, 2.0], [1.0, 0.0]], [[2.0, 0.0], [1.0, 0.0], [2.0, 1.0]], [[0.0, 0.0], [2.0, 1.0], [0.0, 0.0]], [[1.0, 2.0], [1.0, 1.0], [2.0, 0.0]]], [[[3.0, 1.0], [2.0, 0.0], [2.0, 0.0]], [[2.0, 1.0], [0.0, 2.0], [1.0, 1.0]], [[2.0, 1.0], [1.0, 2.0], [2.0, 2.0]], [[2.0, 1.0], [0.0, 2.0], [0.0, 3.0]], [[1.0, 1.0], [0.0, 1.0], [0.0, 3.0]], [[1.0, 0.0], [1.0, 1.0], [0.0, 1.0]], [[1.0, 1.0], [2.0, 1.0], [2.0, 1.0]], [[1.0, 1.0], [1.0, 0.0], [2.0, 2.0]]], [[[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], 
[[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]]]}]

def _make_gather_dim_fn(
    test_case, input, index, dim, grad, device_type, value_type, index_type, machine_ids, device_counts, mirrored
):
    flow.clear_default_session()
    if device_type == "cpu":
        flow.config.gpu_device_num(1)
        machine_ids = "0:0"
    else:
        flow.config.gpu_device_num(device_counts)
    
    func_config = flow.FunctionConfig()
    func_config.default_data_type(value_type)

    if mirrored:
        func_config.default_logical_view(flow.scope.mirrored_view())
    else:
        func_config.default_logical_view(flow.scope.consistent_view())

    if mirrored:
        pass
    else:
        def _compare_diff(blob: oft.Numpy):
            print("##", grad.shape, blob.shape)
            print("##", grad)
            print("##", blob)
            test_case.assertTrue(
                np.array_equal(grad, blob)
            )

    def do_gather(x_blob, i_blob):
        with flow.scope.placement(device_type, machine_ids):
            x = flow.get_variable(
                "input",
                shape=input.shape,
                dtype=value_type,
                initializer=flow.constant_initializer(0),
            )
            x = flow.cast_to_current_logical_view(x)
            x_blob = flow.cast_to_current_logical_view(x_blob)
            x = x + x_blob

            y = flow.gather_dim(x, dim, i_blob)
            flow.watch_diff(x, _compare_diff)
        flow.optimizer.SGD(
            flow.optimizer.PiecewiseConstantScheduler([], [1e-3]), momentum=0
        ).minimize(y)
        return y

    @flow.global_function(type="train", function_config=func_config)
    def gather_fn(
        params_def: oft.Numpy.Placeholder(input.shape, dtype=value_type),
        indices_def: oft.Numpy.Placeholder(index.shape, dtype=index_type),
    ):
        return do_gather(params_def, indices_def)

    return gather_fn


def _compare_gatherdim_with_samples(
    test_case,
    device_type,
    sample,
    value_type,
    index_type,
    machine_ids,
    device_counts,
    mirrored=False,
):
    input = np.array(sample["input"]).astype(value_type[0])
    index = np.array(sample["index"]).astype(index_type[0])
    out = np.array(sample["out"]).astype(np.float32)
    dim = sample["dim"]
    grad = np.array(sample["grad"]).astype(value_type[0])

    params, indices = input, index
    gather_fn = _make_gather_dim_fn(
        test_case, params, indices, dim, grad, device_type, value_type[1], index_type[1], machine_ids, device_counts, mirrored
    )

    if mirrored:
        of_y = gather_fn([params], [indices]).get().numpy_list()[0]
    else:
        of_y = gather_fn(params, indices).get().numpy()

    test_case.assertTrue(np.array_equal(out, of_y))


def test_gather_dim_cpu(test_case):
    global g_samples
    arg_dict = OrderedDict()
    arg_dict["device_type"] = ["cpu"]
    arg_dict["samples"] = g_samples
    arg_dict["value_type"] = [(np.float32, flow.float32), (np.double, flow.double)]
    arg_dict["index_type"] = [(np.int32, flow.int32), (np.int64, flow.int64)]
    arg_dict["machine_ids"] = ["0:0-0"]
    arg_dict["device_count"] = [1]
    for arg in GenArgList(arg_dict):
        _compare_gatherdim_with_samples(
            test_case, *arg
        )

def test_gather_dim_gpu(test_case):
    global g_samples
    arg_dict = OrderedDict()
    arg_dict["device_type"] = ["gpu"]
    arg_dict["samples"] = g_samples
    arg_dict["value_type"] = [(np.float32, flow.float32), (np.double, flow.double)]
    arg_dict["index_type"] = [(np.int32, flow.int32), (np.int64, flow.int64)]
    arg_dict["machine_ids"] = ["0:0-0"]
    arg_dict["device_count"] = [1]
    for arg in GenArgList(arg_dict):
        _compare_gatherdim_with_samples(
            test_case, *arg
        )

# def test_gather_dim_2cards(test_case):
#     global g_samples
#     arg_dict = OrderedDict()
#     arg_dict["device_type"] = ["gpu"]
#     arg_dict["samples"] = g_samples
#     arg_dict["value_type"] = [(np.float32, flow.float32), (np.double, flow.double)]
#     arg_dict["index_type"] = [(np.int32, flow.int32), (np.int64, flow.int64)]
#     arg_dict["machine_ids"] = ["0:0-1"]
#     arg_dict["device_count"] = [2]
#     for arg in GenArgList(arg_dict):
#         _compare_gatherdim_with_samples(
#             test_case, *arg
#         )

