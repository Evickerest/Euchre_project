def renege( self, input, played_cards, trump ):
        if len( played_cards ) == 0: return False
        led_card = played_cards[0]
        led_suit = led_card.suit

        # If led card is left bower, led suit should be trump
        if self.is_card_left_bower( led_card, trump):
            led_suit = BOWER_SUITS[ led_suit ]

        # Checks is card played is legal
        if self.is_card_left_bower( input, trump):
            if led_suit == trump:
                return False
        elif input.suit == led_suit: 
            return False

        # For checking to see if there a card that could be played
        for card in self.hand:
            if self.is_card_left_bower(card, trump):
                if led_suit == trump: 
                    return True
            elif card.suit == led_suit: 
                return True

        return False