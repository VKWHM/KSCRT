import sys
import os
import random

def parse_args():
    if len(sys.argv) < 2 or not str(sys.argv[1]).upper() in ['X', 'O']:
        sys.stderr.write("usage: {} <select 'X' or 'O' to start with it>\n".format(sys.argv[0]))
        sys.exit(1)
    return str(sys.argv[1]).upper()

class XOX:
    def __init__(self, start='O'):
        self.player = start
        self.ai = "X" if start == "O" else "O"
        self.empty = ' '
        self.board = [
            ['', '  | ', '', ' |  ', ''],
            ['---','|','---','|','---'],
            ['', '  | ', '', ' |  ', ''],
            ['---','|','---','|','---'],
            ['', '  | ', '', ' |  ', ''],
        ]
        self.inputs = [[self.empty for _ in range(3)] for _ in range(3)]
        self.winner = None

    @property
    def hasWinner(self):
        for player in [self.ai, self.player]:
            if self._checkWinner(player):
                self.winner = player
                return True
        return False

    def getUserInput(self):
        while True:
            result = input(f"[{self.player}] [1,2,3]/[1,2,3]~# ")
            try:
                h,v = [int(i) for i in result.strip().split('/')]
                if h in [1,2,3] and v in [1,2,3]:
                    return (int(h-1), int(v-1))
            except ValueError:
                pass

    def setOnBoard(self, player, h, v):
        if self.inputs[h][v] == self.empty:
            self.inputs[h][v] = player
            return True
        return False

    def _clearScreen(self):
        if sys.platform.startswith('win'):
            os.system('cls')
        else:
            os.system('clear')

    def printBoard(self):
        self._clearScreen()
        placer = [0,0,1,0,2]
        for i,list_ in enumerate(self.board):
            for j, item in enumerate(list_):
                if i % 2 == 0 and j % 2 == 0:
                    print(self.inputs[placer[i]][placer[j]], end='')
                print(item, end='')
            print('')

    def _checkWinner(self, player):
        filterated = list(map(lambda x: list(map(lambda y: y == player, x)), self.inputs))
        for i,list_ in enumerate(filterated):
            for j, item in enumerate(list_):
                if item and list_[(j+1) % len(list_)] and list_[(j+2) % len(list_)]:
                    return True
                elif item and filterated[(i+1) % len(list_)][j] and filterated[(i+2) % len(list_)][j]:
                    return True
                elif ([i,j] in [[0,0],[1,1], [2,2]]) and (item and filterated[(i+1) % len(list_)][(j+1) % len(list_)] and filterated[(i+2) % len(list_)][(j+2) % len(list_)]):
                    return True

                # [[0,2], [1,1], [0,2]] changed to [[0,2], [1,1], [2,0]]
                # [(i-1) % len(list_)][(j   -    1) % len(list_)] changed to [(i-1) % len(list_)][(j   +   1) % len(list_)]
                elif ([i,j] in [[0,2],[1,1], [2,0]]) and (item and filterated[(i-1) % len(list_)][(j+1) % len(list_)] and filterated[(i-2) % len(list_)][(j+2) % len(list_)]):
                    return True
        return False

    def _check(self, player):
        filterated = list(map(lambda x: list(map(lambda y: y == player, x)), self.inputs))
        for i,list_ in enumerate(filterated):
            for j, item in enumerate(list_):
                if item and list_[(j+1) % len(list_)] and self.inputs[i][(j+2) % len(list_)] == self.empty:
                    return (i, (j+2) % len(list_))
                elif item and filterated[(i+1) % len(list_)][j] and self.inputs[(i+2) % len(list_)][j] == self.empty:
                    return ((i+2) % len(list_), j)
                elif ([i,j] in [[0,0],[1,1], [2,2]]) and (item and filterated[(i+1) % len(list_)][(j+1) % len(list_)] and self.inputs[(i+2) % len(list_)][(j+2) % len(list_)] == self.empty):
                    return ((i+2) % len(list_), (j+2) % len(list_))
                # [[0,2], [1,1], [0,2]] changed to [[0,2], [1,1], [2,0]]
                elif ([i,j] in [[0,2],[1,1], [2,0]]) and (item and filterated[(i-1) % len(list_)][(j-1) % len(list_)] and self.inputs[(i-2) % len(list_)][(j-2) % len(list_)] == self.empty):
                    return ((i-2) % len(list_), (j-2) % len(list_))
        return None

    def runAI(self):
        for player in [self.ai, self.player]:
            result = self._check(player)
            if result is not None:
                self.setOnBoard(self.ai, *result)
                return
        else:
            # condition added
            if not self.hasWinner:
                while True:
                    if self.setOnBoard(self.ai, random.randint(0,2), random.randint(0,2)):
                        return

if __name__ == '__main__':
    xox = XOX(parse_args())
    while not xox.hasWinner:
        xox.printBoard()
        while True:
            result = xox.getUserInput()
            if xox.setOnBoard(xox.player, *result):
                break

        # check winner before run AI
        if not xox.hasWinner and xox.player == 'X':
            xox.runAI()
    else:
        xox.printBoard()
        print("The Winner is: ", xox.winner)
