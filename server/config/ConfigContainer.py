from dataclasses import *
import inspect
import json

from utils.File import File

@dataclass
class ConfigContainer:

    collection: str = "projectz0"
    connectionUri: str = "http://192.168.1.2:15984/"

    couchdb_user: str = "projectz0"
    couchdb_pass: str = "1Cr3x8X5TKIPTdrp7xZd"

    redis_host: str = "192.168.1.2"
    redis_port: int = 30059
    redis_user: str = "root"
    redis_pass: str = "1Cr3x8X5TKIPTdrp7xZd"

    dispatchKey: str = ""




    def __json__(self):
        return {key: getattr(self, key) for key in inspect.getfullargspec(self.__init__).args if key != 'self'}

    def __decode__(self, dct):
        cls_attributes = inspect.getfullargspec(ConfigContainer.__init__).args
        if all(key in dct for key in cls_attributes if key != 'self'):
            return ConfigContainer(**dct)
        return dct
    
    def __load__(self, file: File):
        self = json.loads(file.read(), object_hook=self.__decode__)
    
    def __save__(self, file: File):
        return file.write(json.dumps(self, default=lambda o: o.__json__() if hasattr(o, '__json__') else None))

    

