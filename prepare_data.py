# load data for day. grab serial number of each row.
# load data for the next day , and just keep serial number and failed columns

# Add failed_next_day column to first day data

# classify failed_next_day as 0 or 1 based on first day attributes

import csv
import pdb
import os

DATA_DIR = '../hd-data'
OUTPUT_DIR = '../hd-data/output'


def failures_for_file(filename):
    failures = {}
    with open(filename, 'r') as csvfile:
        datareader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        # header = datareader.__next__()
        for row in datareader:
            serial_number = row['serial_number']
            failure_status = row['failure']
            failures[serial_number] = failure_status
    return failures


def write_curr_day_with_failures(failures_dict={}, curr_day_filename='', output_filename=''):
    with open(curr_day_filename, 'r') as curr_day_csv_file: # open current day file
        with open(output_filename, 'w') as outfile: # open output file
            datareader = csv.DictReader(curr_day_csv_file, delimiter=',', quotechar='|')

            output_fieldnames = datareader.fieldnames
            output_fieldnames.append('fails_next_day')

            datawriter = csv.DictWriter(outfile, output_fieldnames, delimiter=',', quotechar='|')

            datawriter.writeheader()
            for row in datareader:
                serial_number = row['serial_number']
                if serial_number in next_day_failures:
                    fails_next_day = next_day_failures[serial_number]
                    row['fails_next_day'] = fails_next_day
                    datawriter.writerow(row)


input_files = list(filter(lambda x:  os.path.splitext(x)[1] == '.csv', os.listdir(DATA_DIR)))
input_files.sort()

for i in range(len(input_files) - 1):
    curr_day_filename = input_files[i]
    curr_day_filename_base = os.path.splitext(curr_day_filename)[0]
    next_day_filename = input_files[i + 1]

    curr_day_filepath = os.path.join(DATA_DIR, curr_day_filename)
    next_day_filepath = os.path.join(DATA_DIR, next_day_filename)

    output_filepath = os.path.join(OUTPUT_DIR, curr_day_filename_base + 'fn.csv')

    print('writing next day failures from ' + curr_day_filename + ' to ' + output_filepath)
    next_day_failures = failures_for_file(next_day_filepath)
    write_curr_day_with_failures(next_day_failures, curr_day_filepath, output_filepath)
