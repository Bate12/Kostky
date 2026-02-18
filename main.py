from random import randint
from time import sleep

DICES_VISUAL_LIST = [
    """+-------+
|       |
|   ●   |
|       |
+-------+""",

    """+-------+
| ●     |
|       |
|     ● |
+-------+""",

    """+-------+
| ●     |
|   ●   |
|     ● |
+-------+""",

    """+-------+
| ●   ● |
|       |
| ●   ● |
+-------+""",

    """+-------+
| ●   ● |
|   ●   |
| ●   ● |
+-------+""",

    """+-------+
| ●   ● |
| ●   ● |
| ●   ● |
+-------+"""
]


class Player():
    def __init__(self, id, name : str) -> None:
        self.id = id
        self.name = name
        self.score = 0
        self.scoreNow = 0
        self.lines = 0

    def play(self, minimal):
        print(f"Musí hodit alespoň {minimal}\n")
        roundEnd = False
        self.scoreNow = 0
        freeDices = 6

        while not roundEnd:
            input("\tHod")

            dices = []
            lastScore = self.scoreNow

            for i in range(freeDices):
                d = rollDice()
                dices.append(d)

            dice_images = [DICES_VISUAL_LIST[d-1] for d in dices]
            split_dice = [img.splitlines() for img in dice_images]

            for row_parts in zip(*split_dice):
                print("  ".join(row_parts))

            dices.sort()
            print()
            print(*dices)

            print("___________________________________________________\n")

            # nechat jakoukoliv kombinaci jedniček nebo pětek (100, 50)
            # trojičky atd (tři 4 = 400, čtyři je 400*2) X
            # postupka, automaticky do plných X
            # dohodit postupku
            frequencyList = []
            for i in range (1,7):
                currentNumberCount = dices.count(i)
                frequencyList.append(currentNumberCount)
                
                if currentNumberCount >= 3:
                    if i == 1: big = 1000
                    else: big = 100

                    increment = currentNumberCount-3

                    calculatedScore = i * big * (2 ** increment)
                    print(f"Tykráso, {currentNumberCount} krát {i}? No to snad neni možný. +{calculatedScore}")

                    keepChoice = input("Chceš si to nechat? (A/N) > ")
                    if keepChoice.lower() == "a":
                        self.scoreNow += calculatedScore
                        freeDices -= currentNumberCount
                        frequencyList[i-1] = 0


            #print(f"debug: četnosti : {frequencyList}")

            if frequencyList == [1, 1, 1, 1, 1, 1]: # Postupka
                print("Postupka! +2000\n")
                self.scoreNow += 2000
                freeDices = 0
                frequencyList = [0, 0, 0, 0, 0, 0]
            
            elif frequencyList.count(1) == 4 and freeDices == 6 : # Dohodit postupku
                missingNumber = frequencyList.index(0)+1
                thrownNumber = frequencyList.index(2)+1
                print(f"Můžeš zkusit dohodit postupku, chybí ti {missingNumber} a máš dvě {thrownNumber}")
                tossChoice = input("Chceš to zkusit? (A/N) > ")

                if tossChoice.lower() == "a":
                    input("\tHod")
                    d = rollDice()
                    print(DICES_VISUAL_LIST[d-1],"\n")
                    if d == missingNumber:
                        print("Hurá, postupka je v kapse. +2000\n")
                        self.scoreNow += 2000
                        freeDices = 0
                        frequencyList = [0, 0, 0, 0, 0, 0]
                    else:
                        print("Někdy příště :)")
                        self.scoreNow = 0
                        roundEnd = True
                        self.lines += 1
                        continue

            if frequencyList[0] > 0: # Jedničky
                oneChoice = getKeepChoice("jedničku", frequencyList[0])
                
                if oneChoice > 0:
                    self.scoreNow += oneChoice * 100
                    freeDices -= oneChoice

            if frequencyList[4] > 0: # Pětky
                fiveChoice = getKeepChoice("pětku", frequencyList[4])
                
                if fiveChoice > 0:
                    self.scoreNow += fiveChoice * 50
                    freeDices -= fiveChoice

            if freeDices == 0:
                print("Jde se do plných, všechny kostky byly vrženy")
                freeDices = 6
                continue

            if self.scoreNow == lastScore and freeDices == 6: # Poslední šance dohodit postupku
                print("\nNehodil jsi nic, ale můžeš zkusit dohodit postupku")
                missingNumbers = []

                for i in range(0,6):
                    currentFrequency = frequencyList[i]
                    if currentFrequency == 0:
                        missingNumbers.append(i+1)
                
                missingNumbers.sort()
                print(f"Chybí ti tyto čísla > {missingNumbers}\n")

                rolledNumbers = []
                input("\tHod")
                for i in range(len(missingNumbers)):
                
                    d = rollDice()
                    rolledNumbers.append(d)

                dice_images = [DICES_VISUAL_LIST[d-1] for d in rolledNumbers]
                split_dice = [img.splitlines() for img in dice_images]

                for row_parts in zip(*split_dice):
                    print("  ".join(row_parts))

                rolledNumbers.sort()

                if missingNumbers == rolledNumbers:
                    print("\nLets go vyšlo to, máš postupku +2000\n")
                    self.scoreNow += 2000
                    freeDices = 0
                    frequencyList = [0, 0, 0, 0, 0, 0]

                else:
                    print("\nNevyšlo to, někdy příště")
                    self.lines += 1
                    self.scoreNow = 0
                    roundEnd = True
                    continue


            elif self.scoreNow == lastScore:
                print("Bohužel jsi nic nehodil, smutné\n")
                self.scoreNow = 0
                self.lines += 1
                roundEnd = True
                continue

            if self.scoreNow >= minimal:
                continueChoice = input("Chceš pokračovat? (A/N) > ")
                if continueChoice.lower() == "a":
                    if freeDices == 0:
                        freeDices = 6
                else:
                    roundEnd = True
                    self.lines = 0

            else:
                print(f"\nZatím máš {self.scoreNow} bodů, musíš přehodit {minimal} aby jsi mohl pokračovat.", end="\n\n")

        
        self.score += self.scoreNow

        if self.lines == 3:
            print("Vynuloval jsi, máš tři čárky :(")
            self.score = 0
            self.lines = 0

        print(f"\n{'Konec kola, získali jste':<30} {self.scoreNow}")
        print(f"{'Celkový počet bodů':<30} {self.score}")
        print("___________________________________________________\n")

    

def rollDice() -> int:
    return randint(1,6)

def printPlayerScores(players : list[Player]):
    print("\n\t======= Skóre hráčů =======\n")
    for player in players:
        name_part = f"Hráč {player.id} - {player.name} >"
        score_part = f"{player.score} bodů"

        print(f"{name_part:<25} {score_part:<15} {player.lines * '| '}")

def getKeepChoice(diceName, frequency):
    while True:
        try:
            choice = int(input(f"Chceš si nechat nějakou {diceName}? Zadej číslo 0 - {frequency} > "))
            break
        except ValueError:
            print("Zadej číslo!")
            continue
        except Exception as e:
            raise e
    return choice


players = []
minimalScore = 350
winScore = 10_000
gameOver = False

while True:
    try:
        choice = int(input("Zadej počet hráčů > "))
        if choice <= 1:
            print("Musí být alespoň dva hráči!\n")
            continue
        playerCount = choice
        break
    except ValueError:
        print("Zadej číslo!\n")
        continue

for i in range(1, playerCount+1):
    name = input(f"Napište jméno {i}. hráče > ")
    player = Player(i, name)
    players.append(player)

print()
for player in players:
    print(f"Hráč {player.id} > {player.name}")

print("\n\tHra začíná")

mustOverThrow = minimalScore
playerWon = None

while not gameOver:
    for player in players:
        print(f"\nHraje hráč {player.id} - {player.name}")

        player.play(mustOverThrow)

        if mustOverThrow <= player.scoreNow:
            mustOverThrow = player.scoreNow + 50
        else:
            mustOverThrow = minimalScore

        if player.score >= winScore:
            playerWon = player
            winScore = player.score

    if playerWon:
        print(f"Konec hry, vyhrává hráč {playerWon.id} - {playerWon.name}. Gratulujeme :D\n")
        gameOver = True

    printPlayerScores(players)