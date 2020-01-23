import pickle
import re

from keras.models import load_model
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from collections import OrderedDict
import sys
import os
import json
import pandas as pd
import numpy as np
import optparse

def predict(input_dir, requests_dir, predictions_csv):
    print("Loading Model...")
    with open(('%s/build/tokenizer.pkl' % input_dir), 'rb') as handle:
        tokenizer = pickle.load(handle)
    model = load_model('%s/privapi-lstm-model.h5' % input_dir)
    model.load_weights('%s/privapi-lstm-weights.h5' % input_dir)
    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    print("Model Loaded.")
    print("Generating predictions...")
    result_dict = []
    for dirpath, dirs, files in os.walk(requests_dir):
        reqs = [fi for fi in files if fi.endswith(".json")]
        for req in reqs:
            reqf = os.path.join(dirpath, req)
            with open(reqf) as f:
                reqd = json.load(f, object_pairs_hook=OrderedDict)
                reqj = json.dumps(reqd, separators=(',', ':'))
                reqs = tokenizer.texts_to_sequences([reqj])
                max_log_length = 1024
                reqsp = sequence.pad_sequences(reqs, maxlen=max_log_length)
                prediction = model.predict(reqsp)
                prediction_class = model.predict_classes(reqsp)
                result_dict.append([os.path.basename(reqf), prediction_class[0][0], prediction[0][0]])

    result_array = np.array(result_dict)
    df = pd.DataFrame(result_array)
    df.columns = ['payload_file', 'is_sensitive', 'probability']
    df.to_csv(predictions_csv, index=False)
    print("Predictions Generated.")

if __name__ == '__main__':
    from tensorflow.python.util import deprecation
    deprecation._PRINT_DEPRECATION_WARNINGS = False

    basedir = os.path.join(os.path.dirname(__file__), os.pardir)
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', action="store", dest="input", help="folder with model and dictionary")
    parser.add_option('-r', '--requests', action="store", dest="requests", help="folder with JSON request files")
    parser.add_option('-o', '--predictions', action="store", dest="predictions", help="output CSV file")
    options, args = parser.parse_args()

    if options.input is not None:
        input_dir = options.input
    else:
        input_dir = '%s/out' % basedir

    if options.requests is not None:
        request_dir = options.requests
    else:
        request_dir = '%s/predict' % basedir

    if options.predictions is not None:
        predictions_csv = options.predictions
    else:
        predictions_csv = '%s/predictions.csv' % basedir

    predict(input_dir, request_dir, predictions_csv)
