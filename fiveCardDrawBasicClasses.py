import random

#each card has a suit and a value.
#Suits are: 'SPADE', 'HEART', 'DIAMOND', 'CLUB'
#Card Values are: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ,14
#Each number corresponds to the card value, except, 11, ... , 14 are Jack, ... , Ace
class Card:
    def __init__(self, cardValue: int, suit: str):
        self.cardValue = cardValue
        self.suit = suit
        
    #prints the card as 'X of SUIT'
    def print(self):
        if self.cardValue < 11:
            print(self.cardValue, 'of ', end='')
        elif(self.cardValue == 11):
            print('Jack of ', end='')
        elif(self.cardValue == 12):
            print('Queen of ', end='')
        elif(self.cardValue == 13):
            print('King of ', end='')
        elif(self.cardValue == 14):
            print('Ace of ', end='')
        print(self.suit, 's', sep='')
        

#A deck has up to 52 cards, but may have less if cards have been dealt
class Deck:
    deck = []
    #default constructor loads deck with standard 52 cards
    def __init__(self):
        for suit in ['SPADE', 'HEART', 'DIAMOND', 'CLUB']:
            for value in range(2,15):
                self.deck.append(Card(value, suit))
                
    #randomizes the order of the deck
    def shuffle(self):
        newDeck = []
        for i in range(51, -1, -1):            
            index = random.randint(0,i)
            newDeck.append(self.deck.pop(index))
        self.deck = newDeck
        
    #prints the deck in order
    def print(self):
        for card in self.deck:
            card.print()

    #returns a bool if the deck is empty or not
    def empty(self):
        if len(self.deck) > 0:
            return False
        else:
            return True

    #removes the last card from the deck and returns it
    def drawCard(self) -> Card:
        if not self.empty():
            return self.deck.pop()
    
            

#a hand consists of up to five cards and can be compared with other hands
class Hand:
    def __init__(self):
        self.hand = []
    
    #adds the card to a hand
    def addCard(self, card: Card):
        self.hand.append(card)

    #removes a card from the hand by its index, returns the card
    def removeCard(self, index: int) -> Card:
        if index < len(self.hand):
            return self.hand.pop(index)

    #gets a card from the hand by its  index, keeps the card
    def getCard(self, index: int) -> Card:
        return self.hand[index]
        
    def print(self):
        for card in self.hand:
            card.print()


#A player has a hand and an amount of money which they can bet
#They may or may not have folded
class Player:
    def __init__(self, name: str, money: int):
        self.money = money
        self.name = name
        self.hand = Hand()
        self.hasFolded = False
        self.isAllIn = False
        self.amountBet = 0

    #subtracts the amount from the person, returning true if the player has enough
    def bet(self, amount: int) -> bool:
        if amount <= self.money:
            self.money = self.money - amount
            self.amountBet += amount
            return True
        else:
            return False
        
    def allIn(self):
        self.isAllIn = True

    def fold(self):
        self.hasFolded = True
    def unfold(self):
        self.hasFolded = False

    def print(self):
        print('Name:', self.name)
        print('Money:', self.money)
        if(self.hasFolded):
            print("Status: Folded")
        else:
            print('Hand:')
            self.hand.print()
        




