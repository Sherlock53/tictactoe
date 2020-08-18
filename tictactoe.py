# write your code here
import random
from math import inf as infinity
HUMAN='O'
COMP='X'
class TicTacToe:
    def __init__(self,state,field,playerone,playertwo):
        self.state = state
        self.field = field
        self.gamestatus = False
        self.player = 'X'
        self.playerone = playerone
        self.playertwo =playertwo

    def __str__(self):
        s='---------\n'
        for i in range(3):
            s += "|"
            for t in range(3):
                s +=' ' + self.state[i*3+t]
            s += " |\n"
        s+='---------'
        return s

    def checkwin(self,c):
        if [c,c,c] in self.field:
            return True
        else:
            return False

    def fields(self,state):
        self.field=[]
        for i in range(3):
            self.field.append([state[i*3 + k] for k in range(3)])
            self.field.append([state[t] for t in range(9) if t % 3 == i])
        self.field.append([state[0],state[4],state[8]])
        self.field.append([state[2],state[4],state[6]])

    def status(self):
        self.fields(self.state)
        if abs(len([i for i in self.state if i=='O']) - len([i for i in self.state if i == 'X'])) > 1 or (self.checkwin('X') and self.checkwin('O')):
            print("Impossible")
        else:
            if self.checkwin('X'):
                self.gamestatus = True
                #print("X wins")
            elif self.checkwin('O'):
                self.gamestatus = True
                #print("O wins")
            elif '_' in self.state:
                self.gamestatus = False
                #print("Game not finished")
            else:
                self.gamestatus = True
                #print("Draw")

    def randomstep(self):
        x = random.randint(1,3)
        y = random.randint(1,3)
        while True:
            pos = (3-int(y))*3 +(int(x)-1)
            if self.state[pos] == '_':
                break
            x = random.randint(1,3)
            y = random.randint(1,3)
        return pos

    def oppositeplayer(self,player):
        if player == 'X':
            return 'O'
        else:
            return 'X'

    def easycompstep(self):
        print('Making move level "easy"')
        pos=self.randomstep()
        self.state=self.state[:pos] + self.player + self.state[pos+1:]
        self.player=self.oppositeplayer(self.player)
        return

    def checkifwinpos(self,player):
        for i in range(3):
            a=[self.state[i*3 + k] for k in range(3)]
            if a.count(player)==2 and '_' in a:
                return i*3+a.index('_')
            a=[self.state[t] for t in range(9) if t % 3 == i]
            if a.count(player)==2 and '_' in a:
                return i+a.index('_')*3
        a=[self.state[0],self.state[4],self.state[8]]
        if a.count(player)==2 and '_' in a:
            return a.index('_')*4
        a=[self.state[2],self.state[4],self.state[6]]
        if a.count(player)==2 and '_' in a:
            return (a.index('_')+1)*2
        return -1

    def mediumcompstep(self):
        print('Making move level "medium"')
        pos=-1
        pos=self.checkifwinpos(self.player)
        if pos ==-1:
            pos=self.checkifwinpos(self.oppositeplayer(self.player))
        if pos==-1:
            pos=self.randomstep()
        self.state=self.state[:pos] + self.player + self.state[pos+1:]
        self.player=self.oppositeplayer(self.player)
        return

    def step(self):
        t=input('Enter the coordinates:')
        if ' ' not in t:
            print("You should enter numbers!")
            self.step()
            return
        x,y = t.split()
        if not x.isdigit() or not y.isdigit():
            print("You should enter numbers!")
            self.step()
            return
        if int(x) not in range(1,4) or int(y) not in range(1,4):
            print('Coordinates should be from 1 to 3!')
            self.step()
            return
        pos = (3-int(y))*3 +(int(x)-1)
        if self.state[pos] != '_':
            print('This cell is occupied! Choose another one!')
            self.step()
            return
        else:
            self.state=self.state[:pos] + self.player + self.state[pos+1:]
            self.player=self.oppositeplayer(self.player)
            return

    def evaluate(self,state):
        self.fields(state)
        if self.checkwin(self.player):
            score = 1
        elif self.checkwin(self.oppositeplayer(self.player)):
            score = -1
        else:
            score = 0
        return score

    def hardplayerstep(self):
        print('Making move level "hard"')
        if self.state.count('_')==0:
            return
        if 9 == self.state.count('_'):
            pos=self.randomstep()
        else:
            move=self.minimax(self.state,self.state.count('_'),self.player)
            pos=move[0]
        self.state=self.state[:pos] + self.player + self.state[pos+1:]
        self.player=self.oppositeplayer(self.player)


    def empty_cells(self,state):
        cells=[]
        for i in range(len(state)):
            if state[i]=='_':
                cells.append(i)
        return cells

    def minimax(self,state,depth,player):
        if player==self.player:
            best = [-1,-infinity]
        else:
            best =[-1, +infinity]
        if depth == 0 or self.evaluate(state)!=0:
            score = self.evaluate(state)
            return [-1, score]
        for cell in self.empty_cells(state):
            state=state[:cell] + player + state[cell+1:]
            score=self.minimax(state,depth-1,self.oppositeplayer(player))
            state=state[:cell] + '_' + state[cell+1:]
            score[0]=cell

            if player == self.player:
                if score[1]>best[1]:
                    best=score
            else:
                if score[1] < best[1]:
                    best =score
        return best

class Playing:
    def plays(self,action):
        if action=="exit":
            return False
        if "start" not in action:
            print("Bad parameters!")
            return True
        if "start" in action and action.count(' ')<2:
            print("Bad parameters!")
            return True
        at=action.split()
        game=TicTacToe('_________',[],at[1],at[2])
        print(game)
        while not game.gamestatus:
            if game.player=='X':
                if game.playerone=="easy":
                    game.easycompstep()
                elif game.playerone=="user":
                    game.step()
                elif game.playerone=="medium":
                    game.mediumcompstep()
                elif game.playerone=="hard":
                    game.hardplayerstep()
            else:
                if game.playertwo=="easy":
                    game.easycompstep()
                elif game.playertwo=="user":
                    game.step()
                elif game.playertwo=="medium":
                    game.mediumcompstep()
                elif game.playertwo=="hard":
                    game.hardplayerstep()
            print(game)
            game.status()

        if game.checkwin('X'):
            print("X wins")
        elif game.checkwin('O'):
            print("O wins")
        else:
            print("Draw")
        return True

plays=input()
playing=Playing()
while playing.plays(plays):
    plays=input()
