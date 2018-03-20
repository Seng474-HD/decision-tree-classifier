import csv
import numpy as np
import pdb
from sklearn import tree
import time
import os


DATA_FILE_PATH = '../hd-data/output/months/jan.csv'

CLASS_LABEL_INDEX = -1
NUM_ATTRS = 10
NUM_ROWS = 1915631 # manually checked because eff reading the whole thing in first

NUM_TRAIN_ROWS = 1500000
NUM_PRED_ROWS = 1500000

# SMART stats from the decision tree paper
# 1- Raw Read Error Rate - 
# 3 - Spin Up Time
# 5 Reallocated Sectors Count
# 5 Reallocated Sectors Count (raw value)
# 7 Seek Error Rate
# 9 Power On Hours
# 187 Reported Uncorrectable Errors
# 189 High Fly Writes
# 194 Temperature Celsius
# 195 Hardware ECC Recovered

RAW_READ_ERR_RATE_IDX = 6
SPIN_UP_TIME_IDX = 9
REALL_SEC_COUNT_IDX = 13
RAW_REALL_SEC_COUNT_IDX = 14
SEEK_ERR_RATE_IDX = 15
POWER_ON_HRS_IDX = 19
REP_UNCORR_ERRS_IDX = 37
HIGH_FLY_WRITES_IDX = 41
TEMP_CELCIUS = 51
HW_ECC_RECOVERED_IDX = 53

# 5 Reallocated Sectors Count (raw value)
# 7 Seek Error Rate
# 9 Power On Hours
# 187 Reported Uncorrectable Errors
# 189 High Fly Writes
# 194 Temperature Celsius
# 195 Hardware ECC Recovered


# this loads just the january data

def prune_row(row=[]):
    pruned_row = []
    pruned_row.append(row[RAW_READ_ERR_RATE_IDX])
    pruned_row.append(row[SPIN_UP_TIME_IDX])
    pruned_row.append(row[REALL_SEC_COUNT_IDX])
    pruned_row.append(row[RAW_REALL_SEC_COUNT_IDX])
    pruned_row.append(row[SEEK_ERR_RATE_IDX])
    pruned_row.append(row[POWER_ON_HRS_IDX])
    pruned_row.append(row[REP_UNCORR_ERRS_IDX])
    pruned_row.append(row[HIGH_FLY_WRITES_IDX])
    pruned_row.append(row[TEMP_CELCIUS])
    pruned_row.append(row[HW_ECC_RECOVERED_IDX])
    return pruned_row


X = np.zeros((NUM_ROWS, NUM_ATTRS))
Y = np.zeros(NUM_ROWS)


print("Reading data")
start_time = time.time()

with open(DATA_FILE_PATH, 'r') as input_file:
    reader = csv.reader(input_file, delimiter=',', quotechar='|')
    next(reader) # skip header

    row_idx = 0
    for row in reader:
        pruned_row = prune_row(row)
        pruned_row = list(map(lambda x: int(x) if x else 0, pruned_row))
        X[row_idx] = pruned_row

        label = row[CLASS_LABEL_INDEX]
        Y[row_idx] = label
        row_idx += 1

end_time = time.time()
print('Time elapsed: ', end_time - start_time)


X_train = []
X_test = []

if os.environ.get('BALANCE_TYPE') is not None:
    X_fail = []
    X_non_fail = []
    Y_fail = []
    Y_non_fail = []
    num_failures = 0
    for i in range(len(X)):
        row_train = X[i]
        row_class = Y[i]
        if row_class == 1:
            num_failures += 1
            X_fail.append(row_train)
            Y_fail.append(row_class)
        else:
            X_non_fail.append(row_train)
            Y_non_fail.append(row_class)

    if os.environ['BALANCE_TYPE'] == "oversample":
        X_fail = X_fail * 100
        Y_fail = Y_fail * 100
        num_failures = num_failures * 100

    num_train = (num_failures*9)/10
    X_non_fail = X_non_fail[:num_failures]
    Y_non_fail = Y_non_fail[:num_failures]

    X_train = X_fail[:num_train] + X_non_fail[:num_train]
    X_test = X_fail[num_train:] + X_non_fail[num_train:]
    Y_train = Y_fail[:num_train] + Y_non_fail[:num_train]
    Y_test = Y_fail[num_train:] + Y_non_fail[num_train:]

else:
    X_train = X[:NUM_TRAIN_ROWS]
    X_test = X[NUM_TRAIN_ROWS:]
    Y_train = Y[:NUM_TRAIN_ROWS]
    Y_test = Y[NUM_TRAIN_ROWS:]

print('Fitting classifier on training data')
start_time = time.time()

clf = tree.DecisionTreeClassifier()
clf.fit(X_train, Y_train)

end_time = time.time()
print('Time elapsed: ', end_time - start_time)

print('Predicting labels of test data')
preds = clf.predict(X_test)
baseline_preds = np.zeros(len(preds))

print('Calculating prediction error')
errors = np.mean(preds != Y_test)
print('Prediction error: ', errors)
baseline_errors = np.mean(baseline_preds != Y_test)
print('Baseline error (always predicting non-fail): ', baseline_errors)
