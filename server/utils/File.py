

from dataclasses import dataclass


@dataclass
class File:

    filename: str = ""
    data: object = ""


    def write(self, *data):
        if len(data) > 0:
            self.data = data[0]

        if isinstance(self.data, str):
            open(self.filename, "w", encoding="utf-8").write(self.data)

        if isinstance(self.data, bytes):
            open(self.filename, "wb", encoding="utf-8").write(self.data)
    

    def read(self, rb=False):
        readMode = "r"
        if rb: readMode = "rb"

        return open(self.filename, readMode, encoding="utf-8").read()