# load data for day. grab serial number of each row.
# load data for the next day , and just keep serial number and failed columns

# Add failed_next_day column to first day data

# classify failed_next_day as 0 or 1 based on first day attributes

import csv
import pdb

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

def fails_next_day(serial_no):
    return next_day_failures[serial_no]

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

# january
# for day in range(1,31)
curr_day_filename = '../hd-data/2017-01-01.csv'
next_day_filename = '../hd-data/2017-01-02.csv'
output_filename = '../hd-data/2017-01-01fn.csv' # day 1 with fails next day appended

next_day_failures = failures_for_file(next_day_filename)

write_curr_day_with_failures(next_day_failures, curr_day_filename, output_filename)
