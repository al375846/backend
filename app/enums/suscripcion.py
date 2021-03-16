from enum import Enum

class TipoSuscripcion(str, Enum):
    edu = "EDU"
    host = "HOST"
    enterprise = "ENTERPRISE"
    custom = "CUSTOM"