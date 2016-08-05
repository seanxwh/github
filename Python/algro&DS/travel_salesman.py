def travelSaleMan(arr, start, prvNodes, org):
    if len(prvNodes) == len(arr):
            return arr[start][org]
    minDst = float('inf')
    for idx in range(len(arr)):
        if idx not in prvNodes:
            tmp = prvNodes[:]
            tmp.append(idx)
            minDst = min(arr[start][idx]+travelSaleMan(arr,idx, tmp, org),
                            minDst)
    return minDst

def main(arr, org):
    numCities = len(arr)
    prvNodes = [org]
    return travelSaleMan(arr, org, prvNodes, org)






org = 0
disAry = [[0, 20, 42, 35], [20, 0, 30, 34], [42, 30, 0, 12], [35, 34, 12, 0]]
print main(disAry, org)
