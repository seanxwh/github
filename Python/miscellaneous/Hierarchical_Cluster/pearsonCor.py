from math import sqrt
import numpy as np

# def pearsonCor(v1,v2):
#     if (isinstance(v1, list)
#         and isinstance(v2,list)
#         and len(v1)==len(v2)):
#         #refer to https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
#         length=len(v1)
#         sum1=sum(v1)
#         sum2=sum(v2)
#         expV1=sum1/length
#         expV2=sum2/length
#         expV1Sq=sum(pow(elm,2) for elm in v1)/length
#         expV2Sq=sum(pow(elm,2) for elm in v2)/length
#         expV1V2=sum(v1[i]*v2[i] for i in range(length))/length
#         stdX=(expV1Sq-pow(expV1,2))
#         stdY=(expV2Sq-pow(expV2,2))
#         if (stdX*stdY==0):
#             return 0
#         r=(expV1V2-expV1Sq*expV2Sq)/sqrt(stdX*stdY)
#         invertR=1-r
#         return invertR
#     else:
#         raise ValueError


def pearsonCor(v1,v2):
    print v1,"\n",v2
    if (isinstance(v1, list)
        and isinstance(v2,list)
        and len(v1)==len(v2)):
        #refer to https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
        length=len(v1)
        sum1=np.sum(v1)
        sum2=np.sum(v2)
        expV1=sum1/length
        expV2=sum2/length
        expV1Sq=np.sum(np.dot(v1,v1))/length
        expV2Sq=np.sum(np.dot(v2,v2))/length
        expV1V2=np.sum(np.dot(v1,v2))/length
        stdX=(expV1Sq-pow(expV1,2))
        stdY=(expV2Sq-pow(expV2,2))
        if (stdX*stdY==0):
            return 0
        r=(expV1V2-expV1Sq*expV2Sq)/sqrt(stdX*stdY)
        invertR=1-r
        return invertR
    else:
        raise ValueError
