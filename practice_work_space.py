class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.text = f"{rank} of {suit}"

    def __contains__(self, card):
        print('hello')


class Game:
    def __init__(self):
        self.hand = [1,2,3,4,5]
        self.players = []

    
class Team:
    def __init__(self):
        self.score = 0
    

class Player:
    def __init__(self,name):
        super().__init__()
        self.hand = []
        self.name = name
        self.dealer = False

    def __repr__(self):
        return self.name

    
Euchre = Game()

p1 = Player("Eric")
p2 = Player("Joe")
p3 = Player("Billy")
p4 = Player("Schmo")

Euchre.players = [p1,p2,p3,p4]

print( Euchre.players[2].Team.score ) 

