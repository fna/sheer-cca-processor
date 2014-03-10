sheer-cca-processor
===================

A custom processor for credit card agreements data in Sheer

This module will load CCA data from a zip archive. It will read the archive contents, find a ``csv`` file inside it
and index its contents.

To use it place the following code into ``_settings/custom_processors.json``:

``{
    "credit_cards_agreements": {
      "archive"   : "/path/to/archive/name.zip",
      "processor" : "cca_processor"
    }
  }``
