#!/usr/bin/env python2.7

import argparse
import base64                   # The two used for encodings multiple values
import cPickle as pickle        #  into one, to be passed from mapper to reducer
from mrjob.job import MRJob     # Extended to make a mr job
import numpy as np              # Useful matrix functionality

# CONSTANTS
MU = 0.1

# ENCODINGS; One-Hot encoding would be preferred, but does not work with svm afaik
WORK_CLASS_INDEX = 1
EDUCATION_INDEX = 3
MARITAL_STATUS_INDEX = 5
OCCUPATION_INDEX = 6
RELATIONSHIP_INDEX = 7
RACE_INDEX = 8
SEX_INDEX = 9
NATIVE_COUNTRY_INDEX = 13
WORK_CLASS = {'Private': 1.0, 'Self-emp-not-inc': 2.0, 'Self-emp-inc': 3.0, 'Federal-gov': 4.0, 'Local-gov': 5.0, 'State-gov': 6.0, 'Without-pay': 7.0, 'Never-worked': 8.0}
EDUCATION = {'Bachelors': 1.0, 'Some-college': 2.0, '11th': 3.0, 'HS-grad': 4.0, 'Prof-school': 5.0, 'Assoc-acdm': 6.0, 'Assoc-voc': 7.0, '9th': 8.0, '7th-8th': 9.0, '12th': 10.0, 'Masters': 11.0, '1st-4th': 12.0, '10th': 13.0, 'Doctorate': 14.0, '5th-6th': 15.0, 'Preschool': 16.0}
MARITAL_STATUS = {'Married-civ-spouse': 1.0, 'Divorced': 2.0, 'Never-married': 3.0, 'Separated': 4.0, 'Widowed': 5.0, 'Married-spouse-absent': 6.0, 'Married-AF-spouse': 7.0}
OCCUPATION = {'Tech-support': 1.0, 'Craft-repair': 2.0, 'Other-service': 3.0, 'Sales': 4.0, 'Exec-managerial': 5.0, 'Prof-specialty': 6.0, 'Handlers-cleaners': 7.0, 'Machine-op-inspct': 8.0, 'Adm-clerical': 9.0, 'Farming-fishing': 10.0, 'Transport-moving': 11.0, 'Priv-house-serv': 12.0, 'Protective-serv': 13.0, 'Armed-Forces': 14.0}
RELATIONSHIP = {'Wife': 1.0, 'Own-child': 2.0, 'Husband': 3.0, 'Not-in-family': 4.0, 'Other-relative': 5.0, 'Unmarried': 6.0}
RACE = {'White': 1.0, 'Asian-Pac-Islander': 2.0, 'Amer-Indian-Eskimo': 3.0, 'Other': 4.0, 'Black': 5.0}
SEX = {'Female': -1.0, 'Male': 1.0}
NATIVE_COUNTRY = {'United-States': 1.0, 'Cambodia': 2.0, 'England': 3.0, 'Puerto-Rico': 4.0, 'Canada': 5.0, 'Germany': 6.0, 'Outlying-US(Guam-USVI-etc)': 7.0, 'India': 8.0, 'Japan': 9.0, 'Greece': 10.0, 'South': 11.0, 'China': 12.0, 'Cuba': 13.0, 'Iran': 14.0, 'Honduras': 15.0, 'Philippines': 16.0, 'Italy': 17.0, 'Poland': 18.0, 'Jamaica': 19.0, 'Vietnam': 20.0, 'Mexico': 21.0, 'Portugal': 22.0, 'Ireland': 23.0, 'France': 24.0, 'Dominican-Republic': 25.0, 'Laos': 26.0, 'Ecuador': 27.0, 'Taiwan': 28.0, 'Haiti': 29.0, 'Columbia': 30.0, 'Hungary': 31.0, 'Guatemala': 32.0, 'Nicaragua': 33.0, 'Scotland': 34.0, 'Thailand': 35.0, 'Yugoslavia': 36.0, 'El-Salvador': 37.0, 'Trinadad&Tobago': 38.0, 'Peru': 39.0, 'Hong': 40.0, 'Holand-Netherlands': 41.0}


def numerify_feature(feature, index):
    if feature == '?':
        return 0.0
    else:
        return {
            WORK_CLASS_INDEX: WORK_CLASS[feature],
            EDUCATION_INDEX: EDUCATION[feature],
            MARITAL_STATUS_INDEX: MARITAL_STATUS[feature],
            OCCUPATION_INDEX: OCCUPATION[feature],
            RELATIONSHIP_INDEX: RELATIONSHIP[feature],
            RACE_INDEX: RACE[feature],
            SEX_INDEX: SEX[feature]
        }.get(index, feature)   # Switch statement replaced, default: feature

    return float(feature)


def extract_features(line_array):
    """
        Given a line of the input csv as an array of values.
        Return the features of the line (all but the last value) with
            numerical values substituted for categorical.
    """
    features = line_array[1:-1]
    return [numerify_feature(features[i], i) for i in range(len(features))]


def extract_category(line_array):
    """
        Given a line of the input csv as an array of values.
        Compare the last value (the category) and return
            -1.0 if income is less than or equal to 50k
            1.0  if income is greater than 50k
    """
    neg_cat = "<=50K"
    category = line_array[-1].strip()
    return -1.0 if category == neg_cat else 1.0


def transform_input(_, line):
    line_array = line.split(',')
    features = extract_features(line_array)
    category = extract_category(line_array)
    yield category, features


class MRIterativeSVM(MRJob):
    """
        Implementation of the iterative SVM machine learning algorithm
         leveraging the Hadoop MapReduce system for parallel execution.
    """

    def __init__(self, *args, **kwargs):
        super(MRIterativeSVM, self).__init__(*args, **kwargs)

    def mapper(self, line_num, line):
        """
            Mapper class.
            Variables as in "Incremental Support Vector Machine Classification":
                 features_matrix: A
                 training_classes_matrix: D
                 identity_matrix: e
                 E: E
            Computations are according to the paper above.
            Maps a feature line into a tuple with the values to be used by
             the reducer. We perform as much computation in the mapper as possible.
        """
        # Extract category and features from input line
        key, value = transform_input(line_num, line)

        num_training_features = len(value)

        features_matrix = np.matrix(
            np.reshape(np.array(value),
                       (1, num_training_features)))
        training_classes_matrix = np.diag([key])
        identity_matrix = np.matrix(np.ones(len(features_matrix))
                                    .reshape(len(features_matrix), 1))
        E = np.matrix(np.append(features_matrix, -identity_matrix, axis=1))

        # Encode tuple of two values needed by the reducer into one value for mr
        values_tuple = base64.b64encode(pickle.dumps((E.T * E,
                                                      E.T * training_classes_matrix * identity_matrix)))

        # a key is needed by mr, but not for out application
        yield "outputkey", values_tuple

    def reducer(self, key, values_tuples):
        """
            All values have same key.
            Values is a set of encoded tuples of two values each, used for
             computation.
            Computation proceeds according to paper mentioned in mapper.
        """
        mu = MU  # constant above

        sum_ETE = None
        sum_ETDe = None
        for values in values_tuples:
            ETE, ETDe = pickle.loads(base64.b64decode(values))  # decode values

            if sum_ETE is None:
                sum_ETE = np.matrix(np.eye(ETE.shape[1]) / mu)
            sum_ETE += ETE

            if sum_ETDe is None:
                sum_ETDe = ETDe
            else:
                sum_ETDe += ETDe

        result = sum_ETE.I * sum_ETDe
        yield key, str(result.tolist())


if __name__ == '__main__':
    MRIterativeSVM.run()
