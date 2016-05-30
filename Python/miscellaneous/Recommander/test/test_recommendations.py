import sys
import nose
from nose.tools import *
from app.recommendations import critics,sim_pearson,topMatches,getRecommendations,transformPrefs,calSimilarItems,calRecommendationItems,transformAryToDict

assert_equal(topMatches(critics,'Toby',3,sim_pearson)[0],[0.9912407071619299, 'Lisa Rose'])
assert_raises(ValueError,topMatches,critics,'Toby','three',sim_pearson)
assert_equal(getRecommendations(critics,'Toby',sim_pearson), [(3.3477895267131013, 'The Night Listener'), (2.8325499182641614, 'Lady in the Water'), (2.5309807037655645, 'Just My Luck')])
assert_raises(ValueError,getRecommendations,critics,'Sean')
assert_equal(transformPrefs({'Lisa Rose':{'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5}}),
                                            {'Lady in the Water': {'Lisa Rose': 2.5},
                                            'Snakes on a Plane': {'Lisa Rose': 3.5}})
# movies=transformPrefs(critics)
# assert_equal(topMatches(movies,'Superman Returns'),
#                                 [(0.657, 'You, Me and Dupree'),(0.487, 'Lady in the Water'),
#                                 (0.111, 'Snakes on a Plane'), (-0.179, 'The Night Listener'),
#                                  (-0.422, 'Just My Luck')])
# assert_equal(getRecommendations(movies,'Just My Luck'),
#                                         [(4.0, 'Michael Phillips'),
#                                          (3.0, 'Jack Matthews')])
assert_equal(transformAryToDict({'Lady in the Water': [[0.7637626158259785, 'Snakes on a Plane'],
                                                        [0.4879500364742689, 'Superman Returns']]}),
                                {'Lady in the Water': {'Snakes on a Plane': 0.7637626158259785,
                                                        'Superman Returns': 0.4879500364742689}})

simiItms=calSimilarItems(critics)
assert_equal(simiItms,
            {'Lady in the Water': [[0.4, 'You, Me and Dupree'], [0.2857142857142857, 'The Night Listener'], [0.2222222222222222, 'Snakes on a Plane'], [0.2222222222222222, 'Just My Luck'], [0.09090909090909091, 'Superman Returns']],
            'Snakes on a Plane': [[0.2222222222222222, 'Lady in the Water'], [0.18181818181818182, 'The Night Listener'], [0.16666666666666666, 'Superman Returns'], [0.10526315789473684, 'Just My Luck'], [0.05128205128205128, 'You, Me and Dupree']],
            'Just My Luck': [[0.2222222222222222, 'Lady in the Water'], [0.18181818181818182, 'You, Me and Dupree'], [0.15384615384615385, 'The Night Listener'], [0.10526315789473684, 'Snakes on a Plane'], [0.06451612903225806, 'Superman Returns']],
            'Superman Returns': [[0.16666666666666666, 'Snakes on a Plane'], [0.10256410256410256, 'The Night Listener'], [0.09090909090909091, 'Lady in the Water'], [0.06451612903225806, 'Just My Luck'], [0.05333333333333334, 'You, Me and Dupree']],
            'You, Me and Dupree': [[0.4, 'Lady in the Water'], [0.18181818181818182, 'Just My Luck'], [0.14814814814814814, 'The Night Listener'], [0.05333333333333334, 'Superman Returns'], [0.05128205128205128, 'Snakes on a Plane']],
            'The Night Listener': [[0.2857142857142857, 'Lady in the Water'], [0.18181818181818182, 'Snakes on a Plane'], [0.15384615384615385, 'Just My Luck'], [0.14814814814814814, 'You, Me and Dupree'], [0.10256410256410256, 'Superman Returns']]})

assert_equal(calRecommendationItems(critics,simiItms,'Toby'),
                                    {'Lady in the Water': 2.4730878186968837,
                                     'Just My Luck': 2.5983318700614575,
                                     'The Night Listener': 3.182634730538922})
if __name__ == '__main__':
    unittest.main()
