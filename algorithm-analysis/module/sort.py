from random import randint

def _merge(arr1, arr2):
    i, j = 0, 0
    arr = [None for _ in arr1 + arr2]

    for x in range(len(arr)):
        if i < len(arr1) and j < len(arr2):
            if arr1[i] < arr2[j]:
                arr[x] = arr1[i]
                i += 1
            else:
                arr[x] = arr2[j]
                j += 1
        elif i < len(arr1):
            arr[x] = arr1[i]
            i += 1
        else:
            arr[x] = arr2[j]
            j += 1
    return arr
    
def merge_sort(A):
    n = len(A)
    if n <= 1:
        return A
    
    m = n //2
    arr1 = merge_sort(A[:m]) # T(floor(n/2))
    arr2 = merge_sort(A[m:]) # T(ceil(n/2))
    return _merge(arr1, arr2) # Theta(n)


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    index = randint(0, len(arr) - 1) 
    left, right = _partition(arr, index)
    left = quick_sort(left)
    right = quick_sort(right)
    return left + [arr[index]] + right


def _partition(arr, index):
    pivot = arr[index]
    return [e for i, e in enumerate(arr) if e <= pivot and i != index], [e for e in arr if e > pivot]

def quick_select(arr, r):
    index = randint(0, len(arr) - 1) 
    left, right = _partition(arr, index)
    if len(left) == r:
        return arr[index]

    if r > len(left):
        return quick_select(right, r-len(left)-1)
    
    return quick_select(left, r)
