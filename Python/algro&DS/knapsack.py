def knapsack(wLst,vLst,idx,weight,dic):
    if (idx,weight) in dic.keys():
        return dic[(idx,weight)]
    if weight == 0 or idx < 0 : return 0
    if wLst[idx] > weight: return knapsnap(wLst,vLst,idx-1,weight,dic)
    dic[(idx,weight)] = max(vLst[idx]+knapsnap(wLst,vLst,idx-1,weight-wLst[idx],dic),
                            knapsnap(wLst,vLst,idx-1,weight,dic)
                            )
    return dic[(idx,weight)]


def main(wLst,vlst,weight):
    dic = {}
    return knapsnap(wLst,vlst,len(wLst)-1,weight,dic)


ls1 = [10, 30, 100, 35, 50, 130]
ls2 = [1, 2, 10, 4, 6, 12]
print main(ls2,ls1,15)
