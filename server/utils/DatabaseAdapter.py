
from dataclasses import dataclass, fields, is_dataclass
from datetime import date, datetime, timedelta
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from cryptography.x509 import Certificate, load_pem_x509_certificate

import hashlib
import json, base64
from typing import Any, Dict, Type, TypeVar, Union
from uuid import UUID

# Define a type variable for Dataclasses, bounded to the base class.
_T = TypeVar('_T', bound=dataclass)


class Serializable:
    """
    A mixin class that adds JSON export functionality to dataclasses.

    When used as a base class for a dataclass, it provides a `to_json()` method
    that converts the dataclass instance into a JSON string.  It handles nested
    dataclasses, lists, and dictionaries.  It also provides a `from_json()`
    method to reconstruct a dataclass instance from a JSON string.

    Example Usage:

    @dataclasses.dataclass
    class Point(Serializable):
        x: int
        y: int

    @dataclasses.dataclass
    class MyData(Serializable):
        name: str
        count: int
        points: List[Point]
        mapping: Dict[str, Point]
        value: Union[int, float, None]

    data = MyData(
        name="Example",
        count=10,
        points=[Point(x=1, y=2), Point(x=3, y=4)],
        mapping={"a": Point(x=5, y=6), "b": Point(x=7, y=8)},
        value=3.14
    )

    json_string = data.to_json()
    print(json_string)

    loaded_data = MyData.from_json(json_string)
    print(loaded_data)
    """
    
    @classmethod
    def __set__(cls, **kwargs):
        for k,v in kwargs.items():
            cls.__setattr__(k,v)
        
        return cls

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the dataclass instance to a dictionary, handling nested dataclasses,
        lists, and dictionaries.

        Returns:
            dict: A dictionary representation of the dataclass.
        """
        def _convert_value(value: Any) -> Any:
            if is_dataclass(value):
                return value.to_dict()
            elif isinstance(value, list):
                return [_convert_value(item) for item in value]
            elif isinstance(value, dict):
                return {k: _convert_value(v) for k, v in value.items()}
            elif isinstance(value, UUID):
                return value.hex
            elif isinstance(value, rsa.RSAPrivateKey):
                return "BASE64::PRIVATE_KEY::"+base64.b64encode(value.private_bytes(
                    Encoding.PEM,
                    PrivateFormat.TraditionalOpenSSL,
                    NoEncryption() # TODO: Please figure something else out than this
                )).decode()
            elif isinstance(value, rsa.RSAPublicKey):
                return "BASE64::PUBLIC_KEY::"+base64.b64encode(value.public_bytes(
                    Encoding.PEM,
                    PublicFormat.SubjectPublicKeyInfo
                )).decode()
            elif isinstance(value, Certificate):
                return "BASE64::CERTIFICATE::"+base64.b64encode(value.public_bytes(
                            Encoding.PEM
                        )).decode()
            else:
                return None

        return {field.name: _convert_value(getattr(self, field.name))
                for field in fields(self)}

    def to_json(self, indent: int = 2) -> str:
        """
        Converts the dataclass instance to a JSON string.

        Args:
            indent (int, optional): The indentation level for the JSON output. Defaults to 2.

        Returns:
            str: A JSON string representation of the dataclass.
        """
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls: Type[_T], data: Dict[str, Any]) -> _T:
        """
        Reconstructs a dataclass instance from a dictionary.  Handles nested
        dataclasses, lists, and dictionaries.  This is a class method.

        Args:
            data (dict): A dictionary representation of the dataclass.

        Returns:
            _T: An instance of the dataclass.
        """
        if not is_dataclass(cls):
            raise TypeError(f"from_dict can only be called on dataclass types, not {cls}")

        def _convert_value(field_type: Type, value: Any) -> Any:
            if is_dataclass(field_type):
                #  Check for None
                if value is None:
                    return None
                return field_type.from_dict(value)
            elif hasattr(field_type, '__origin__') and field_type.__origin__ is list:
                if value is None:
                  return []
                (inner_type,) = field_type.__args__
                return [_convert_value(inner_type, item) for item in value]
            elif hasattr(field_type, '__origin__') and field_type.__origin__ is dict:
                if value is None:
                    return {}
                key_type, value_type = field_type.__args__
                return {k: _convert_value(value_type, v) for k, v in value.items()}
            elif hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
                # Handle Optional[Dataclass]
                if value is None:
                    return None
                # Iterate through the types in the Union
                for arg in field_type.__args__:
                    if is_dataclass(arg):
                         return arg.from_dict(value)
                    elif arg is type(None) and value is None:
                         return None
                return value
            elif isinstance(value, str) and value.startswith("BASE64::PRIVATE_KEY::"):
                private_key_bytes: bytes = base64.b64decode(
                    value[len("BASE64::PRIVATE_KEY::"):]
                    .encode()
                )
                private_key: rsa.RSAPrivateKey = serialization.load_pem_private_key(
                    private_key_bytes,
                    backend=default_backend()
                )
                return private_key
            elif isinstance(value, str) and value.startswith("BASE64::PUBLIC_KEY::"):
                public_key_bytes: bytes = base64.b64decode(
                    value[len("BASE64::PUBLIC_KEY::"):]
                    .encode()
                )
                public_key: rsa.RSAPublicKey = serialization.load_pem_public_key(
                    public_key_bytes,
                    backend=default_backend()
                )
                return public_key
            elif isinstance(value, str) and value.startswith("BASE64::CERTIFICATE::"):
                certificate_bytes: bytes = base64.b64decode(
                    value[len("BASE64::CERTIFICATE::"):]
                    .encode()
                )
                certificate: Certificate = load_pem_x509_certificate(
                    public_key_bytes
                )
                return certificate
            else:
                return None

        field_types = {field.name: field.type for field in fields(cls)}
        # Handle the case where a field is missing in the JSON data.
        kwargs = {
            name: _convert_value(field_types[name], data.get(name))
            for name in field_types
        }
        return cls(**kwargs)

    @classmethod
    def from_json(cls: Type[_T], json_str: str) -> _T:
        """
        Reconstructs a dataclass instance from a JSON string. This is a class method.

        Args:
            json_str (str): A JSON string representation of the dataclass.

        Returns:
            _T: An instance of the dataclass.
        """
        data = json.loads(json_str)
        return cls.from_dict(data)