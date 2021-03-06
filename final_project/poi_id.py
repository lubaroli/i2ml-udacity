#!/usr/bin/python

import sys
import pickle
from tester import dump_classifier_and_data
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC

sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from poi_tools import data_dict_points, data_dict_min_max_scale
from poi_tools import data_dict_add_ratio


def clf_scorer(clfs, y, X_test, X_test_tree=None):
    """Computes the F1 score for the classifiers tested by GridSearchCV

    :clfs: list with classifier objects from GridSearchCV
    :X_test: list with test features
    :X_test_tree: optional list with test features for tree based classifiers
    :y: list with test labels
    :returns: returns best classifier based on F1 score

    """
    score = []
    for clf in clfs:
        try:
            score.append(f1_score(labels_test, clf.predict(features_test_tree),
                         average='weighted'))
        except:
            score.append(f1_score(labels_test, clf.predict(features_test),
                         average='weighted'))
    return clfs[score.index(max(score))].best_estimator_


def eval_clf(clf, param_grid, scoring_metric, cv_strat, X, y):
    """Performs a GridSearchCV with clf, using param_grid values. Score for best
    estimator is based on scoring_metric. Optionally uses a cross validation
    strategy defined by cv_strat.

    :clf: classifier to be evaluated
    :param_grid: dictionary of evaluation parameters
    :scoring_metric: string defining the scoring metric for evaluation
    :cv_strat: list of CV indices to be used for training
    :X: list of training features
    :y: list of training labels
    :returns: returns the fitted best estimator for clf

    """
    from time import time

    t0 = time()
    clf = GridSearchCV(clf, param_grid, scoring=scoring_metric, cv=cv_strat)
    clf = clf.fit(X, y)
    print("done in %0.3fs" % (time() - t0))
    print("Best estimator found by grid search:")
    print(clf.best_estimator_)
    return clf


def expand_data(X, y, n_splits=1000, test_size=0.3, random_state=42):
    """TODO: Docstring for expand_data.

    :X: list of features
    :y: list of labels
    :n_splits: number of times the list will be multiplied
    :test_size: percentage of the list reserved for testing
    :random_state: pseudo-random constant
    :returns: expanded list divided into train and test lists

    """
    from sklearn.model_selection import StratifiedShuffleSplit

    sss = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_size,
                                 random_state=random_state)
    for train_index, test_index in sss.split(X, y):
        X_train = []
        X_test = []
        y_train = []
        y_test = []
        for ii in train_index:
            X_train.append(X[ii])
            y_train.append(y[ii])
        for jj in test_index:
            X_test.append(X[jj])
            y_test.append(y[jj])
    return X_train, X_test, y_train, y_test


# Task 1: Select what features you'll use.
# features_list is a list of strings, each of which is a feature name.
# The first feature must be "poi".
features_list = ['poi',
                 'salary', 'deferral_payments', 'total_payments',
                 'bonus', 'restricted_stock_deferred',
                 'deferred_income', 'total_stock_value', 'expenses',
                 'exercised_stock_options', 'long_term_incentive',
                 'restricted_stock', 'director_fees', 'other',
                 'from_poi_to_this_person', 'from_this_person_to_poi',
                 'shared_receipt_with_poi']

# Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# Task 2: Remove outliers
data_dict.pop("TOTAL", 0)    # Remove total line from data
data_dict.pop('LOCKHART EUGENE E', 0)
# data_dict.pop('SKILLING JEFFREY K', 0)
# data_dict.pop('LAY KENNETH L', 0)

###############################################################################
# Task 3: Create new feature(s)
data_dict_add_ratio(data_dict, 'salary', 'bonus', 'sal/bon')
features_list += ['sal/bon']

data_dict_add_ratio(data_dict, 'salary', 'total_stock_value',
                    'sal/stock')
features_list += ['sal/stock']

data_dict_add_ratio(data_dict, 'from_poi_to_this_person', 'to_messages',
                    'fraction_from_poi')
features_list += ['fraction_from_poi']

data_dict_add_ratio(data_dict, 'from_this_person_to_poi', 'from_messages',
                    'fraction_to_poi')
features_list += ['fraction_to_poi']

# Store to my_dataset for easy export below. Note that this is a pointer to the
# same dictionary.
my_dataset = data_dict
data_dict_min_max_scale(data_dict, features_list)

# Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

# Print some dataset insight
n_samples = len(labels)
n_features = len(features[0])

print("\nTotal dataset size:")
print("n_samples: %d" % n_samples)
print("n_features: %d" % n_features)

###############################################################################
# Task 4: Try a varity of classifiers
# Please name your classifier clf for easy export below.
# Note that if you want to do PCA or other multi-stage operations,
# you'll need to use Pipelines. For more info:
# http://scikit-learn.org/stable/modules/pipeline.html
# Example starting point. Try investigating other evaluation techniques!
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

# Optional: Expand data using Stratified Shuffle Split
# Results are worsening with use, perhaps try with non-stratified?

# features_train, features_test, labels_train, labels_test = \
#     expand_data(features, labels, test_size=0.3, random_state=42)

# GridSearchCV does the StratifiedKFold split on the dataset based on cv_strat
cv_strat = 3
scoring_metric = 'f1_weighted'

# Task 5: Tune your classifier to achieve better than .3 precision and recall
# using our testing script. Check the tester.py script in the final project
# folder for details on the evaluation method, especially the test_classifier
# function. Because of the small size of the dataset, the script uses
# stratified shuffle split cross validation. For more info:
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

###############################################################################
# Quantitative evaluation of the Decision Tree model quality on the test set

# Use this features for best performance with Decision Tree and AdaBoost
features_list_tree = ['shared_receipt_with_poi', 'fraction_from_poi',
                      'fraction_to_poi']
# data = featureFormat(my_dataset, features_list, sort_keys=True)
# labels, features = targetFeatureSplit(data)
# features_train, features_test, labels_train, labels_test = \
#     train_test_split(features, labels, test_size=0.3, random_state=42)
features_train_tree = []
features_test_tree = []
for row in features_train:
    # subtract 1 from index as POI is removed from features_list
    features_train_tree.append([row[features_list.index(key)-1]
                                for key in features_list_tree])
for row in features_test:
    # subtract 1 from index as POI is removed from features_list
    features_test_tree.append([row[features_list.index(key)-1]
                               for key in features_list_tree])

print("\nFitting the Decision Tree classifier to the training set")
param_grid_DTC = {
    'min_samples_split': [2, 3, 4, 5, 6, 7, 8],
    'criterion': ['gini', 'entropy'],
}
clf_DTC = eval_clf(DecisionTreeClassifier(class_weight='balanced',
                                          max_features=3, random_state=42),
                   param_grid_DTC, scoring_metric, cv_strat,
                   features_train_tree, labels_train)


print("Predicting the POIs on the testing set")
labels_pred = clf_DTC.predict(features_test_tree)
print(classification_report(labels_test, labels_pred,
                            target_names=['Non-POI', 'POI']))
print(confusion_matrix(labels_test, labels_pred))

###############################################################################
# Quantitative evaluation of the AdaBoost model quality on the test set
print("\nFitting the AdaBoost classifier to the training set")
param_grid_ABC = {
    'n_estimators': [10, 20, 50, 100],
    'learning_rate': [0.01, 0.05, 0.1, 0.5, 1]
}
base_DTC = DecisionTreeClassifier(class_weight='balanced')
clf_ABC = eval_clf(AdaBoostClassifier(base_estimator=base_DTC),
                   param_grid_ABC, scoring_metric, cv_strat,
                   features_train_tree, labels_train)

print("Predicting the POIs on the testing set")
labels_pred = clf_ABC.predict(features_test_tree)
print(classification_report(labels_test, labels_pred,
                            target_names=['Non-POI', 'POI']))
print(confusion_matrix(labels_test, labels_pred))

print("\nFeatures selected by Decision Tree and AdaBoost")
counter = 0
feats_used = clf_DTC.best_estimator_.max_features_
for n, v in sorted(zip(features_list_tree,
                       clf_DTC.best_estimator_.feature_importances_),
                   key=lambda k: k[1], reverse=True):
    print("Feature '%s' - Score: %0.3f, Datapoints: %i"
          % (n, v, data_dict_points(data_dict, n)))
    counter += 1
    if counter == feats_used:
        break

###############################################################################
# Do feature selection to choose k best performing features for KNN and SVC
selector = SelectKBest(f_classif, k=3)
features = selector.fit_transform(features, labels)

###############################################################################
# Quantitative evaluation of the SVC model quality on the test set
print("\nFitting the SVC classifier to the training set")
param_grid_SVC = {
    'C': [1, 500, 1e3, 5e3, 1e4],
    'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1, 'auto'],
    'kernel': ['rbf', 'linear']
}
clf_SVC = eval_clf(SVC(class_weight='balanced'), param_grid_SVC,
                   scoring_metric, cv_strat, features_train, labels_train)

print("Predicting the POIs on the testing set")
labels_pred = clf_SVC.predict(features_test)

print(classification_report(labels_test, labels_pred,
                            target_names=['Non-POI', 'POI']))
print(confusion_matrix(labels_test, labels_pred))

###############################################################################
# Quantitative evaluation of the K-Nearest Neighbors model quality on the test
# set
print("\nFitting the KNN classifier to the training set")
param_grid_KNN = {
    'n_neighbors': [5, 15, 25],
    'weights': ['uniform', 'distance'],
}
clf_KNN = eval_clf(KNeighborsClassifier(), param_grid_KNN,
                   scoring_metric, cv_strat, features_train, labels_train)

print("Predicting the people names on the testing set")
labels_pred = clf_KNN.predict(features_test)
print(classification_report(labels_test, labels_pred,
                            target_names=['Non-POI', 'POI']))
print(confusion_matrix(labels_test, labels_pred))

print("\nFeatures selected for SVC and KNN")
counter = 0
feats_used = selector.k
for n, v in sorted(zip(features_list[1:], selector.scores_),
                   key=lambda k: k[1], reverse=True):
    print("Feature '%s' - Score: %0.3f, Datapoints: %i"
          % (n, v, data_dict_points(data_dict, n)))
    counter += 1
    if counter == feats_used:
        break

# Task 6: Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.
print("\nBest classifier found:")
clf_results = [clf_KNN, clf_ABC, clf_SVC, clf_DTC]
clf = clf_scorer(clf_results, labels_test, features_test, features_test_tree)
print(clf)

dump_classifier_and_data(clf, my_dataset, features_list)
