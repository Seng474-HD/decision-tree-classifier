import csv
import pdb
import os

INPUT_DIR = '../hd-data/output'
OUTPUT_DIR = '../hd-data/output/months'

def write_header(input_filepath, output_filepath): # write header from input_file to output_file
    with open(input_filepath, 'r') as input_file:
        with open(output_filepath, 'w') as output_file: # open output file for overwriting
            datareader = csv.DictReader(input_file, delimiter=',', quotechar='|')
            output_fieldnames = datareader.fieldnames
            datawriter = csv.DictWriter(output_file, output_fieldnames, delimiter=',', quotechar='|')
            datawriter.writeheader()


def append_rows_to_output_file(input_filepath, output_filepath):
    with open(input_filepath, 'r') as input_file:
        with open(output_filepath, 'a') as output_file: # open output file for appending
            datareader = csv.DictReader(input_file, delimiter=',', quotechar='|')
            datawriter = csv.DictWriter(output_file, datareader.fieldnames, delimiter=',', quotechar='|')

            for row in datareader:
                datawriter.writerow(row)


# january
jan_output_filepath = os.path.join(OUTPUT_DIR, 'jan.csv')

write_header(os.path.join(INPUT_DIR, '2017-01-01fn.csv'), jan_output_filepath)

for day in range(1,32):
    day = '0' + str(day) if day < 10 else str(day) # e.g. 01, 02, ... 10, 11
    input_filename = '2017-01-' + day + 'fn.csv'
    input_filepath = os.path.join(INPUT_DIR, input_filename)
    print('writing ' + input_filename)
    append_rows_to_output_file(input_filepath, jan_output_filepath)
