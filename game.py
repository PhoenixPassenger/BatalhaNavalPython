import os
import sys
import battlefield
import bombfield
import ship
import player
nth = {
    1: "primero",
    2: "segundo",
    3: "terceiro",
    4: "quarto",
    5: "quinto",
    6: "sexto",
    7: "setimo",
    8: "oitavo"
}

rowlist = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]


class Game:

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def __init__(self):
        self.p1 = ""
        self.p2 = ""

        self.p1Field = battlefield.Battlefield()
        self.p2Field = battlefield.Battlefield()
        self.p1BombField = bombfield.Bombfield()
        self.p2BombField = bombfield.Bombfield()

        self.ships = []
        self.ships.append(ship.Ship(5))
        self.ships.append(ship.Ship(4))
        self.ships.append(ship.Ship(4))
        self.ships.append(ship.Ship(2))
        self.ships.append(ship.Ship(2))
        self.ships.append(ship.Ship(2))
        self.ships.append(ship.Ship(1))
        self.ships.append(ship.Ship(1))

    def columnExist(self, column):
        if ("A" <= column <= "N"):
            return True
        else:
            return False

    def rowExist(self, row):
        if (1 <= row <= 14):
            return True
        else:
            return False

    def printfield(self, f):

        l = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
        spacing = ' '.join(['{:<2}'] * len(l))
        text = spacing.format(*l)
        for v in range(1, len(l)):
            text += "\n" + spacing.format(v, f['A'][v], f['B'][v], f['C'][v], f['D'][v], f['E'][v], f['F'][v],
                                          f['G'][v], f['H'][v], f['I'][v], f['J'][v], f['K'][v], f['L'][v], f['M'][v],
                                          f['N'][
                                              v])

        return text

    def placeShips(self, player):
        counter = 1

        print(player.name + ", coloque seus navios na posição inicial,\n")
        print("Depois diga a direção (right, left, up ou down)\n")

        print(self.printfield(player.field.field))

        for x in player.ships:
            column = ""
            row = ""
            direction = ""
            cellBusy = True
            pff = player.field.field
            while self.columnExist(column) == False or row not in rowlist or cellBusy == True:
                userInput = input(
                    player.name + ", em que celula (A-N)(1-14) você quer colocar sua " + nth[counter] + " barca?\n")
                if (len(userInput) >= 2):
                    column = userInput[0].upper()
                    row = userInput[1]
                    if len(userInput) >= 3:
                        row += userInput[2]
                if (self.columnExist(column) and row in rowlist):
                    cellBusy = pff[column][int(row)]

            row = int(row)

            newrow = row
            newcolumn = column
            if len(x.parts)==1:
                pff[newcolumn][newrow] = True
            else:
                while (
                        direction != "right" and direction != "left" and direction != "up" and direction != "down") or self.rowExist(
                        newrow) == False or self.columnExist(newcolumn) == False or cellBusy == True:
                    direction = input(player.name + ", qual direção (right, left, up or down) seu barco " + nth[
                        counter] + " está virado?\n")
                    cellBusy = False
                    partCounter = 0

                    for y in range(len(x.parts)):
                        newcolumn = column
                        newrow = row
                        if (direction == "down"):
                            newrow = row + partCounter

                        elif (direction == "up"):
                            newrow = row - partCounter

                        elif (direction == "left"):
                            newcolumn = chr(ord(column) - partCounter)

                        elif (direction == "right"):
                            newcolumn = chr(ord(column) + partCounter)

                        partCounter += 1
                        if self.columnExist(newcolumn) and self.rowExist(newrow):
                            if pff[newcolumn][newrow] == True:
                                cellBusy = pff[newcolumn][newrow]

                            elif pff[newcolumn][newrow] == False and partCounter == len(x.parts):
                                for p in range(0, partCounter):
                                    if (ord(newcolumn) < ord(column)):
                                        pff[chr(ord(column) - p)][newrow] = True
                                    elif (ord(newcolumn) > ord(column)):
                                        pff[chr(ord(column) + p)][newrow] = True
                                    elif (newrow < row):
                                        pff[newcolumn][newrow + p] = True
                                    elif (newrow > row):
                                        pff[newcolumn][newrow - p] = True

            self.clear()
            print(self.printfield(player.field.field))
            counter += 1

    def newPlayer(self, n, ships, field, bombfield):
        newName = input("Player " + str(n) + ",qual teu nick?\n")
        while newName == "":
            newName = input("Digita ai mano\n")
        self.clear()
        p = player.Player(newName, ships[:], field, bombfield)

        self.placeShips(p)
        return p

    def anythingLeft(self, d):
        newList = []

        def myprint(d):
            for k, v in d.items():
                if isinstance(v, dict):
                    myprint(v)
                else:
                    newList.append(v)

        myprint(d)
        return True in newList

    def selectCell(self, player):
        column = ""
        row = ""
        while self.columnExist(column) == False or row not in rowlist:
            userInput = input(player.name + ", onde (A-N)(1-14) tu quer mandar o pipoco?\n")

            if (len(userInput) < 2):
                column = ""
                row = ""
            else:
                column = userInput[0].upper()
                row = userInput[1]
                if len(userInput) == 3:
                    row += userInput[2]

        return [column, row]

    def bomb(self, player, enemy, column, row):
        eff = enemy.field.field
        self.result = ''

        row = int(row)
        if (eff[column][row] == True):
            self.result = 'X'
            eff[column][row] = 'X'
            player.bombfield.field[column][row] = 'X'

            if self.anythingLeft(eff) == False:
                self.result = player.name + " wins!"
        else:
            self.result = 'O'
            eff[column][row] = '@'
            if player.bombfield.field[column][row] != 'X':
                player.bombfield.field[column][row] = 'O'

    def start(self):
        while self.anythingLeft(self.p1.field.field) and self.anythingLeft(self.p2.field.field):
            print('Teu campo:\n')
            print(self.printfield(self.p1.field.field))
            print('\nCampo delas:\n')
            print(self.printfield(self.p1.bombfield.field))
            cell = self.selectCell(self.p1)
            self.bomb(self.p1, self.p2, cell[0], cell[1])
            self.clear()

            if self.result == 'X':
                print('ACERTOU CARA!')
            elif self.result == 'O':
                print('ERROOOOOU!')
            else:
                print(self.result)
                sys.exit()  # Exit the application

            print(self.printfield(self.p1.bombfield.field))

            input('aperta enter men')
            self.clear()

            if self.anythingLeft(self.p1.field.field) and self.anythingLeft(self.p2.field.field):
                print('Teu campo:\n')
                print(self.printfield(self.p2.field.field))
                print('\nCampo do babaca la:\n')
                print(self.printfield(self.p2.bombfield.field))
                cell = self.selectCell(self.p2)
                self.bomb(self.p2, self.p1, cell[0], cell[1])
                self.clear()

                if self.result == 'X':
                    print('Acertou, mizera!')
                elif self.result == 'O':
                    print('Errou de novo pora!')
                else:
                    print(self.result)
                    sys.exit()

                input('Aperta enter parça')
                self.clear()