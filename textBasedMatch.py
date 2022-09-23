from match import *
import AI

def runTextBasedMatch(minBet: int, anteAmount: int, players, AIplayers):#AIplayers is an lsit of ints; if it is 0, it is a player, if it is 1, it is the dumb ai, if it is 2, it is the smart ai
    m = Match(minBet,anteAmount,players)
    while (m.state != State.WIN_BY_FOLD and m.state != State.END):
        m.print()
        if m.state == State.ANTE:
            print("\n\n--------------------------------------------------------------------------------------\n\n")
            if not AIplayers[m.curPlayerTurn]:#it is a player
                print("It is ", m.players[m.curPlayerTurn].name, "'s turn!", sep="")
                print("Please ante up!")
                print("Ante up price is:", m.anteAmount)
                x = input("Enter y to anti and anything else to fold: ")
                if x == 'y':
                    m.anteUp(m.curPlayerTurn)
                else:
                    m.fold(m.curPlayerTurn)
            else:
                m.anteUp(m.curPlayerTurn)#the AI always antes up
        elif m.state == State.BET1:
            print("\n\n--------------------------------------------------------------------------------------\n\n")
            if not AIplayers[m.curPlayerTurn]:#it is a player
                print("It is ", m.players[m.curPlayerTurn].name, "'s turn!", sep="")
                print("Please bet!")
                print("Your money:", m.players[m.curPlayerTurn].money)
                print("Current bet is:", m.curBet)
                print("You have already bet:", m.amountBetThisRound[m.curPlayerTurn])
                x = int(input("Enter an amount to bet or -1 to fold or -2 to check: "))
                if x == -1:
                    m.fold(m.curPlayerTurn)
                elif x == -2:
                    m.check(m.curPlayerTurn)
                else:# the player wants to bet
                    m.bet(m.curPlayerTurn, x)
            else:#have the AI bet
                if AIplayers[m.curPlayerTurn] == 1:#it is the dumb ai
                    bet = AI.randomAIBet(m.players[m.curPlayerTurn], m.curBet+m.players[m.curPlayerTurn].amountBet-m.amountBetThisRound[m.curPlayerTurn])
                elif AIplayers[m.curPlayerTurn] == 2:#it is the smart ai
                    bet = AI.smartAIBet(m.players[m.curPlayerTurn], m.curBet+m.players[m.curPlayerTurn].amountBet-m.amountBetThisRound[m.curPlayerTurn])
                if bet == -1:
                    print(m.players[m.curPlayerTurn].name, "folded.")
                    m.fold(m.curPlayerTurn)
                else:
                    print(m.players[m.curPlayerTurn].name, " has bet: ", bet, "!",sep="")
                    m.bet(m.curPlayerTurn, bet)
        elif m.state == State.TRADE:
            print("\n\n--------------------------------------------------------------------------------------\n\n")
            if not AIplayers[m.curPlayerTurn]:#it is a player
                print("It is ", m.players[m.curPlayerTurn].name, "'s turn!", sep="")
                print("Please trade up to three cards!")
                x = input("Enter up to three cards to trade by index (0-4) seperated by a comma but no space.\nIf you want to trade nothing, press enter: ")
                cards = []
                if len(x) != 0:
                    x = x.split(',')
                    for string in x:
                        cards.append(int(string))
                m.trade(m.curPlayerTurn, cards)
            else:# it is the AI
                if AIplayers[m.curPlayerTurn] == 1:#it is the dumb ai
                    cards = AI.randomAIDraw(m.players[m.curPlayerTurn])
                elif AIplayers[m.curPlayerTurn] == 2:#it is the smart ai
                    cards = AI.smartAIDraw(m.players[m.curPlayerTurn])
                print(m.players[m.curPlayerTurn].name, " traded cards: ", cards, "!",sep="")
                m.trade(m.curPlayerTurn, cards[0:3])#trade the cards
        elif m.state == State.BET2:
            print("\n\n--------------------------------------------------------------------------------------\n\n")
            if not AIplayers[m.curPlayerTurn]:#it is a player
                print("It is ", m.players[m.curPlayerTurn].name, "'s turn!", sep="")
                print("Please bet!")
                print("Your money:", m.players[m.curPlayerTurn].money)
                print("Current bet is:", m.curBet)
                print("You have already bet:", m.amountBetThisRound[m.curPlayerTurn])
                x = int(input("Enter an amount to bet or -1 to fold or -2 to check: "))
                if x == -1:
                    m.fold(m.curPlayerTurn)
                elif x == -2:
                    m.check(m.curPlayerTurn)
                else:# the player wants to bet
                    m.bet(m.curPlayerTurn, x)
            else:
                if AIplayers[m.curPlayerTurn] == 1:#it is the dumb ai
                    bet = AI.randomAIBet(m.players[m.curPlayerTurn], m.curBet+m.players[m.curPlayerTurn].amountBet-m.amountBetThisRound[m.curPlayerTurn])
                elif AIplayers[m.curPlayerTurn] == 2:#it is the smart ai
                    bet = AI.smartAIBet(m.players[m.curPlayerTurn], m.curBet+m.players[m.curPlayerTurn].amountBet-m.amountBetThisRound[m.curPlayerTurn])
                if bet == -1:
                    print(m.players[m.curPlayerTurn].name, "folded.")
                    m.fold(m.curPlayerTurn)
                else:
                    print(m.players[m.curPlayerTurn].name, " has bet: ", bet, "!",sep="")
                    m.bet(m.curPlayerTurn, bet)
                    
        
    print("\n\n--------------------------------------------------------------------------------------\n\n")
    m.endMatch()
    winner = m.getWinningPlayer(m.players)
    print("The match has ended!")
    print("The final match state is: ")
    m.print()
    print("\nAnd the winner is...")
    print(winner.name, "!", sep="")

STARTING_CASH = 100


g = Player("George", STARTING_CASH)
ai1 = Player("AIsmart", STARTING_CASH)
t = Player("Tom", STARTING_CASH)
ai2 = Player("AIsimple", STARTING_CASH)

runTextBasedMatch(5,10,[g,ai1,t,ai2], [0, 2, 0, 1])