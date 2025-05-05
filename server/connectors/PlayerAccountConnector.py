


from server.player.Account import Account
from server.player.Player import Player


class Connector:

    def __init__(self, player: Player, account: Account):
        self.player = player
        self.account = account
    
    def get_player(self):
        return self.player
    
    def get_account(self):
        return self.account