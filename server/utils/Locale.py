


from dataclasses import dataclass
from utils.DatabaseAdapter import Serializable

@dataclass
class Locale(Serializable):
    ENGLISH = 0
    FRENCH = 1
    GERMAN = 2
    ITALIAN = 3
    JAPANESE = 4
    KOREAN = 5
    CHINESE = 6
    SIMPLIFIED_CHINESE = 7
    TRADITIONAL_CHINESE = 8
    FRANCE = 9
    GERMANY = 10
    ITALY = 11
    JAPAN = 12
    KOREA = 13
    UK = 14
    US = 15
    CANADA = 16
    CANADA_FRENCH = 17