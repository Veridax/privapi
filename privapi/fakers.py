import random
import string
from uuid import UUID
from . import _fake

def _date_(obj, opt, val=None):
    if val:
        return val
    return _fake.date()

def _full_name_(obj, opt, val=None):
    if val:
        return val
    return _fake.name()

def _first_name_(obj, opt, val=None):
    if val:
        return val
    return _fake.first_name()

def _last_name_(obj, opt, val=None):
    if val:
        return val
    return _fake.last_name()

def _nationality_(obj, opt, val=None):
    if val:
        return val
    return _fake.country()

def _address_(obj, opt, val=None):
    if val:
        return val
    return _fake.address()

def _postal_code_(obj, opt, val=None):
    if val:
        return val
    return _fake.postcode()

def _state_(obj, opt, val=None):
    if val:
        return val
    return _fake.state()

def _street_(obj, opt, val=None):
    if val:
        return val
    return _fake.secondary_address()

def _state_(obj, opt, val=None):
    if val:
        return val
    return _fake.state()

def _province_(obj, opt, val=None):
    if val:
        return val
    return _fake.state()

def _building_number_(obj, opt, val=None):
    if val:
        return val
    return _fake.building_number()

def _country_(obj, opt, val=None):
    if val:
        return val
    return _fake.country()

def _country_code_(obj, opt, val=None):
    if val:
        return val
    return _fake.country_code()

def _email_(obj, opt, val=None):
    if val:
        return val
    return _fake.email()

def _text_(obj, opt, val=None):
    if val:
        return val

    wds = _fake.words(nb=3)
    chars = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(8))
    digits = ''.join(random.choice(string.digits) for _ in range(8))
    chars_and_digits = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

    return ' '.join(random.sample(wds + [chars, digits, chars_and_digits], random.randint(1, 6)))

def _word_(obj, opt, val=None):
    if val:
        return val
    return _fake.word()

def _phone_number_(obj, opt, val=None):
    if val:
        return val
    return _fake.phone_number()

def _country_code_(obj, opt, val=None):
    if val:
        return val
    return _fake.country_code()

def _gender_(obj, opt, val=None):
    if val:
        return val
    return random.choice(['M', 'F'])

def _id_(obj, opt, val=None):
    if val:
        return val
    return _fake.sha1()

def _key_(obj, opt, val=None):
    if val:
        return val
    return _fake.uuid4()

def _uuid_(obj, opt, val=None):
    if val:
        return val
    return UUID(_fake.uuid4())

def _ssn_(obj, opt, val=None):
    if val:
        return val
    return _fake.ssn()

def _company_business_id_(obj, opt, val=None):
    if val:
        return val
    return _fake.company()

def _company_(obj, opt, val=None):
    if val:
        return val
    return _fake.company()

def _bank_account_(obj, opt, val=None):
    if val:
        return val
    return _fake.bban()

def _bban_(obj, opt, val=None):
    if val:
        return val
    return _fake.bban()

def _iban_(obj, opt, val=None):
    if val:
        return val
    return _fake.iban()

def _credit_card_provider_(obj, opt, val=None):
    if val:
        return val
    return _fake.credit_card_provider()

def _credit_card_number_(obj, opt, val=None):
    if val:
        return val
    return _fake.credit_card_number()

def _credit_card_expire_(obj, opt, val=None):
    if val:
        return val
    return _fake.credit_card_expire()

def _credit_card_full_(obj, opt, val=None):
    if val:
        return val
    return _fake.credit_card_full()

def _credit_card_security_code_(obj, opt, val=None):
    if val:
        return val
    return _fake.credit_card_security_code()

def _credit_card_type_(obj, opt, val=None):
    if val:
        return val
    return _fake._credit_card_type()

def _city_(obj, opt, val=None):
    if val:
        return val
    return _fake.city()

def _amount_(obj, opt, val=None):
    if val:
        return val
    return round(random.uniform(10, 100000), 2)

def _amount_str_(obj, opt, val=None):
    return str(_amount_(obj, opt, val))

def _alphanumeric_(obj, opt, val=None):
    if val:
        return val
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def _credit_score_str_(obj, opt, val=None):
    return str(_credit_score_(obj, opt, val))

def _credit_score_(obj, opt, val=None):
    if val:
        return val
    return _fake.credit_score()

def _location_(obj, opt, val=None):
    if val:
        return val
    return str(_fake.coordinate())

def _latitude_str_(obj, opt, val=None):
    return str(_latitude_(obj, opt, val))

def _longitude_str_(obj, opt, val=None):
    return str(_longitude_(obj, opt, val))

def _latitude_(obj, opt, val=None):
    if val:
        return val
    return _fake.latitude()

def _longitude_(obj, opt, val=None):
    if val:
        return val
    return _fake.longitude()

def _timestamp_str_(obj, opt, val=None):
    return str(_timestamp_(obj, opt, val))

def _timestamp_(obj, opt, val=None):
    if val:
        return val
    return _fake.unix_time()



