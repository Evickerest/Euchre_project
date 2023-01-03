#
# Made By Eric Moras in about two weeks
# Project is text-based Euchre. This version is able to do loners, farmer's hands, and screw the dealer.
# Future plan is to create AI players
# Version 1.0
# 

import random

CARD_VALUES = {
    "Jack Trump":19,
    "Jack Bower":18,
    "Ace Trump":17,
    "King Trump":16,
    "Queen Trump":15,
    "Ten Trump":14,
    "Nine Trump":13,
    "Ace Led":12,
    "King Led":11,
    "Queen Led":10,
    "Jack Led":9,
    "Ten Led":8,
    "Nine Led":7,
    "Ace":6,
    "King":5,
    "Queen":4,
    "Jack":3,
    "Ten":2,
    "Nine":1
}

BOWER_SUITS = {
    "Spades": "Clubs",
    "Clubs": "Spades",
    "Diamonds": "Hearts",
    "Hearts": "Diamonds"
}

# Score -- Attacker/Defender: Points won
SCORING = {
    "0 Attacker": 0,
    "1 Attacker": 0,
    "2 Attacker": 0,
    "3 Attacker": 1,
    "4 Attacker": 1,
    "5 Attacker": 2,

    "0 Defender": 0,
    "1 Defender": 0,
    "2 Defender": 0,
    "3 Defender": 2,
    "4 Defender": 2,
    "5 Defender": 4,

    "0 Attacker Alone": 0,
    "1 Attacker Alone": 0,
    "2 Attacker Alone": 0,
    "3 Attacker Alone": 1,
    "4 Attacker Alone": 1,
    "5 Attacker Alone": 4,

    "0 Defender Alone": 0,
    "1 Defender Alone": 0,
    "2 Defender Alone": 0,
    "3 Defender Alone": 2,
    "4 Defender Alone": 2,
    "5 Defender Alone": 4
}

NUM_OF_TRICKS = 5
STICK_THE_DEALER = False
FARMERS_HAND = False
GOING_ALONE = False

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.text = f"{rank} of {suit}"

    def __repr__(self):
        return self.text


class Game:
    def __init__(self):
        self.players = []
        self.cards = []
        self.trump = ""
        self.attacker = None
        self.defender = None

    def change_starting_order(self, starting_index):
        self.players = [ self.players[i % 4] for i in range( starting_index, starting_index+4) ]

    def change_dealer(self):
        # Get player that is dealer
        for player in self.players:
            if player.is_dealer: 
                dealer = player

        # Get dealer's index in self.players
        dealer_index = self.players.index( dealer )

        # Set new player players after old dealer
        self.change_starting_order( (dealer_index + 2) % 4 )

        # Change new dealer to dealer, and old dealer to not dealer
        self.players[3].is_dealer = True
        self.players[2].is_dealer = False

        print("Current dealer is:", self.players[3])
        
    def play_again(self):
        while True:
            answer = input("Do you want to play again? Y or N? ").lower()
            if answer == "y":
                self.reset()
                return True
            if answer == "n":
                return False
            print("Answer wasn't recoginzed.\n")

    def add_card(self, card):
        self.cards.append( card )

    def add_players(self, player):
        self.players.append( player )

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def deal_cards(self):
        index = 0
        for player in self.players:
            player.set_hand(self.cards[index:index+5])
            index += 5
        self.trump = self.cards[20].suit

    def set_as_attacker( self, player ):
        index = self.players.index( player )
        modulo_player = lambda x: self.players[ (index+x) % 4]

        self.attacker = [player, modulo_player(2)]
        self.defender = [modulo_player(1), modulo_player(3)]

    def reset( self ):
        self.trump = ""
        self.attacker = None
        self.defender = None
        for player in self.players:
            player.self_score = 0
            player.team_score = 0
            player.going_alone = False
            player.can_play = True

    def decide_trump(self):
        for player in self.players:
            trump_decided = player.decide_card_trump( self.cards )
            if trump_decided:
                self.set_as_attacker( player )
                self.players[3].discard_card_for_trump( self.cards[20] )
                return
          
        for player in self.players:
            new_trump = player.pick_trump( self.trump  )
            if new_trump != None: 
                self.set_as_attacker( player )
                self.trump = new_trump
                return

        print("\nAll players have passed, round is resetted.\n")
        return True

    def play_round(self):
        current_played_cards = []
        for player in self.players:
            if not player.can_play: 
                current_played_cards.append( None )
                continue
            player.play_card( current_played_cards, self.trump )
        return current_played_cards

    def determine_winner( self, played_cards ):
        led_suit = played_cards[0].suit
        card_values = [ self.change_card_to_value(card, led_suit) for card in played_cards ]
        max_index = card_values.index( max(card_values) )
        max_card = played_cards[ max_index ]
        winning_player = self.players[max_index]
        winning_player.self_score += 1
        
        print(f"Winning card is: {max_card} by {winning_player}\n")
        return max_index

    def change_card_to_value( self, card, led_suit):
        if card == None: return 0

        key_string = card.rank + ""
        if card.suit == self.trump and card.rank != "Jack": 
            key_string += " Trump"

        if card.rank == "Jack":
            if card.suit == self.trump:
                key_string += " Trump" 
            if card.suit == BOWER_SUITS[self.trump]:
                key_string += " Bower"
        
        if card.suit == led_suit and not key_string.endswith(("Trump","Bower")):
            key_string += " Led"

        return CARD_VALUES[ key_string ]

    def distribute_points( self ):
        attacker_string = " Attacker"
        defender_string = " Defender"
      
        # If a player went alone
        for player in self.attacker:
            if player.going_alone:  
                attacker_string += " Alone"
                defender_string += " Alone"
    
        attacker_score = self.attacker[0].self_score + self.attacker[1].self_score
        defender_score = self.defender[0].self_score + self.defender[1].self_score
        attacker_team_score = SCORING[ str(attacker_score)+attacker_string ]
        defender_team_score = SCORING[ str(defender_score)+defender_string ]
        self.attacker[0].team_score = self.attacker[1].team_score = attacker_team_score
        self.defender[0].team_score = self.defender[1].team_score = defender_team_score

        print(f"Attackers were {self.attacker}, who won {attacker_score} tricks, and won {attacker_team_score} points.")
        print(f"Defenders were {self.defender}, who won {defender_score} tricks, and won {defender_team_score} points.\n")
        print(f"Players {self.attacker} have {self.attacker[0].team_score} points and")
        print(f"Players {self.defender} have {self.defender[0].team_score} points.\n")
        
        if( attacker_team_score >= 10):
            return self.attacker
        if( defender_team_score >= 10):
            return self.defender

class Team:
    def __init__(self):
        self.trick_score = 0
        self.team_score = 0

class Player( Team ):
    def __init__(self, name):
        super().__init__()
        self.hand = []
        self.name = name
        # self.self_score = 0
        # self.team_score = 0
        self.is_dealer = False
        self.going_alone = False
        self.can_play = True
        self.teammate = None
        self.is_ai =  False
        
    def set_hand(self, hand):
        self.hand = hand

    def get_card( self ):
        while True:
            answer = input("What card would you like to select? ")
            print()
            for card in self.hand:
                if card.text == answer: return card
            print("Answer wasn't recognized")

    def is_card_left_bower( self, card, trump):
        return (card.rank == "Jack" and card.suit == BOWER_SUITS[ trump ])

    def get_legal_cards( self, played_cards, trump):
        # This get rids of index error
        if len(played_cards) == 0:
            return self.hand

        led_suit = played_cards[0].suit
        legal_cards = []

        # Go through hand and hand legal cards to legal_cards
        for card in self.hand:
            if self.is_card_left_bower( card, trump ):
                if led_suit == trump:
                    legal_cards.append( card )
            elif card.suit == led_suit: 
                legal_cards.append( card )
        
        # If there is no legal cards, then any card can be played
        if len(legal_cards) == 0:
            return self.hand
        return legal_cards
     
    def display_hand(self, msg, cards):
        # Magic to get the list of card objects to display as string
        # During going alone there will be an empty card, so ternary get rid of that
        text = " | ".join(list(map(lambda x: "" if x == None else x.text, cards)))
        print(msg + text + "\n")

    def decide_card_trump(self, cards):
        self.display_hand( f"Current player: {self}\n", self.hand )

        if FARMERS_HAND:
            self.check_for_farmers_hand( cards )
        while True:
            answer = input(f"Would you like {cards[20]} to be trump? Y or N? ").lower()
            print()
            if answer == "y":
                if GOING_ALONE:
                    self.check_for_going_alone()
                return True
            if answer == "n":
                return False
            print("Answer wasn't recognized.\n")

    

    def pick_trump(self, trump ):
        self.display_hand( f"Current player: {self}\n", self.hand )
        while True:
            answer = input("What trump would you like? N to pass. ")
            if answer == trump:
                print("Suit can't be previous suit.")
                continue
            if answer in Suits:
                if GOING_ALONE:
                    self.check_for_going_alone()
                return answer
            if answer.lower() == "n":
                if self.is_dealer and STICK_THE_DEALER:
                    print("You must pick a suit.\n")
                    continue
                return None
            print("Answer wasn't recognized.\n")

    def discard_card_for_trump(self, card):
        self.display_hand( f"Current player: {self}\n", self.hand )
        print(f"You must discard a card for {card}.")
        removed_card = self.get_card()
        self.hand.remove( removed_card )
        self.hand.append( card )

    def play_card(self, played_cards, trump):
        self.display_hand( f"Current player: {self}\n", self.hand )
        while True:
            card = self.get_card() 

            if card in self.get_legal_cards(played_cards, trump):
                self.hand.remove( card )
                played_cards.append( card)
                self.display_hand("Current played cards:", played_cards  )
                return

            needed_suit = played_cards[0].suit
            if self.is_card_left_bower( played_cards[0], trump ):
                needed_suit = BOWER_SUITS[ needed_suit ]

            print(f"Can't play that card, you must play a {needed_suit}")
        
    def check_for_farmers_hand( self, cards ):
        low_rank_count = 0
        for card in self.hand:
            if card.rank == "Ten" or card.rank == "Nine": 
                low_rank_count += 1
        if low_rank_count >= 3:
            self.discard_for_farmers_hand( cards )

    def discard_for_farmers_hand( self, cards ):
        while True:
            answer = input("Would you like to discard for farmer's hand? Y or N? ").lower()
            if answer == "y":
                break
            if answer == "n":
                return
            print("Answer was not recognized")
        
        print("Select three cards to discard")
        cards_removed = []
        while True:
            card = self.get_card()
            if card.rank not in ("Nine","Ten"):
                print("Card must be a Nine or Ten to remove.\n")
                continue
            self.hand.remove( card )
            cards_removed.append( card )
            if len( cards_removed ) == 3:
                self.hand.extend( cards[21:24] )

                # This is so we can still perserve the reference we have to the cards array in the game class
                cards.pop()
                cards.pop()
                cards.pop()
                cards.append( cards_removed[0])
                cards.append( cards_removed[1])
                cards.append( cards_removed[2])
               
                self.display_hand( "Your new hand: ", self.hand )
                return

    def check_for_going_alone( self ):
        while True:
            answer = input("Would you like to go alone? Y or N? ").lower()
            if answer == "y":
                self.go_alone()
                return
            if answer == "n":
                return
            print("Answer wasn't recognized.\n")

    def go_alone( self ):
        self.going_alone = True
        self.teammate.can_play = False
            
    def __repr__(self):
        return self.name.upper()

class AI_Player( Player ):
    def __init__(self, name):
        super().__init__( name )

AiP1 = AI_Player( "AIPlayer1")

print( AiP1 )

if __name__ == "__main__":  
    # Set Up 
    Euchre = Game()

    Suits = ("Hearts","Diamonds","Clubs","Spades")
    Ranks = ("Nine","Ten","Jack","Queen","King","Ace")
    Names = ("player1", "player2", "player3", "player4")

    # Set up cards in Euchre object
    for i in range(4): 
        Euchre.add_players( Player(Names[i]) )
        for j in range(6):
            Euchre.add_card( Card(Ranks[j], Suits[i]) )

    # Set up teammates for going alone
    Euchre.players[0].teammate = Euchre.players[2]
    Euchre.players[1].teammate = Euchre.players[3]
    Euchre.players[2].teammate = Euchre.players[0]
    Euchre.players[3].teammate = Euchre.players[1]

    # Set player 3 as dealer so when run Euchre.change_dealer() its player 1 who's dealer
    Euchre.players[3].is_dealer = True

    # Ask for rules
    STICK_THE_DEALER = True if input("Would you like stick the dealer? Y or N? ").lower() == "y" else False
    FARMERS_HAND = True if input("Would you like farmer's hand? Y or N? ").lower() == "y" else False
    GOING_ALONE = True if input("Would you like going alone? Y or N? ").lower() == "y" else False
    print("\n")

    def game():
        # Shuffle and deal cards
        Euchre.shuffle_cards()
        Euchre.deal_cards()

        # Change dealer from previous round
        Euchre.change_dealer()

        #For screw the dealer
        reset = Euchre.decide_trump()
        if reset: game()
    
        for _ in range(NUM_OF_TRICKS):
            # Play round and change who starts first next round
            played_cards = Euchre.play_round()
            winning_player_index = Euchre.determine_winner( played_cards )
            Euchre.change_starting_order( winning_player_index ) 

        # Calculate points for each team
        winning_team = Euchre.distribute_points()

        # If a team win ask if want to play again
        if winning_team != None:
            print(f"Players {winning_team} won!")
            if not Euchre.play_again():
                return
        game()

    game()