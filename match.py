from fiveCardDrawBasicClasses import *
from operator import itemgetter
from enum import Enum, auto
import winningHand

#has all the states a match could be in
class State(Enum):
    ANTE = auto()#players must ante up
    DEAL = auto()#deal cards
    BET1 = auto()#first round of betting
    TRADE = auto()#trade up to 3 cards
    BET2 = auto()#2nd round of betting
    END = auto()#reveal cards and declare winner
    WIN_BY_FOLD = auto()#the state if a player wins because everyone else folded


#The match class describes the current state of a match. 
#A match can be completely run by examining the state and calling: anteUp, fold, bet, and trade functions (expected to be called with event handlers in the UI)
class Match:
    def __init__(self, minBet: int, anteAmount: int, players):
        #ADD CHECKS HERE TO MAKE SURE WE HAVE VALID PARAMETERS

        #set the current state
        self.state = State.ANTE
        self.curPlayerTurn = 0 #the first player goes first

        #set the basic parameters
        self.anteAmount = anteAmount
        self.curPot = 0
        self.minBet = minBet
        self.curBet = minBet
        self.lastPlayerChecked = True
        
        #initilize the players
        self.players = players
        self.numPlayers = len(players)
        self.amountBetThisRound = []
        self.lastPlayerToRaise = -1#this is the index of the player who last raised the bet
        for player in self.players:
            player.amountBet = 0
            player.isFolded = False
            player.isAllIn = False
            self.amountBetThisRound.append(0)
        
        #initilize the deck
        self.deck = Deck()
        self.deck.shuffle()

    #prints the current match  
    def print(self):
        print("state:",self.state)
        print("curPlayerTurn:", self.curPlayerTurn)
        print("curPlayer:", self.players[self.curPlayerTurn].name)
        print("pot:", self.curPot)
        print()
        print("---PLAYERS---")
        for p in self.players:
            p.print()
            print()#add a newline

    #deals cards to all of the players
    def dealCards(self):
        for i in range(0, 5):#give each player 5 cards
            for p in self.players:
                if not p.hasFolded:#make sure the player anted up
                    p.hand.addCard(self.deck.drawCard())

    #folds for the player if it is their turn, then advances the turn
    def fold(self, playerIndex: int):
        if self.curPlayerTurn == playerIndex:
            self.players[playerIndex].fold()
            self.advanceTurn()
        else:
            raise Exception("Player cannot fold when it is not their turn")
    
    #antes up the player and advances the turn or folds
    def anteUp(self, playerIndex: int):
        if self.curPlayerTurn == playerIndex and self.state == State.ANTE:
            if(self.players[playerIndex].bet(self.anteAmount)):
                self.curPot += self.anteAmount
                self.advanceTurn()
            else:
                raise Exception("Player cannot ante up")
        else:
            raise Exception("Not player's turn/Not ante state")
        
    #tries to bet the amount for the player. If amount = player.money, then the player bets all in
    def bet(self, playerIndex: int, amount: int):
        if self.curPlayerTurn == playerIndex and (self.state == State.BET1 or self.state == State.BET2):
            if amount == self.players[playerIndex].money:#all in 
                if self.curBet < amount + self.amountBetThisRound[playerIndex]:
                    self.curBet = amount + self.amountBetThisRound[playerIndex]
                self.amountBetThisRound[playerIndex] += amount
                self.players[playerIndex].bet(amount)# bet all the player's money
                self.players[playerIndex].allIn()
                self.curPot += amount
                self.lastPlayerChecked = False
                self.advanceTurn()

            elif amount <= self.players[playerIndex].money and (amount + self.amountBetThisRound[playerIndex]) >= self.curBet:
                self.players[playerIndex].bet(amount)
                if self.curBet < self.amountBetThisRound[playerIndex] + amount:#the player raised
                    self.lastPlayerToRaise = playerIndex
                self.curBet = amount + self.amountBetThisRound[playerIndex]#raise the bet if need be
                self.amountBetThisRound[playerIndex] += amount#the player has bet more
                self.curPot += amount#add the new amount
                self.lastPlayerChecked = False
                self.advanceTurn()

            elif amount < self.curBet:
                raise Exception("A player must bet at least the current bet or match it overall")
            else:
                raise Exception("A player cannot bet more than they have")
        else:
            raise Exception("Not player's turn/Not betting state")

    def check(self, playerIndex: int):
        if self.curPlayerTurn == playerIndex and (self.state == State.BET1 or self.state == State.BET2):
            if self.lastPlayerChecked:
                self.advanceTurn()
            else:
                raise Exception("A player cannot check if the last player did not")
        else:
            raise Exception("Not player's turn/Not bet state")


    #returns true if all nonfolded players have called, thus ending the betting round
    def allPlayersHaveBet(self):
        largestBet = 0
        for i in range(0, self.numPlayers):
            if not self.players[i].hasFolded:
                if self.amountBetThisRound[i] > largestBet:
                    largestBet = self.amountBetThisRound[i]
        if largestBet == 0:
            return False#no one has bet yet
        for i in range(0, self.numPlayers):
            if not self.players[i].hasFolded and not self.players[i].isAllIn:
                if self.amountBetThisRound[i] < largestBet:
                    return False
        return True

    def resetAmountBet(self):
        self.lastPlayerToRaise = -1
        for i in range(0, self.numPlayers):
            self.amountBetThisRound[i] = 0

    #tries to trade the specified cards from the player. cardsToTrade is a list of up to 3 integers corresponding to the cards in the player's hand to trade
    def trade(self, playerIndex: int, cardsToTrade):
        if self.curPlayerTurn == playerIndex and self.state == State.TRADE:
            if len(cardsToTrade) <= 3:
                #check to make sure each int is less than 5 and does not repeat
                tmpCards = []#a temporary list used to check if cards repeat
                for card in cardsToTrade:
                    if card >= 5:
                        raise Exception("Card indeces cannot exceed 4")
                    elif card in tmpCards:
                        raise Exception("Cannot trade the same card twice")
                    else:
                        tmpCards.append(card)#add to the list
                        #trade the card
                        self.players[playerIndex].hand.hand[card] = self.deck.drawCard()#replace the old card with a new one
                
            else:
                raise Exception("Cannot trade more than 3 cards")
        else:
            raise Exception("Not player's turn/Not trading state")
        self.advanceTurn()

    #returns the index of the next player who has not folded after the curIndex
    def getNextNonFoldedPlayer(self, curIndex: int) -> int:
        for offset in range(1, self.numPlayers+1):
            index = (curIndex+offset)%self.numPlayers#check the rest of the players
            if not self.players[index].hasFolded:
                return index

    #returns the index of the first player who has not folded
    def getFirstNonFoldedPlayer(self) -> int:
        for index in range(0, self.numPlayers):
            if not self.players[index].hasFolded:
                return index
        
    def advanceTurn(self):
        #check to see if the last player folded, thus allowing the remaining player to win by fold
        nxtPlayer = self.getNextNonFoldedPlayer(self.curPlayerTurn)

        if nxtPlayer == self.getNextNonFoldedPlayer(nxtPlayer):#in other words, this player is the last player standing
            self.state = State.WIN_BY_FOLD
            return
        #if we are in a betting state we need to handle differently
        if self.state == State.BET1 or self.state == State.BET2:
            nxtPlayer = self.getNextNonFoldedPlayer(self.curPlayerTurn)#the next player who has not folded
            #first check if everyone checked
            if self.lastPlayerChecked:
                tmpPlayer = nxtPlayer
                while self.players[tmpPlayer].isAllIn:#This player is all in and is done betting
                    tmpPlayer = self.getNextNonFoldedPlayer(tmpPlayer)#find the next player who isn't all in
                if tmpPlayer <= self.curPlayerTurn:#all players have checked
                    self.curPlayerTurn = self.getFirstNonFoldedPlayer()
                    if self.state == State.BET1:
                        self.state = State.TRADE
                    else:
                        self.state = State.END
                    return
            #now did everyone go all in
            if not self.allPlayersHaveBet():#not all players have called, folded or gone all in
                while self.players[nxtPlayer].isAllIn:#This player is all in and is done betting
                    nxtPlayer = self.getNextNonFoldedPlayer(nxtPlayer)#find the next player who isn't all in
                self.curPlayerTurn = nxtPlayer
            else:#we have finished a betting cycle
                self.curPlayerTurn = self.getFirstNonFoldedPlayer()
                if self.state == State.BET1:
                    self.state = State.TRADE
                else:
                    self.state = State.END  
        else:#we are in a TRADE or ANTE or END or WIN_BY_FOLD State
            curPlayer = self.curPlayerTurn#the player who just moved
            nxtPlayer = self.getNextNonFoldedPlayer(curPlayer)#the next player who has not folded
            self.curPlayerTurn = nxtPlayer
            if nxtPlayer <= curPlayer:#we need to change state since we made a cycle
                if self.state == State.ANTE:
                    self.dealCards()#deal the cards
                    self.state = State.BET1
                    self.lastPlayerChecked = True
                    self.curBet = self.minBet#reset the min bet
                    self.resetAmountBet()
                elif self.state == State.TRADE:
                    #check if all player are all in
                    for p in self.players:
                        if not p.hasFolded and not p.isAllIn:#we continue betting
                            self.state = State.BET2
                            self.lastPlayerChecked = True
                            self.curBet = self.minBet#reset the min bet
                            self.resetAmountBet()
                            #find the first player who is not all in
                            while self.players[self.curPlayerTurn].isAllIn:
                                self.curPlayerTurn = self.getNextNonFoldedPlayer(self.curPlayerTurn)
                            return
                        else:#all the players are either folded or all in
                            self.state = State.END
        return

    #returns the winning player from a set of players
    def getWinningPlayer(self, players):
        eligablePlayers = []
        for player in players:
            if not player.hasFolded:
                eligablePlayers.append(player)
        if len(eligablePlayers) > 0:
            return winningHand.winningHand(eligablePlayers)
        else:#there is no one who can win the game
            return False

    def determinePayouts(self):
        #copy the list of players so we can manipulate it
        players = []
        for player in self.players:
            players.append(player)

        while len(players) > 1:#there are still players who have money they have bet which needs to be allocated
            mainPot = 0#the pot which goes to the winner in players
            #first find the minimum amount bet
            minBet = players[0].amountBet
            for p in players[1:]:
                if p.amountBet < minBet:
                    minBet = p.amountBet
            #now we must subtract this amount from each players money and add it to the pot
            for player in players:
                mainPot += minBet
                player.amountBet -= minBet
            #find the winner and give him the money
            winner = self.getWinningPlayer(players)#find the winning player out of the remaining players (excudes folded players)
            winner.money += mainPot#pay the winner of the main pot
            #now we must adjust the players list to remove those who have no more money bet. They arent eligable for more winnings
            tmp = []
            for player in players:
                if player.amountBet > 0:
                    tmp.append(player)
            players = tmp

        #this is the special case where one player bet more than the rest and money must be returned
        if len(players) == 1:
            players[0].money += players[0].amountBet
            players[0].amountBet = 0 #reset the amountBet

    
    def endMatch(self):
        if self.state == State.END or self.state == State.WIN_BY_FOLD:
            self.determinePayouts()
        else:
            raise Exception("The match has not ended, yet endMatch was called")
