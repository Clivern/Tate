# 035. pickle
#
# pickle serializes Python objects to bytes. Never unpickle untrusted data.
#
# Run: python 035_pickle_mod/main.py

import pickle

obj = {"n": 3, "xs": [1, 2]}
blob = pickle.dumps(obj)
print(pickle.loads(blob))
