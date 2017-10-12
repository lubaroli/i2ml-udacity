#!/usr/bin/python

"""
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails the Enron corpus by their authors:
    Sara has label 0
    Chris has label 1
"""

import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()


#########################################################
### your code goes here ###

#########################################################

from sklearn import svm

clf = svm.SVC(kernel='rbf', C=10000)

# features_train = features_train[:len(features_train)/100]
# labels_train = labels_train[:len(labels_train)/100]

t0 = time()
clf.fit(features_train, labels_train)
t_train = time() - t0

t0 = time()
accuracy = clf.score(features_test, labels_test)
t_test = time() - t0
print "training time:", round(t_train, 3), "s"
print "prediction time:", round(t_test, 3), "s"
print "average accuracy:", round(accuracy, 4)
print "emails written by Chris:", clf.predict(features_test).tolist().count(1)
