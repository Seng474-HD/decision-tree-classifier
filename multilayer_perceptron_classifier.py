import csv
import numpy as np
import pdb
from sklearn.neural_network import MLPClassifier
import time
import os


DATA_FILE_PATH = '../hd-data/output/months/jan.csv'

CLASS_LABEL_INDEX = -1
NUM_ATTRS = 91
NUM_ROWS = 1915631 # manually checked because eff reading the whole thing in first

NUM_TRAIN_ROWS = NUM_ROWS//5

# this loads just the january data

X = np.zeros((NUM_ROWS, NUM_ATTRS))
Y = np.zeros(NUM_ROWS)

start_time = time.time()
print("hi")
with open(DATA_FILE_PATH, 'r') as input_file:
    reader = csv.reader(input_file, delimiter=',', quotechar='|')
    reader.__next__() # skip header

    row_idx = 0
    for row in reader:
        # row[4:-1] is attributes minus date, serial_number, model, and capacity_bytes
        int_row = list(map(lambda x: int(x) if x else 0, row[4:-1]))
        X[row_idx] = int_row

        label = row[CLASS_LABEL_INDEX]
        Y[row_idx] = label
        row_idx += 1

end_time = time.time()
print('Time elapsed: ', end_time - start_time)

clf = MLPClassifier(activation='logistic', solver='sgd', learning_rate='adaptive', learning_rate_init=0.1, verbose='true', hidden_layer_sizes=(100, 70, 50))

totalerrors = 0
for i in range(5):
    X_train = np.append(X[:NUM_TRAIN_ROWS*i], X[NUM_TRAIN_ROWS*(i+1):], axis=0)
    X_test = X[NUM_TRAIN_ROWS*i:NUM_TRAIN_ROWS*(i+1)]
    
    Y_train = np.append(Y[:NUM_TRAIN_ROWS*i], Y[NUM_TRAIN_ROWS*(i+1):], axis=0)
    Y_test = Y[NUM_TRAIN_ROWS*i:NUM_TRAIN_ROWS*(i+1)]

    print('Fitting classifier on training data')
    clf.fit(X_train, Y_train)

    print('Predicting labels of test data')
    preds = clf.predict(X_test)
    
    print('Calculating prediction error')
    errors = np.mean(preds != Y_test)
    totalerrors = errors + totalerrors
    print('Prediction error: ', errors)  

avgerrors = totalerrors/5

baseline_preds = np.zeros(len(preds))
print('Average prediction error: ', avgerrors)
baseline_errors = np.mean(baseline_preds != Y_test)
print('Baseline error (always predicting non-fail): ', baseline_errors)

