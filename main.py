from random import randint
from time import sleep

class Player():
    def __init__(self, id, name : str) -> None:
        self.id = id
        self.name = name
        self.score = 0
        self.scoreNow = 0
        self.lines = 0

    def play(self, minimal):
        print(f"Musí přehodit {minimal}")
        roundEnd = False
        self.scoreNow = 0
        while not roundEnd:
            input("Hod")

            dices = []
            freeDices = 6

            for i in range(freeDices):
                d = rollDice()
                sleep(randint(80, 100) / 100)
                print(d)
                dices.append(d)

            dices.sort()
            print(f"debug : {dices}")

            print("Co chcete udělat?")
            # nechat jakoukoliv kombinaci jedniček nebo pětek (100, 50)
            # trojičky atd (tři 4 = 400, čtyři je 400*2)
            # postupka, automaticky do plných
            # dohodit postupku
            frequencyList = []
            for i in range (1,6):
                f = dices.count(i)
                frequencyList.append(f)
                
                if f == 6:
                    if i == 0: big = 1000
                    else: big = 100

                    calculatedScore = (i+1) * big * 8
                    print(f"Tykráso, šest {i+1}? No to snad ani neni možný. +{calculatedScore}")
            print(f"debug: četnosti : {frequencyList}")

            if frequencyList == [1, 1, 1, 1, 1]: # Postupka
                print("Postupka! +2000")
                self.scoreNow += 2000

            choice = input("něco")


def rollDice() -> int:
    return randint(1,6)


players = []
playerCount = 2
minimalScore = 350
winScore = 10_000
gameOver = False

for i in range(1, playerCount+1):
    name = input(f"Napište jmnéno {i}. hráče > ")
    player = Player(i, name)
    players.append(player)

print()
for player in players:
    print(f"Hráč {player.id} > {player.name}")

print("\n\tHra začíná")

mustOverThrow = minimalScore
while not gameOver:
    for player in players:
        print(f"Hraje hráč {player.id} - {player.name}")

        player.play(mustOverThrow)

        if player.score >= winScore:
            print(f"Konec hry, vyhrává hráč {player.id} - {player.name} \n\tskóre - {player.score}")
            gameOver = True