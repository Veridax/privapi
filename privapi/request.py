from pyswagger import App
from pyswagger.primitives import Renderer
from pyswagger.scan import Scanner, Dispatcher
from pyswagger.spec.v2_0.objects import Operation
from xeger import Xeger
import json
import os
import pathlib as pathlib
import random
import re
import uuid
from config import *
from privapi.fakers import _email_, _text_
from .utils import PrivapiEncoder

class FakeRequestRenderer(Renderer):
    pii_classified = set()

    def __init__(self):
        super(FakeRequestRenderer, self).__init__()

        self._default_opts = dict(
            max_name_length=64,
            max_prop_count=32,
            max_str_length=50,
            max_byte_length=50,
            max_array_length=10,
            max_file_length=100,
            minimal_property=False,
            minimal_parameter=False,
            files=[],
            object_template={},
            parameter_template={},
            max_property=False,
            max_parameter=False,
        )

        self._map['string']['email'] = _email_
        self._map['string'][''] = _text_
        self._map['string'][None] = _text_

    def _generate(self, obj, opt):
        name_ = getattr(obj, 'name', None)
        type_ = getattr(obj, 'type', None)
        if name_ is not None:
            g = self._getgen(name_, type_)
            if g:
                out = None
                out = g(obj, opt, out)
                self.pii_classified.add(name_)
                return out
            dg = self._get(getattr(obj, 'type', None), getattr(obj, 'format', None))
            if dg:
                return super(FakeRequestRenderer, self)._generate(obj, self._default_opts)


    def _getgen(self, _name, _type, _format=None):
        r = name_type_to_gen.get(_type, None)
        if r is not None:
            gen = None
            for regex in r.keys():
                if re.match(regex, _name):
                    gen = r.get(regex)
                    break

            return gen


class FakeRequestGenerator(object):
    """ a scanner to generate fake requests given an operation
    """

    class Disp(Dispatcher):
        pass

    def __init__(self, folder, reqhandler):
        self.folder = folder
        self.renderer = FakeRequestRenderer()
        self.reqhandler = reqhandler


    def _apis_to_requests(self):
        for dirpath, dirs, files in os.walk(self.folder):
            descriptors = [fi for fi in files if 'swagger.yaml' or 'swagger.json' in fi]
            for desc in descriptors:
                fname = os.path.join(dirpath, desc)
                for ex in exclusions:
                    if re.match(ex, fname) is None:
                        print(('Generating {:s}...').format(fname))
                        try:
                            self._api_to_requests(fname)
                            print(('Generated {:s}.').format(fname))
                        except Exception as e:
                            pass

    def _api_to_requests(self, fname):
        self.app = App.create(fname)
        s = Scanner(self.app)
        s.scan(route=[self], root=self.app.raw)

    @Disp.register([Operation])
    def _operation(self, path, obj, _):
        op = obj
        fr = self.renderer.render_all(op)
        is_pii = len(self.renderer.pii_classified) > 0

        json_req = json.dumps(fr, cls=PrivapiEncoder)
        json_req_obj = json.loads(json_req)
        json_req_obj = {k: v for k, v in json_req_obj.items() if k if v}
        if not bool(json_req_obj):
            return

        x = Xeger(limit=10)
        r = name_type_to_gen.get("string", None)
        self.reqhandler(json.dumps(json_req_obj, cls=PrivapiEncoder), is_pii)
        if is_pii and r:
            for i in range(2):
                for regex in random.sample(r.keys(), round(len(r.keys()) * .1)):
                    rv = None
                    g = r.get(regex)
                    rn = x.xeger(regex)
                    rv = g(obj, [], rv)
                    n_fr = self.renderer.render_all(op)
                    n_json_req = json.dumps(n_fr, cls=PrivapiEncoder)
                    n_json_req_obj = json.loads(n_json_req)
                    n_json_req_obj[rn] = rv
                    self.reqhandler(json.dumps(n_json_req_obj, cls=PrivapiEncoder), is_pii)
        self.renderer.pii_classified.clear()

def print_request(targetdir, request):
    print(request)

def save_request(targetdir, request, has_pii):
    filename = "%s/%s.json" % (targetdir, str(uuid.uuid4()))
    pathlib.Path(targetdir).mkdir(parents=True, exist_ok=True)
    with open(filename, 'w') as f:
        f.write("%s\n" % request)

def save_request_to_csv(csvfile, request, has_pii):
        row = [request, '1' if has_pii else '0']
        csvfile.writerow(row)



