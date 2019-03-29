import csv
import optparse
import os
import pathlib
from functools import partial

from privapi.request import FakeRequestGenerator, save_request_to_csv


def generate(apis, training_csv):
    pathlib.Path(training_csv).parent.mkdir(parents=True, exist_ok=True)
    csvfile = open(training_csv, 'w')
    csvwriter = csv.writer(csvfile, quotechar='|')
    frg = FakeRequestGenerator(apis, partial(save_request_to_csv, csvwriter))
    #frg = FakeRequestGenerator('%s/APIs/circuitsandbox.net/2.9.119' % basedir, partial(save_request_to_csv, csvwriter))
    #frg = FakeRequestGenerator('%s/APIs/swagger_test/v2_0/render/operation' % basedir, partial(save_request_to_csv, csvwriter))
    frg._apis_to_requests()
    csvfile.close()

if __name__ == '__main__':
    basedir = os.path.join(os.path.dirname(__file__), os.pardir)
    parser = optparse.OptionParser()
    parser.add_option('-a', '--apis', action="store", dest="apis", help="folder for source OpenAPI descriptors")
    parser.add_option('-t', '--training', action="store", dest="training", help="output training CSV file")
    options, args = parser.parse_args()

    if options.apis is not None:
        apis = options.apis
    else:
        apis = '%s/APIs' % basedir

    if options.training is not None:
        training_csv = options.training
    else:
        training_csv = '%s/data/training.csv' % basedir

    generate(apis, training_csv)