def LIS(arr, idx, ref, dic):
    if idx < 0:
        return 0
    if (idx, ref) in dic.keys():
        return dic[(idx, ref)]
    if arr[idx] <= ref:
        res = 1+LIS(arr, idx-1, arr[idx], dic)
    else:
        res = max(LIS(arr, idx-1, arr[idx], dic),
                LIS(arr, idx-1, ref, dic))
    dic[(idx, ref)] = res
    return dic[(idx, ref)]

def main(arr):
    res = 0
    dic = {}
    idx = len(arr)-1
    ref = float('inf')
    return LIS(arr, idx, ref, dic)

arr = [10 , 22 , 9 , 33 , 21 , 50 , 41 , 60]
# arr= [-7,10,9,2,3,8,8,1]
# arr = [12,8,9,15,16,17,10,11]
print main(arr)
