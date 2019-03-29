from __future__ import absolute_import

import datetime
import json
import unittest
import uuid
from os import path

import six
from pyswagger import App
from validate_email import validate_email

from config import *
from privapi.request import FakeRequestRenderer
from privapi.utils import PrivapiEncoder, get_test_data_folder


class PayloadGenerationTestCase(unittest.TestCase):
    """ test case for JSON payload traffic generator """
    @classmethod
    def setUpClass(kls):
        kls.app = App.create(get_test_data_folder(
            which=path.join('operation')
        ))
        kls.rnd = FakeRequestRenderer()

    def test_set_1(self):
        """ test query, header, path parameter """
        op = self.app.s("api.1/{path_email}").get
        ps = self.rnd.render_all(op)
        # checking generated parameter set
        self.assertTrue(isinstance(ps, dict), 'should be a dict, not {0}'.format(ps))
        self.assertTrue("path_email" in ps, 'path_email should be in set, but {0}'.format(ps))
        self.assertTrue(isinstance(ps['path_email'], six.string_types), 'should be string, not {0}'.format(str(type(ps['path_email']))))
        self.assertTrue(validate_email(ps['path_email']), 'should be a valid email, not {0}'.format(ps['path_email']))
        self.assertTrue(isinstance(ps['path_timestamp'], datetime.datetime), 'should be a valid timestamp, not {0}'.format(str(type(ps['path_timestamp']))))
        self.assertTrue("header.uuid" in ps, 'header.uuid should be in set, but {0}'.format(ps))
        self.assertTrue(isinstance(ps['header.uuid'], uuid.UUID), 'should be an uuid.UUID, not {0}'.format(str(type(ps['header.uuid']))))
        self.assertTrue("query.integer" in ps, 'query.integer should be in set, but {0}'.format(ps))
        self.assertTrue(isinstance(ps['query.integer'], six.integer_types), 'should be int, not {0}'.format(str(type(ps['query.integer']))))

        # ok to be passed into Operation object
        req, resp = op(**ps)
        req.prepare(scheme='http', handle_files=False)

        # query
        found_query = False
        for v in req.query:
            if v[0] == 'query.integer':
                found_query = True
                break
        self.assertEqual(found_query, True)

        # header
        found_header = False
        for k, v in six.iteritems(req.header):
            if k == 'header.uuid':
                found_header = True
                break
        self.assertEqual(found_header, True)

        # path
        self.assertTrue(validate_email(six.moves.urllib.parse.unquote_plus(req.path[len('/api.1/'):])), 'should contain a valid email, not {0}'.format(req.path))

    def test_set_2(self):
        op = self.app.s("api.1/{path_email}").get
        ps = self.rnd.render_all(op)
        j = json.dumps(ps, cls=PrivapiEncoder)
        json.loads(j)

    def test_string_fakers(self):
        r = name_type_to_gen.get("string", None)
        if r is not None:
            for gen in r.values():
                fs = gen(obj=None, opt=[])
                self.assertTrue(isinstance(fs, six.string_types), 'string faker {0} generated {1} which should be string, not {2}'.format(str(gen), fs, str(type(fs))))

    def test_number_fakers(self):
        r = name_type_to_gen.get("number", None)
        if r is not None:
            for gen in r.values():
                fs = gen(obj=None, opt=[])
                self.assertTrue(isinstance(fs, six.string_types), 'number faker {0} generated {1} which should be string, not {2}'.format(str(gen), fs, str(type(fs))))

    def test_generation_from_config(self):
        class NV:
            name = 'firstname'
            type = 'string'

        obj = NV()
        firstname = self.rnd._generate(obj, opt=[])
        self.assertTrue(isinstance(firstname, six.string_types), 'should be string, not {0}'.format(str(type(firstname))))

