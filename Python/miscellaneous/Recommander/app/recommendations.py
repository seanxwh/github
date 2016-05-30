import sys
# import imp
from math import sqrt
# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
 # Get the list of shared_items
 si={}
 for item in prefs[person1]:
     if item in prefs[person2]:
        si[item]=1
 # if they have no ratings in common, return 0
 if len(si)==0: return 0
 # Add up the squares of all the differences
 sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                    for item in prefs[person1] if item in prefs[person2]])
 return 1/(1+sum_of_squares)


def sim_pearson(prefs,p1,p2):
    if(type(prefs) is dict
        and p1 in prefs
        and p2 in prefs):
        # Get the list of mutually rated items
        si={}
        for item in prefs[p1]:
            if item in prefs[p2]: si[item]=1
        # Find the number of elements
        n=len(si)
        # if they are no ratings in common, return 0
        if n==0: return 0
        # Add up all the preferences
        sum1=sum([prefs[p1][it] for it in si])
        sum2=sum([prefs[p2][it] for it in si])
        # Sum up the squares
        sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
        sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
        # Sum up the products
        pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
        # Calculate Pearson score
        num=pSum-(sum1*sum2/n)
        den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
        if den==0: return 0
        r=num/den
        return r

    else:
        raise ValueError


def topMatches(prefs,target,num=5,similarity=sim_pearson):
    if (type(prefs) is dict
        and target in prefs
        and isinstance(target, basestring)
        and isinstance(num,int)
        and hasattr(similarity,'__call__')):

        list=[[similarity(prefs,target,other),other]
                    for other in prefs if other!=target]
        list.sort()
        list.reverse()
        return list[0:num]

    else:
        raise ValueError


def getRecommendations(prefs,target,similarity=sim_pearson):
    if (type(prefs) is dict
        and target in prefs
        and isinstance(target, basestring)
        and hasattr(similarity,'__call__')):

        similarityDict={other:similarity(prefs,target,other)
            for other in prefs if other!=target}
        itemsScore={};
        similaritySumScore={}
        for owner in prefs:
            if (owner!=target):
                for item in prefs[owner]:
                    if (similarityDict[owner]>=0 and item not in prefs[target]):
                        if item not in itemsScore:
                            itemsScore[item]=0
                            similaritySumScore[item]=0
                        itemsScore[item]+=similarityDict[owner]*prefs[owner][item]
                        similaritySumScore[item]+=similarityDict[owner]
        newItemsRating=[(itemsScore[item]/similaritySumScore[item],item) for item in itemsScore]
        newItemsRating.sort()
        newItemsRating.reverse()
        return newItemsRating

    else:
        raise ValueError

# def getRecommendations(prefs,owner,similarity=sim_pearson):
#  totals={}
#  simSums={}
#  for other in prefs:
#      # don't compare me to myself
#      if other==owner: continue
#      sim=similarity(prefs,owner,other)
#      # ignore scores of zero or lower
#      if sim<=0: continue
#      for item in prefs[other]:
#          # only score movies I haven't seen yet
#          if item not in prefs[owner] or prefs[owner][item]==0:
#              # Similarity * Score
#              totals.setdefault(item,0)
#              totals[item]+=prefs[other][item]*sim
#              # Sum of similarities
#              simSums.setdefault(item,0)
#              simSums[item]+=sim
#  # Create the normalized list
#  rankings=[(total/simSums[item],item) for item,total in totals.items( )]
#  # Return the sorted list
#  rankings.sort()
#  rankings.reverse()
#  return rankings



def transformPrefs(prefs):
    result={}
    for owner in prefs:
        for item in prefs[owner]:
            result.setdefault(item,{})
     # Flip item and owner
            result[item][owner]=prefs[owner][item]
    return result


def transformAryToDict(prefs):
    if(type(prefs) is dict):
        newPrefs={}
        for key in prefs:
            newPrefs[key]={}
            for itm in prefs[key]:
                newPrefs[key][itm[1]]=itm[0]
        return newPrefs
    else:
        raise ValueError


def calSimilarItems(prefs,num=10):
    if(type(prefs) is dict
        and isinstance(num,int)):
        #first transform prefs form {owner1:{item1:XX, item2:XX}, owner2:{item1:XX, item2:XX}}
        # to{item1:{owner1:XX owner2:XX},item1:{owner1:XX owner2:XX}}
        itemsDict=transformPrefs(prefs)
        itemSimlarityDict={}
        for item in itemsDict:
            itemSimlarityDict[item]=topMatches(itemsDict,item,similarity=sim_distance)
        return itemSimlarityDict
    else:
        raise ValueError


def calRecommendationItems(prefs,simiItemsScore,target):
    if (type(prefs) is dict
        and type (simiItemsScore) is dict
        and isinstance(target,basestring)
        and target in prefs):
        newSimiItemsScore=transformAryToDict(simiItemsScore)
        sumAdjustedSimilarityScore={}
        sumUnadjustedSimilarityScore={}
        adjustedSimilarityScore={}
        items = prefs[target].keys()
        for itm in newSimiItemsScore:
            if (itm in items):
                for subfield in newSimiItemsScore[itm]:
                    if (subfield not in items):
                        if (subfield not in sumUnadjustedSimilarityScore and subfield not in sumAdjustedSimilarityScore):
                            sumUnadjustedSimilarityScore[subfield]=0
                            sumAdjustedSimilarityScore[subfield]=0
                        sumUnadjustedSimilarityScore[subfield]+=newSimiItemsScore[itm][subfield]
                        sumAdjustedSimilarityScore[subfield]+=newSimiItemsScore[itm][subfield]*prefs[target][itm]
        for field in sumUnadjustedSimilarityScore:
            adjustedSimilarityScore[field]=sumAdjustedSimilarityScore[field]/sumUnadjustedSimilarityScore[field]
        return adjustedSimilarityScore
    else:
        raise ValueError
