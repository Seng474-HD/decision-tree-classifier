# load data for day. grab serial number of each row.
# load data for the next day , and just keep serial number and failed columns

# Add failed_next_day column to first day data

# classify failed_next_day as 0 or 1 based on first day attributes


import csv
import pdb

failure_col = 4
serial_col = 1

# january
# for day in range(1,31)
day1file = 'data/2017-01-01.csv'
day2file = 'data/2017-01-02.csv'
outputfile = 'data/2017-01-01fn.csv' # day 1 with fails next day appended

def failures_for_day(filename):
    failures = {}
    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader:
            serial_num = row[serial_col]
            failure_status = row[failure_col]
            failures[serial_num] = failure_status
    return failures


day2failures = failures_for_day(day2file)

with open(day1file, 'r') as csvfile:
    with open(outputfile, 'w+') as outfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        datawriter = csv.writer(outfile, delimiter=',', quotechar='|')
        pdb.set_trace()


pdb.set_trace()

# with open(outputfile, 'w') as csvfile:
