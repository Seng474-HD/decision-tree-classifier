import csv
import numpy as np
import pdb
from sklearn import tree
import time
import os


DATA_FILE_PATH = '../hd-data/output/months/jan.csv'

CLASS_LABEL_INDEX = -1
NUM_ATTRS = 91
NUM_ROWS = 1915631 # manually checked because eff reading the whole thing in first

NUM_TRAIN_ROWS = 1500000
NUM_PRED_ROWS = 1500000

# this loads just the january data

X = np.zeros((NUM_ROWS, NUM_ATTRS))
Y = np.zeros(NUM_ROWS)

start_time = time.time()
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
print('Time elapsed: ')
print(end_time - start_time)

X_train = X[:NUM_TRAIN_ROWS]
X_test = X[NUM_TRAIN_ROWS:]

Y_train = Y[:NUM_TRAIN_ROWS]
Y_test = Y[NUM_TRAIN_ROWS:]

pdb.set_trace()
clf = tree.DecisionTreeClassifier()
clf.fit(X, Y)

