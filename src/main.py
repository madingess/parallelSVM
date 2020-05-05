#!/usr/bin/env python2.7

import argparse
import subprocess
import re
import time
from helper_functions import transform_input


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


# Record total time to run application
total_time_start = time.time()


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
test_set = lines[:int(num_lines * split_ratio)]
train_set = lines[int(num_lines * split_ratio):]
with open(train_filename, 'w') as train_writer:
    for train_line in train_set:
        train_writer.write(train_line)


# Invoke MRIterativeSVM implementation on the training data
# Run in new process to capture output values.
print("Training Iterative SVM with MapReduce...")
#TODO: track training time
alg_training_time_start = time.time()
alg_output = subprocess.check_output(["python", "src/mr_svm.py", train_filename],
                                     stderr=subprocess.STDOUT)
alg_training_time = time.time() - alg_training_time_start
if debug:
    print("\nMapReduce Job Output:")
    print(alg_output)


# Parse algorithm parameters
mr_output_str_array = alg_output.split("\n")[-3].split("\"")[3]
weight_str_arrays = re.findall('\[.+?\]', mr_output_str_array[1:-1])
weights = [float(weight_str_array[1:-1])
           for weight_str_array in weight_str_arrays]


# Evaluate train set using weight parameters
train_eval_time_start = time.time()
num_train = len(train_set)
num_train_correct = 0
for train_line in train_set:
    true_category, feature_values = transform_input("", train_line)

    result = 0.0
    for i in range(len(feature_values)):
        result += feature_values[i] * weights[i]

    if result >= 1.0:
        predicted_category = 1.0
    else:
        predicted_category = -1.0
    if predicted_category == true_category:
        num_train_correct += 1

percent_train_correct = float(num_train_correct) / float(num_train) * 100
train_eval_time = time.time() - train_eval_time_start


# Evaluate test set using weight parameters
test_eval_time_start = time.time()
num_test = len(test_set)
num_test_correct = 0
for test_line in test_set:
    true_category, feature_values = transform_input("", test_line)

    result = 0.0
    for i in range(len(feature_values)):
        result += feature_values[i] * weights[i]

    if result >= 1.0:
        predicted_category = 1.0
    else:
        predicted_category = -1.0
    if predicted_category == true_category:
        num_test_correct += 1

percent_test_correct = float(num_test_correct) / float(num_test) * 100
test_eval_time = time.time() - test_eval_time_start


# Record total time to run application, excluding statistic printing
total_time = time.time() - total_time_start

# Print statistics
#TODO: Rounding of percent values
print("\nAlgorithm trained weights")
print weights

print("\nResults")
print "(", num_lines - int(num_lines * split_ratio), " train, ",
      int(num_lines * split_ratio), " test)"
print "Total correct on training set: ", num_train_correct, "(",
      percent_train_correct, "%)"
print "Total correct on testing set: ", num_test_correct, "(",
      percent_test_correct, "%)"

print("\nComputation Time")
print "Algorithm training time: ", alg_training_time
print "Training set evaluation time: ", train_eval_time
print "Testing set evaluation time: ", test_eval_time
print "Total system runtime: ", total_time
