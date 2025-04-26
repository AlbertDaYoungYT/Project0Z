
from dataclasses import dataclass
import inspect

from utils.DatabaseAdapter import Serializable


class Modelable:
    
    @classmethod
    def __set__(cls, **kwargs):
        for k,v in kwargs.items():
            cls.__setattr__(k,v)
        
        return cls


@dataclass
class Model(Serializable):
    

    @classmethod
    def from_class(cls, other) -> Serializable:
        self_attributes = inspect.getmembers(cls, lambda a:not(inspect.isroutine(a)))
        other_attributes = inspect.getmembers(other, lambda a:not(inspect.isroutine(a)))

        list_of_self_attr = [a for a in self_attributes if not(a[0].startswith('__') and a[0].endswith('__'))]

        for k,v in [a for a in other_attributes if not(a[0].startswith('__') and a[0].endswith('__'))]:
            if (k, v) in list_of_self_attr:
                cls.__setattr__(k, v)
        
        return cls

    @classmethod
    def to_class(cls, clazz: Modelable) -> Modelable:
        self_attributes = dict(inspect.getmembers(cls, lambda a:not(inspect.isroutine(a))))
        return clazz.__set__(self_attributes)
    


