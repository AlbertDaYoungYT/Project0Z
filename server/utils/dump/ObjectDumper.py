


import base64
import pickle
from utils.DatabaseAdapter import Serializable


def dump_non_serializable_object(obj: object) -> bytes:
    if isinstance(Serializable):
        raise TypeError("Unable to Dump Serializable Object as Non Serializable Class")
    
    dump = pickle.dumps(obj)
    dump = base64.urlsafe_b64encode(dump)
    return dump

def dump_serializable_object(obj: Serializable) -> bytes:
    obj = obj.to_json(indent=0)

    dump = pickle.dumps(obj)
    dump = base64.urlsafe_b64encode(dump)
    return dump