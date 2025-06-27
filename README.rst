
.. code-block:: text

   ____       _        _    ____ ___
  |  _ \ _ __(_)_   __/ \  |  _ \_ _|
  | |_) | '__| \ \ / / _ \ | |_) | |
  |  __/| |  | |\ V / ___ \|  __/| |
  |_|   |_|  |_| \_/_/   \_\_|  |___|


.. image:: https://img.shields.io/github/license/veridax/privapi
   :target: https://github.com/veridax/privapi/blob/master/LICENSE.txt
.. image:: https://img.shields.io/badge/Python-3.6%2B-blue?logo=python
   :target: https://www.python.org/
.. image:: https://img.shields.io/badge/tests-unittest-green
   :target: https://docs.python.org/3/library/unittest.html
.. image:: https://img.shields.io/badge/Read-Blog-informational
   :target: https://medium.com/@gbrigandi/privapi-detecting-personal-data-within-api-communication-using-deep-learning-9e52a1ff09c6

Overview
--------

**PrivAPI** is a Python package that uses Deep Neural Networks (DNN) to classify and detect personally identifiable information (PII) within REST API payloads. Built with Keras and TensorFlow, it enables automated privacy risk detection in software systems.

Quickstart
----------

Requirements
^^^^^^^^^^^^

* Python 3.5+

Setup Environment
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python3 -m venv venv
   export PYTHONPATH=.
   source venv/bin/activate

Install Dependencies
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install -r requirements.txt

Train Your Model
^^^^^^^^^^^^^^^^

.. code-block:: bash

   python privapi/train.py

This generates the model and tokenizer in the ``out/`` folder.

.. note::

   Use a GPU for better performance. Training may take 100+ epochs.

Detect Sensitive Data Flows
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python privapi/predict.py

Sample Output (predictions.csv):

+----+----------------------+----------------+--------------+
| ID | Payload File         | Is Sensitive   | Probability  |
+====+======================+================+==============+
| 0  | magento-payload.json | 1              | 0.99997      |
+----+----------------------+----------------+--------------+
| 1  | slack-payload.json   | 0              | 0.40711      |
+----+----------------------+----------------+--------------+

Drop ``.json`` payloads into the ``predict/`` folder and re-run the script.

Generate a Dataset
------------------

.. code-block:: bash

   python privapi/generate.py

Default path: ``data/training.csv``

Get insights on dataset quality:

.. code-block:: bash

   python privapi/analyze.py

Configuration and Labeling
--------------------------

The labeling logic lives in ``config.py``. It defines regex patterns that map field names to generators.

Example snippet:

.. code-block:: python

   name_type_to_gen = {
       'string': {
           '[lL]ocation': _location_,
           '[tT]imestamp': _timestamp_str_,
           ...
       },
       'number': {
           '[aA]mount': _amount_str_,
           '[cC]reditScore': _credit_score_str_,
           ...
       }
   }

Default domain exclusions:

.. code-block:: python

   exclusions = [".*amazonaws.com"]

Run Tests
---------

.. code-block:: bash

   python -m unittest

Contributing
------------

We welcome your contributions! Please read our `CONTRIBUTING <https://github.com/veridax/privapi/blob/master/CONTRIBUTING.rst>`_ guidelines.

License
-------

PrivAPI is licensed under the Apache 2.0 License. See the full license `here <https://github.com/veridax/privapi/blob/master/LICENSE.txt>`_.

Learn More
----------

* `PrivAPI Blog on Medium <https://medium.com/@gbrigandi/privapi-detecting-personal-data-within-api-communication-using-deep-learning-9e52a1ff09c6>`_

.. note::

   “Code responsibly. Privacy is not a feature, it’s a foundation.”
