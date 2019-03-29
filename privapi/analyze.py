import csv
import json
import sys
import os
import pandas
import optparse

def analyze(csv_file):
    csv.field_size_limit(sys.maxsize)
    dataframe = pandas.read_csv(csv_file, engine='python', quotechar='|', header=None)
    for index, row in dataframe.iterrows():
        try:
            json.loads(row[0])
        except ValueError as e:
            print('Invalid json: ', row[0])
            raise e

    count_frame = dataframe.groupby([1]).count()
    print(count_frame)
    total_req = count_frame[0][0] + count_frame[0][1]
    num_has_pii = count_frame[0][1]

    print("Request containing PII in dataset: {:0.2f}%".format(float(num_has_pii) / total_req * 100))

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action="store", dest="file", help="data file")
    options, args = parser.parse_args()

    if options.file is not None:
        csv_file = options.file
    else:
        basedir = os.path.join(os.path.dirname(__file__), os.pardir)
        csv_file = "%s/data/training.csv" % basedir
    analyze(csv_file)
