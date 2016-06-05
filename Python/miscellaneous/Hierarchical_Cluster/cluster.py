from math import sqrt
import numpy as np
from pearsonCor import pearsonCor


class buildCluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left=left
        self.right=right
        self.vec=vec
        self.id=id
        self.distance=distance

def hcluster(rows,distance=pearsonCor):
    #  initialize the id for first merged cluster
    mergedClusterId=-1
    clusterDistances={}
    clusters=[buildCluster(rows[i],id=i) for i in range(len(rows))]
    #  loop thru all the avaliable clusters
    while len(clusters)>1:
    #   start from the first two clusters in the avaliable "clusters"
        lowestValueClustersPair=(0,1)
        #   initialize the closest distance by using the first two clusters
        closestDistance=distance(clusters[0].vec,clusters[1].vec)
        #   loop thru all avaliable "clusters"
        for i in range(len(clusters)):
         #   take the ith cluster and compare to the following "clusters"
            for k in range(i+1,len(clusters)):
                if (clusters[i].id,clusters[k].id) not in clusterDistances:
                    clusterDistances[(clusters[i].id,clusters[k].id)]=distance(clusters[i].vec,clusters[k].vec)
                d=clusterDistances[(clusters[i].id,clusters[k].id)]
                # replace closest pair and their distance if the current pair has smaller distance
                if (d<closestDistance):
                    lowestValueClustersPair=(i,k)
                    closestDistance=d
        # after finish finding the closest pair in this("the while loop") set of "clusters"
        mergedClusterVec=[(a+b)/2 for a,b in zip(clusters[lowestValueClustersPair[0]].vec,clusters[lowestValueClustersPair[1]].vec)]
        #  mergedClusterVec=[(clusters[lowestValueClustersPair[0]].vec[i]+clusters[lowestValueClustersPair[1]].vec[i])/2
        #         for i in range(len(clusters[0].vec))]

        mergedCluster=buildCluster(
                            mergedClusterVec,
                            left=clusters[lowestValueClustersPair[0]],
                            right=clusters[lowestValueClustersPair[1]],
                            distance=closestDistance,
                            id=mergedClusterId
                            )
        # decreamented the next id for merged cluster
        mergedClusterId-=1
        # remove the lowest pair since it is inside the merged cluster(0 idx last other wise error)
        del clusters[lowestValueClustersPair[1]]
        del clusters[lowestValueClustersPair[0]]
        clusters.append(mergedCluster)
    return clusters[0]


# def hcluster(rows,distance=pearsonCor):
#     distances={}
#     currentClusterId=-1
#     clust=[buildCluster(rows[i],id=i) for i in range(len(rows))]
#
#     while len(clust)>1:
#         print '\n'
#         for itm in clust:
#             print itm.id
#         lowestpair=(0,1)
#         closest=distance(clust[0].vec,clust[1].vec)
#         #check the distance of a cluster with all its flow cluster
#         for i in range(len(clust)):
#             for j in range(i+1,len(clust)):
#                 if (clust[i].id,clust[j].id) not in distances:
#                     distances[clust[i].id,clust[j].id]=distance(clust[i].vec,clust[j].vec)
#                 d=distances[(clust[i].id,clust[j].id)]
#                 # if d is smaller than closest, replace the closest
#                 # print clust[i].id,clust[j].id,"\n"
#                 if d<closest:
#                     closest=d
#                     lowestpair=(i,j)
#
#         # cal the new average of the two cluster
#         mergeVec=[(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2
#                 for i in range(len(clust[0].vec))]
#
#         newCluster=buildCluster(mergeVec,
#                                 left=clust[lowestpair[0]],
#                                 right=clust[lowestpair[1]],
#                                 distance=closest,
#                                 id=currentClusterId)
#         currentClusterId-=1
#         print "del",clust[lowestpair[1]].id
#         del clust[lowestpair[1]]
#         print "del",clust[lowestpair[0]].id
#         del clust[lowestpair[0]]
#         clust.append(newCluster)
#     return clust[0]
