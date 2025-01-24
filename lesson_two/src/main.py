
def search_array(arr, x):
    start, end = 0, len(arr) - 1

    if not isinstance(arr, list):
        raise TypeError('Введенный Вами первый элемент не является списком')
    if not all(isinstance(i, (int, type(None))) for i in arr):
        raise TypeError('Список должен содержать целые числа или тип None')
    if not isinstance(x, (int, type(None))):
        raise TypeError('Искомый элемент должен быть целым числом или None')

    while start <= end:
        mid = (start + end) // 2

        if arr[mid] is None:
            start_index, end_index = mid - 1, mid + 1

            while True:
                if start_index < start and end_index > end:
                    return -1
                elif start <= start_index and arr[start_index] is not None:
                    mid = start_index
                    break
                elif end >= end_index and arr[end_index] is not None:
                    mid = end_index
                    break
                start_index -= 1
                end_index += 1

        if arr[mid] == x:
            return mid
        elif arr[mid] is not None and x is not None:
            if arr[mid] < x:
                start += 1
            else:
                end -= 1
        elif x is None:
            return -1

    return -1

arr = [1, 2, None, None, 5, 6, 7, None, 10, 11]

print(search_array(arr, 8))
print(search_array(arr, 11))
print(search_array(arr, None))
print(search_array(arr, 5))
print(search_array(arr, 2))
print(search_array("АБВ", 5))
print(search_array([1, 2.5, "АБВ"], 5))
print(search_array(arr, ''))



