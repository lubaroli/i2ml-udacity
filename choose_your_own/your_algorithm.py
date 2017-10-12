#!/usr/bin/python

import matplotlib.pyplot as plt
from prep_terrain_data import makeTerrainData
from class_vis import prettyPicture
from sklearn.ensemble import (AdaBoostClassifier,
                              BaggingClassifier, RandomForestClassifier)
from sklearn.neighbors import KNeighborsClassifier

features_train, labels_train, features_test, labels_test = makeTerrainData()

# the training data (features_train, labels_train) have both "fast" and "slow"
# points mixed together--separate them so we can give them different colors
# in the scatterplot and identify them visually
grade_fast = [features_train[ii][0] for ii in range(0, len(features_train)) if
              labels_train[ii] == 0]
bumpy_fast = [features_train[ii][1] for ii in range(0, len(features_train)) if
              labels_train[ii] == 0]
grade_slow = [features_train[ii][0] for ii in range(0, len(features_train)) if
              labels_train[ii] == 1]
bumpy_slow = [features_train[ii][1] for ii in range(0, len(features_train)) if
              labels_train[ii] == 1]


# initial visualization
plt.xlim(0.0, 1.0)
plt.ylim(0.0, 1.0)
plt.scatter(bumpy_fast, grade_fast, color="b", label="fast")
plt.scatter(grade_slow, bumpy_slow, color="r", label="slow")
# plt.legend()
# plt.xlabel("bumpiness")
# plt.ylabel("grade")
# plt.show()
###############################################################################

# your code here!  name your classifier object clf if you want the
# visualization code (prettyPicture) to show you the decision boundary
clf_adaboost = AdaBoostClassifier(n_estimators=20)
clf_adaboost.fit(features_train, labels_train)
# prettyPicture(clf_adaboost, features_test, labels_test)
score = ["adaboost", clf_adaboost.score(features_test, labels_test)]

clf_randomforest = RandomForestClassifier(n_estimators=100)
clf_randomforest.fit(features_train, labels_train)
# prettyPicture(clf_randomforest, features_test, labels_test)
score.append(["randomforest", clf_randomforest.score(features_test,
                                                     labels_test)])

clf_bagging = BaggingClassifier(KNeighborsClassifier(n_neighbors=5),
                                max_samples=0.25, n_estimators=10)
clf_bagging.fit(features_train, labels_train)
prettyPicture(clf_bagging, features_test, labels_test)
score.append(["kNN", clf_bagging.score(features_test,
                                       labels_test)])

print score
plt.show()

try:
    prettyPicture(clf, features_test, labels_test)
except NameError:
    pass
