#!/usr/bin/env python2.7

import argparse
import base64  # The two used for encodings multiple values
import cPickle as pickle  # into one, to be passed from mapper to reducer
from mrjob.job import MRJob  # Extended to make a mr job
import numpy as np  # Useful matrix functionality

# CONSTANTS
MU = 0.1


# TODO: Probably remove this method when moving to categorical features.
def numerify_feature(feature):
    if feature == '?':
        feature = 0.0
    return float(feature)


def extract_features(array):
    """
        Given a line of the input csv as an array of values.
        Return the features of the line (all but the last value) with
            numerical values substituted for categorical.
    """
    # TODO: One-Hot encoding of categorical features
    features = array[1:-1]
    return [numerify_feature(f) for f in features]


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


class MRIterativeSVM(MRJob):
    """
        Implementation of the iterative SVM machine learning algorithm
         leveraging the Hadoop MapReduce system for parallel execution.
    """

    def __init__(self, *args, **kwargs):
        super(MRIterativeSVM, self).__init__(*args, **kwargs)

    def transform_input(self, _, line):
        line_array = line.split(',')
        features = extract_features(line_array)
        category = extract_category(line_array)
        yield category, features

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
        key, value = self.transform_input(line_num, line)

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
