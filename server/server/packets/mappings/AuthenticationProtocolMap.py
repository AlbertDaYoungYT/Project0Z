

from . import PacketProtocolMap


class AuthenticationProtocolMap(PacketProtocolMap): # FIXME
    

    def __init__(self):
        super().__init__()
        self.protocol_map = {}