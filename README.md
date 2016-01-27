# JSONtoCOOL

What is this?
-------------
Basic python based script to generate a (local) COOL database from a neural net stored in a JSON file using the same conventions as required by Dan's lightweight neural network client which is then to be used in a local test run using the flavour tagging performance framework.


How do I use it?
----------------
Set up Athena using https://github.com/Marie89/ATHENA-retagging-setup/blob/master/setup_TestArea.sh

Run the converter. Example:
`python JSONtoCOOL_converter.py "AGILEPack_December_1D_btagging.json" "BTagCalibRUN2-08-14_new.root"`

Adapt the job options.
