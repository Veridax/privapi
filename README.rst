*PrivAPI* is a Python package that allows classifying sensitive data flows within
REST API communication using Deep Neural Networks (DNN).
It relies on Google's Keras and TensorFlow.

As explained in `Detecting Sensitive Dataflows Using Deep Learning`_

----

::

   ____       _        _    ____ ___
  |  _ \ _ __(_)_   __/ \  |  _ \_ _|
  | |_) | '__| \ \ / / _ \ | |_) | |
  |  __/| |  | |\ V / ___ \|  __/| |
  |_|   |_|  |_| \_/_/   \_\_|  |___|


----

Quickstart
----------

Requirements
^^^^^^^^^^^^

Make sure you're running Python 3.5 or newer.

Setup environment
^^^^^^^^^^^^^^^^^

It's strongly recommended to build your own environment so that your local python
packages don't get in the way.
Create a Virtualenv environment within the ``venv`` project folder.

.. code:: bash

    python3 -m venv venv

Then set the PYTHONPATH and activate the environment so the Python scripts can be found:

.. code:: bash

    export PYTHONPATH=.
    source venv/bin/activate

Install dependencies
^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    pip install -r requirements.txt

Create a Neural Network Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In in order to detect sensitive data flows the system has to learn from confidential and non-confidential REST API request
payloads.
The project ships with a pre-generated dataset that can be used to train an LSTM neural network. If you want to generate your
please refer to the next section.

.. code:: bash

    python privapi/train.py

This will generate both the model and token directionary files living within the ``out`` folder.
It's strongly recommended to use a GPU box in ordr to speed up this process at the model requires 100 epochs to converge.

Detect sensitive dataflows
^^^^^^^^^^^^^^^^^^^^^^^^^^

Once a model has been trained, it's time to run predictions based on it.
There are two examples: one that is sensitive (positive class) and one that is not (negative class). Both live within the
``predict`` folder.

.. code:: bash

    python privapi/predict.py

This command will output predictions to the ``predictions.csv`` file within the project root.

.. csv-table::
   :header: "", "payload_file", "is_sensitive", "probability"
   :widths: 5, 30, 10, 10

    0,"magento-payload.json",1,0.9999695
    1,"slack-payload.json",0,0.40711942

As you can notice, Magento's sensitive request payload has been classified as confidential with a 99% confidence.
The non-confidential Slack request payload, even if it contained a first and last name, it was classified correctly.

Drop the request payloads you wish to classify onto the ``predict`` folder and re-run the ``predict.py`` script. Any file having
the ``.json`` extension will be picked up.

Enjoy!

Generate
--------

For generating your own your own training dataset use the following command :

.. code:: bash

    python privapi/generate.py

By default, the dataset will be saved as ``training.csv`` within the ``data`` folder.

In order to obtain relevant metrics of the generated dataset use :

.. code:: bash

    python privapi/analyze.py

Configuration
-------------

What will heavily determine the accuracy of the predictions is quality
of training dataset.
In addition to generate sound request payload examples, we need to make sure that
the associated label - whether sensitive or not - is correct.

In order to label an example, the generator will look in the ``config.py`` descriptor whether there's a matching entry for
a given OpenAPI operation parameter name matches the ``name_type_to_gen`` dictionary.
In case there is, it used the associated generator and label the example as positive (i.e. having PII).

Here's an example configuration file. Feel free to add your own custom entries in order to
consider additional PII fields.

.. code:: python

    from privapi.fakers import (
        _full_name_, _date_, _id_, _key_, _company_business_id_, _company_, _bank_account_, _first_name_, _last_name_,
        _address_, _bban_, _city_, _country_, _country_code_, _ssn_, _email_, _phone_number_, _gender_,
        _building_number_, _iban_, _postal_code_, _state_, _street_, _province_, _amount_, _credit_score_,
        _credit_card_number_, _alphanumeric_, _location_, _latitude_, _longitude_, _timestamp_, _latitude_str_,
        _longitude_str_, _timestamp_str_, _amount_str_, _credit_score_str_)

    name_type_to_gen = {'string':
                            {'[uU]ser': _full_name_,
                             '[fF]ullName': _full_name_,
                             'firstname': _first_name_,
                             'lastname': _last_name_,
                             '[aA]ddress': _address_,
                             '[nN]ationality': _country_,
                             '[dD]ate': _date_,
                             '[tT]axId': _company_business_id_,
                             '[sS]erial': _id_,
                             '[oO]rganization': _company_,
                             '[cC]ompany': _company_,
                             '[dD]ba': _company_,
                             '[dD]oingBusinessAs': _company_,
                             '[bB]usinessName': _company_,
                             '[aA]ccount': _bank_account_,
                             '[uU]UID': _id_,
                             '[sS]hareholder': _full_name_,
                             '[pP]ostalCode': _postal_code_,
                             '[zZ]ip': _postal_code_,
                             '[bB]ic': _bban_,
                             '[bB]ankCity': _city_,
                             '[bB]usinessContact': _full_name_,
                             '[cC]ity': _city_,
                             '[cC]ountryCode': _country_code_,
                             '[cC]country': _country_,
                             '[dD]ateOfBirth': _date_,
                             '[dD]ob': _date_,
                             '[dD]ocumentNumber': _ssn_,
                             '[pP]assport': _ssn_,
                             '[iI]dentityDocument': _ssn_,
                             '[iI]dNumber': _ssn_,
                             '[iI]dCard': _ssn_,
                             '[dD]rivingLicense': _ssn_,
                             '[cC]reditCard': _credit_card_number_,
                             '[eE]mail': _email_,
                             '[pP]hone': _phone_number_,
                             '[pP]honeCountryCode': _country_code_,
                             '[gG]ender': _gender_,
                             '[hH]ouse': _building_number_,
                             '[bB]uilding': _building_number_,
                             '[aA]partment': _building_number_,
                             '[aA]pt': _building_number_,
                             '[iI]ban': _iban_,
                             '[sS]tate': _state_,
                             '[pP]rovince': _province_,
                             '[sS]treet': _street_,
                             '[rR]ecordLocator': _alphanumeric_,
                             '[rR]eservationCode': _alphanumeric_,
                             '[lL]ocation': _location_,
                             '[lL]atitude': _latitude_str_,
                             '[lL]ongitude': _longitude_str_,
                             '[lL]at': _latitude_str_,
                             '[lL]on': _longitude_str_,
                             "[tT]imestamp": _timestamp_str_,
                             "[sS]ignature_sha1": _id_,

                             },
                        'number':
                            {
                                "[tT]imestamp": _timestamp_str_,
                                "[dD]ate": _timestamp_str_,
                                "[bB]alance": _amount_str_,
                                "[aA]mount": _amount_str_,
                                "[cC]redit": _amount_str_,
                                "[cC]reditScore": _credit_score_str_,
                                "[sS]core": _credit_score_str_,
                                "[lL]atitude": _latitude_str_,
                                "[lL]ongitude": _longitude_str_
                            }
                        }

    exclusions = [".*amazonaws.com"]


Tests
-----

Run tests:

.. code:: bash

    python -m unittest


Contribute
----------

Please see `CONTRIBUTING`_.

License
-------

PrivAPI is released under the Apache License. See the bundled `LICENSE`_ file for details.

Detecting-Sensitive-Dataflows-Using-Deep-Learning_

.. _Detecting Sensitive Dataflows Using Deep Learning: https://medium.com/gbrigandi/detecting-personal-data-within-api-communicatioin-using-deep-learning
.. _LICENSE: https://github.com/veridax/privapi/blob/master/LICENSE.txt
.. _CONTRIBUTING: https://github.com/veridax/privapi/blob/master/CONTRIBUTING.rst

