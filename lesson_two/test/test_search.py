import pytest
from lesson_two.src.main import *

@pytest.mark.parametrize(
    'arr, x'
    [
        ([i for i in range(10)], 7),
        ([i for i in range(10)][::-1], 7)

    ]
)

def test_search_array(arr, x):
    assert search_array(arr, x)

# def search_in_sparce_array(arr, x):
#     start, end = 0, len(arr) -1
#
#     while start <= end:
#         mid = start + end // 2
#
#         if arr[mid] is None:
#             start_index, end_index = mid - 1, mid + 1
#
#             while True:
#                 if start >= start_index and end >= end_index:
#                     return -1
#                 elif start <= start_index and arr[start_index] is not None:
#                     mid = start_index
#                     break
#                 elif end >= end_index and arr[end_index] is not None:
#                     mid = end_index
#                     break
#                 start_index -= 1
#                 end_index += 1
#
#         if arr[mid] == x:
#             return mid
#         elif arr[mid] < x:
#             start += 1
#         else:
#             end -= 1
#
#     return -1
#
# arr = [1, 2, None, None, 5, 6, 7, None, 10, 11]
#
# print(search_in_sparce_array(arr, 5))
# print(search_in_sparce_array(arr, 1))
# print(search_in_sparce_array(arr, 9))
#
# #Tests
#
# def test_search_in_sparse_array():
#     arr = [1, 2, None, None, 5, 6, 7, None, 10, 11]
#
#     assert search_in_sparce_array([], 1) == -1
