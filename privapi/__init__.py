from faker import Faker
from faker_credit_score import CreditScore

__version__ = '0.0.1'

_fake = Faker()
_fake.add_provider(CreditScore)
