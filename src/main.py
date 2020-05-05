#!/usr/bin/env python2.7

import argparse
import subprocess
from mr_svm import MRIterativeSVM


def define_args(arg_parser):
    """Defines program arguments"""
    arg_parser.description = 'Driver program for mr_svm.py, an implementation ' \
                             'of the iterative SVM machine learning algorithm ' \
                             'leveraging the Hadoop MapReduce system for ' \
                             'parallel execution. This performs train/test ' \
                             'splitting and model evaluation.'

    arg_parser.add_argument('input_data', nargs=1, type=str,
                            help='CSV file of data formatted in accordance '
                                 'with the adult data dataset.')

    arg_parser.add_argument('-r', '--train_filename', type=str,
                            default='tmp/adult_train.data',
                            help='Output for filename for data split into '
                                 'training set.')
    arg_parser.add_argument('-t', '--test_filename', type=str,
                            default='tmp/adult_test.data',
                            help='Output for filename for data split into '
                                 'testing set.')
    arg_parser.add_argument('-s', '--split', type=float, default='0.2',
                            help='Training/Testing data split value. Default '
                                 '0.2, defaults splits first 20p of file into '
                                 'testing and remaining 80p into training.')
    arg_parser.add_argument('-o', '--observe_first_line', default=True,
                            action='store_false',
                            help='Observes first line of csv, default false.')
    arg_parser.add_argument('-d', '--debug', default=False, action='store_true',
                            help='Run in verbose mode. Prints more stuff.')


# Parse command line arguments
parser = argparse.ArgumentParser()
define_args(parser)
arguments = parser.parse_args()

input_filename = arguments.input_data[0]
train_filename = arguments.train_filename
test_filename = arguments.test_filename
split_ratio = arguments.split
observe_first_line = arguments.observe_first_line
debug = arguments.debug
if debug:
    print("Inputs:")
    print(input_filename)
    print(train_filename)
    print(test_filename)
    print(split_ratio)
    print(observe_first_line)
    print(debug)
    print("")


# Get input data
if debug:
    print("Reading input file...")
num_lines = 0
lines = []
with open(input_filename, 'r') as all_data:
    for line in all_data:
        num_lines += 1
        lines.append(line)

# Split input data into training and test files
if debug:
    print("Splitting input into training and testing files...")
with open(test_filename, 'w') as test_writer:
    for test_line in lines[:int(num_lines * split_ratio)]:
        test_writer.write(test_line)
with open(train_filename, 'w') as train_writer:
    for train_line in lines[int(num_lines * split_ratio):]:
        train_writer.write(train_line)


# Invoke MRIterativeSVM implementation on the training data
# Run in new process to capture output values.
print("Training Iterative SVM with MapReduce...")
#alg = MRIterativeSVM(train_filename)
#abc = alg.run()

alg_output = subprocess.check_output(["python", "src/mr_svm.py", train_filename],
                                     stderr=subprocess.STDOUT)#.decode(
#    'utf-8').split("\n")
print("alg_output:")
print(alg_output)
