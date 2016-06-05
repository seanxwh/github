from math import sqrt
import numpy as np
import random as random
from pearsonCor import pearsonCor


def multiDimScaling(data,distance=pearsonCor,rate=0.01):
    n=len(data)

    clusterDistances=[[distance(data[i],data[j]) for j in range(n)] for i in range(0,n)]

    outerSum=0.0

    loc=[[random.random(),random.random()] for i in range(n)]

    dummyDistances=[[0.0 for j in range(n)] for i in range(n)]

    lastError=None

    for m in range(0,1000):

        for i in range(n):

            for j in range(n):

                dummyDistances[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2)
                                        for x in range(len(loc[i]))]))

            grad=[[0.0,0.0] for i in range(n)]

            totalError=0

            for k in range(n):

                for j in range(n):

                    if j==k: continue

                    errorTerm=(dummyDistances[j][k]-clusterDistances[j][k])/clusterDistances[j][k]

                    grad[k][0]+=((loc[k][0]-loc[j][0])/dummyDistances[j][k])*errorTerm

                    grad[k][1]+=((loc[k][1]-loc[j][1])/dummyDistances[j][k])*errorTerm

                    totalError+=abs(errorTerm)

            print totalError

            if lastError and lastError<totalError: break

            lastError=totalError

            for k in range(n):

                loc[k][0]-=rate*grad[k][0]

                loc[k][1]-=rate*grade[k][1]

        return loc
