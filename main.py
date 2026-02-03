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
        print(f"Musí přehodit {minimal}\n")
        roundEnd = False
        self.scoreNow = 0

        while not roundEnd:
            input("Hod")

            dices = []
            validMovesIndex = 0
            validMoves = {}
            freeDices = 6

            debugDices = [1,2,3,4,5,5]
            for i in range(freeDices):
                #d = rollDice()
                d = debugDices[i]
                #sleep(randint(80, 100) / 100)
                print(d)
                dices.append(d)

            dices.sort()
            print(f"debug : {dices}")

            print("Co chcete udělat?")
            # nechat jakoukoliv kombinaci jedniček nebo pětek (100, 50)
            # trojičky atd (tři 4 = 400, čtyři je 400*2) X
            # postupka, automaticky do plných X
            # dohodit postupku
            frequencyList = []
            for i in range (1,7):
                f = dices.count(i)
                frequencyList.append(f)
                
                if f >= 3:
                    if i == 1: big = 1000
                    else: big = 100

                    increment = f-3

                    calculatedScore = i * big * (2 ** increment)
                    print(f"Tykráso, {f} krát {i}? No to snad neni možný. +{calculatedScore}")
                    


            print(f"debug: četnosti : {frequencyList}")

            if frequencyList == [1, 1, 1, 1, 1, 1]: # Postupka
                print("Postupka! +2000")
                self.scoreNow += 2000
            
            elif frequencyList.count(1) == 4 : # Dohodit postupku
                missingNumber = frequencyList.index(0)+1
                thrownNumber = frequencyList.index(2)+1
                print(f"Můžeš zkusit dohodit postupku, chybí ti {missingNumber} a máš dvě {thrownNumber}")
                tossChoice = input("Chceš to zkusit? (A/N) > ")

                if tossChoice.lower() == "a":
                    input("Hod")
                    d = rollDice()
                    print(d)
                    if d == missingNumber:
                        print("Hurá, postupka je v kapse. +2000")
                        self.scoreNow += 2000
                    else:
                        print("Někdy příště :)")
                        self.scoreNow = 0
                        roundEnd = True


            choice = input("něco")
        
        self.score += self.scoreNow
        print(f"{'Konec kola, získali jste':<30} {self.scoreNow}")
        print(f"{'celkové skóre činí':<30} {self.score}")
        print(f"{'počet čárek':<30} {self.lines}")


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
        print(f"\nHraje hráč {player.id} - {player.name}")

        player.play(mustOverThrow)

        if player.score >= winScore:
            print(f"Konec hry, vyhrává hráč {player.id} - {player.name} \n\tskóre - {player.score}")
            gameOver = True