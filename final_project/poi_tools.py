#!/usr/bin/python

import matplotlib.pyplot as plt


def data_dict_min_max_scale(data_dict, features):
    """Scales the data_dict according to the features list using the min-max
    algorithm. Data may be composed of numbers and strings.

    :data_dict: dictionary of Enron data
    :features: list of features to be scaled on the Enron dictionary
    :returns: data_dict with scaled features

    """
    for feat in features:
        feat_max = max(
            data_dict[name][feat]
            for name in data_dict.keys()
            if isinstance(data_dict[name][feat], (float, int))
        )

        feat_min = min(
            data_dict[name][feat]
            for name in data_dict.keys()
            if isinstance(data_dict[name][feat], (float, int))
        )

        base = feat_max - feat_min

        for name in data_dict.keys():
            if isinstance(data_dict[name][feat], int):
                data_dict[name][feat] = float(
                    (data_dict[name][feat]-feat_min)) / base

    return data_dict


def plot_data(d, feats, labels=''):
    """Creates a scatter plot of two features in the Enron data_dict, and
    optionally colors POIs in red.

    :d: Enron data_dict file
    :feats: List of length 2 with the two features used in the plot
    :labels: Optional list with data labels

    """
    if labels == '':
        labels = [0]*len(d.values()[0][feats[0]])
    else:
        i = 0
        for keys in d:
            if labels[i] == 0:
                plt.scatter(d[keys][feats[0]], d[keys][feats[1]], color='blue')
            else:
                plt.scatter(d[keys][feats[0]], d[keys][feats[1]], color='red')
            i += 1
        plt.xlabel(feats[0])
        plt.ylabel(feats[1])
        plt.show()


def data_dict_points(data_dict, feature):
    """Returns the number of valid entry points for a given data_dict feature

    :data_dict: dictionary of Enron data
    :feature: feature which will be evaluated
    :returns: number of valid data points, i.e. not 'NaN'

    """
    return len(filter(lambda k: isinstance(data_dict[k][feature],
                                           (int, float)), data_dict))


def data_dict_max(data_dict, feature):
    """Returns the maximum value of a feature in the data_dict. Data may be
    composed of floats, integers and strings.

    :data_dict: dictionary of Enron data
    :features: list of features to be scaled on the Enron dictionary
    :returns: name (key) and max value of a data_dict feature

    """
    name = max(filter(lambda k: isinstance(data_dict[k][feature],
               (int, float)), data_dict), key=lambda k: data_dict[k][feature])

    return name, data_dict[name][feature]


def data_dict_add_total(data_dict, sum_args, feat_name):
    """Adds the ratio of numerator/denominator as a new feature to data_dict.

    :data_dict: dictionary of Enron data
    :sum_args: list of feature to be summed into new feature
    :feat_name: name of the new feature
    :returns: adds the new feature to data_dict

    """
    for key in data_dict:
        data_dict[key][feat_name] = 0
        for feat in sum_args:
            if data_dict[key][feat] != 'NaN':
                data_dict[key][feat_name] += data_dict[key][feat]


def data_dict_add_ratio(data_dict, numerator, denominator, feat_name):
    """Adds the ratio of numerator/denominator as a new feature to data_dict.

    :data_dict: dictionary of Enron data
    :numerator: feature to be used as the numerator
    :denominator: feature to be used as the denominator
    :feat_name: name of the new feature
    :returns: adds the new feature to data_dict

    """
    for key in data_dict:
        if (data_dict[key][numerator] == 'NaN' or
            data_dict[key][denominator] == 'NaN'):
                data_dict[key][feat_name] = 'NaN'
        else:
                data_dict[key][feat_name] = (
                    1.0*data_dict[key][numerator]/data_dict[key][denominator]
                )
