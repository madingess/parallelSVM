#!/usr/bin/env python2.7


import base64                   # The two used for encodings multiple values
import cPickle as pickle        #  into one, to be passed from mapper to reducer
from mrjob.job import MRJob     # Extended to make a mr job
import numpy as np              # Useful matrix functionality
from helper_functions import transform_input


# CONSTANTS
MU = 0.1


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


# Run the algorithm if this file is invoked directly
if __name__ == '__main__':
    MRIterativeSVM.run()
