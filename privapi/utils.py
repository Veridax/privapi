from __future__ import absolute_import

import datetime
import json
import os
from uuid import UUID


class PrivapiEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def get_test_data_folder(schemaroot='schema', which=''):
    """
    """
    import privapi.tests.data

    folder = os.path.dirname(os.path.abspath(privapi.tests.data.__file__))
    folder = os.path.join(os.path.join(folder, schemaroot), which)
    return folder
