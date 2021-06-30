import random
import sys
from sly import Parser,Lexer
#global function : for printing the grid on the terminal
def printGrid():               
    for i in range(4):
        for j in range(4): 
            print(game.gridCell[i][j],end='  ')
        print()
        print()

################################
#Board

class Board:
    def __init__(self):
        self.n=4
        self.gridCell=[[0]*4 for i in range(4)] 
        self.compress=False
        self.merge=False
        self.moved=False
        self.score=0
        self.tileName=[[[]]*4 for i in range(4)] 

    def cellValue(self,x,y):
        print(self.gridCell[x][y])
        
    def assignValue(self,value,x,y):
        self.gridCell[x][y]=value 
        if value==0:
            self.tileName[x][y]=[] 
        printGrid()

    def reverse(self):
        #gridCell
        for pos in range(4):
            i=0
            j=3
            while(i<j):
                self.gridCell[pos][i],self.gridCell[pos][j]=self.gridCell[pos][j],self.gridCell[pos][i]
                i+=1
                j-=1
        
        #tileName
        for pos in range(4):
            i=0
            j=3
            while(i<j):
                self.tileName[pos][i],self.tileName[pos][j]=self.tileName[pos][j],self.tileName[pos][i]
                i+=1
                j-=1
                 
    def transpose(self):
        self.gridCell=[list(t)for t in zip(*self.gridCell)]
        self.tileName=[list(t)for t in zip(*self.tileName)]

    def Merge(self,operation):     
        self.merge=False
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] > 0 and self.gridCell[i][j] == self.gridCell[i][j + 1]:
                    #modifying value in gridcell
                    if operation=="ADD":
                        self.gridCell[i][j]=self.gridCell[i][j]+self.gridCell[i][j]
                    elif operation=="SUBTRACT":
                        self.gridCell[i][j]=self.gridCell[i][j]-self.gridCell[i][j]
                    elif operation=="DIVIDE":
                        self.gridCell[i][j]=int(self.gridCell[i][j]/self.gridCell[i][j])
                    elif operation=="MULTIPLY":
                        self.gridCell[i][j]=self.gridCell[i][j]*self.gridCell[i][j]

                    #modifying tileName
                    if operation=="ADD":
                        self.tileName[i][j]=self.tileName[i][j]+self.tileName[i][j+1] 
                    elif operation=="SUBTRACT":
                        self.tileName[i][j]=[] 
                    elif operation=="DIVIDE":
                        self.tileName[i][j]=self.tileName[i][j]+self.tileName[i][j+1] 
                    elif operation=="MULTIPLY":
                        self.tileName[i][j]=self.tileName[i][j]+self.tileName[i][j+1] 
                    
                    self.tileName[i][j+1]=[]
                    self.gridCell[i][j + 1] = 0
                    self.merge = True
                    self.score += self.gridCell[i][j]
        
    def compressGrid(self):
        self.compress=False
        temp=[[0] *4 for i in range(4)]
        tileVar=[[[]]*4 for i in range(4)]
        for i in range(4):
            cnt=0
            for j in range(4):
                if self.gridCell[i][j]!=0:
                    temp[i][cnt]=self.gridCell[i][j]
                    if cnt!=j:
                        self.compress=True
                    cnt+=1
        self.gridCell=temp
        for i in range(4):
            cnt=0
            for j in range(4):
                if len(self.tileName[i][j])!=0: 
                    tileVar[i][cnt]=self.tileName[i][j]
                    cnt+=1
        self.tileName=tileVar
        
        
    def random_cell(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    cells.append((i, j))
        curr=random.choice(cells)
        i=curr[0]
        j=curr[1]
        self.gridCell[i][j]=2
    
    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1]:
                    return True
        
        for i in range(3):
            for j in range(4):
                if self.gridCell[i+1][j] == self.gridCell[i][j]:
                    return True
        return False
    
                    
    def assignName(self,varName,x,y):
        flag=True
        for i in range(4): 
            for j in range(4):
                for nm in self.tileName[i][j]:
                    if nm==varName:
                        flag=False
                        return flag
                    
        
        if self.gridCell[x][y]>0:
            self.tileName[x][y]=self.tileName[x][y]+[varName] 
            return flag
        elif self.gridCell[x][y]==0:
            flag=False
            return flag



##########################################
#Game

class Game:
    def __init__(self,game):
        self.game=game
        self.won=False
        self.end=False
    
    def start(self):
        self.game.random_cell()
        self.game.random_cell()
        print("The start state is:")
        printGrid()  
    
    def movement(self,operation,direction): 
        if self.end or self.won:
            return
        self.game.compress = False
        self.game.merge = False
        self.game.moved = False
        if direction=='UP':
            self.game.transpose()
            self.game.compressGrid()
            self.game.Merge(operation)
            self.game.moved = self.game.compress or self.game.merge
            self.game.compressGrid()
            self.game.transpose()
        elif direction=='DOWN':
            self.game.transpose()
            self.game.reverse()
            self.game.compressGrid()
            self.game.Merge(operation)
            self.game.moved = self.game.compress or self.game.merge
            self.game.compressGrid()
            self.game.reverse()
            self.game.transpose()
        elif direction=='LEFT':
            self.game.compressGrid()
            self.game.Merge(operation)
            self.game.moved = self.game.compress or self.game.merge
            self.game.compressGrid()
        elif direction=='RIGHT':
            self.game.reverse()
            self.game.compressGrid()
            self.game.Merge(operation)
            self.game.moved = self.game.compress or self.game.merge
            self.game.compressGrid()
            self.game.reverse()
        else:
            pass
        flag=0
        for i in range(4):
            for j in range(4):
                if(self.game.gridCell[i][j]==2048):           #if and gridCell value is 2048, The game must exit
                    flag=1
                    break
        if(flag==1): 
            self.won=True
            print("You have won the Game...........")
            return
        for i in range(4):
            for j in range(4):
                if self.game.gridCell[i][j]==0:
                    flag=1
                    break
        if not (flag or self.game.can_merge()):
            self.end=True
            print("You have lost. GAME OVER.........Try again")
        if self.game.moved:
            self.game.random_cell()
        printGrid()



################################################################
#Lexer 


class lexer_2048(Lexer):
    tokens = {STOP,COMMA,VAR,NUMBER,OPERATION,MOVEMENT,ASSIGN,TO,IS,VALUE,IN,OPERATION_ERR,MOVEMENT_ERR,ASSIGN_ERR,IN_ERR,VALUE_ERR,IS_ERR,TO_ERR}
    ignore = '\t '
    
    NUMBER = r'\d+'
    MOVEMENT = r'LEFT|UP|DOWN|RIGHT'
    OPERATION = r'MULTIPLY|ADD|DIVIDE|SUBTRACT'
    ASSIGN = r'ASSIGN'
    TO = r'TO'
    VALUE = r'VALUE'
    IN = r'IN'
    IS = r'IS'
    MOVEMENT_ERR=r'[lL][eE][fF][tT]|[uU][pP]|[dD][oO][wW][nN]|[rR][iI][gG][hH][tT]'
    OPERATION_ERR=r'[mM][uU][lL][tT][iI][pP][lL][yY]|[aA][dD][dD]|[dD][iI][vV][iI][dD][eE]|[sS][uU][bB][tT][rR][aA][cC][tT]' 
    ASSIGN_ERR=r'[aA][sS][sS][iI][gG][nN]'
    TO_ERR=r'[to][To][tO]'
    IS_ERR=r'[is][iS][Is]'
    VALUE_ERR=r'[vV][aA][lL][uU][eE]'
    IN_ERR=r'[in][iN][In]'
    VAR = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STOP = r'[.]'
    COMMA = r'[,]'

############################################
#Parser

    
#making game objects
game = Board()
gme = Game(game)
gme.start()


class parser_2048(Parser):
    tokens = lexer_2048.tokens
    def error(self, token):
        raise Exception 

    def __init__(self):
        self.env = { }
        
    @_('')
    def output(self, p):
        pass

    @_('OPERATION MOVEMENT') # without fullstop
    def output(self, p):
        print("You need to end a command with a full-stop.")
        return -1

    @_('OPERATION MOVEMENT STOP') # correct command
    def output(self, p):
        print("Thanks,move done,random tile added.")
        gme.movement(p[0], p[1])
        return 0

    @_('NUMBER COMMA NUMBER IS OPERATION STOP')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER COMMA NUMBER IS MOVEMENT STOP')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER COMMA NUMBER IS ASSIGN STOP')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER COMMA NUMBER IS TO STOP')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1

    @_('NUMBER COMMA NUMBER IS VALUE STOP')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER COMMA NUMBER IS IS STOP')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1

    @_('NUMBER COMMA NUMBER IS IN STOP')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1

    @_('ASSIGN NUMBER TO NUMBER COMMA NUMBER') 
    def output(self, p):
        print("You need to end a command with a full-stop.")
        return -1

    @_('ASSIGN NUMBER TO NUMBER COMMA NUMBER STOP') 
    def output(self, p):
        val=int(p[1])
        x=int(p[3])
        y=int(p[5])
        if(x>=1 and x<=4 and y>=1 and y<=4):
            print("Thanks, assignment done.")
            game.assignValue(int(p[1]), int(p[3])-1, int(p[5])-1)

            if(x==2048):
                return 1
            else:
                return 0
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1

    

    @_('OPERATION_ERR MOVEMENT_ERR STOP')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('OPERATION_ERR MOVEMENT STOP')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('OPERATION MOVEMENT_ERR STOP')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('ASSIGN NUMBER TO_ERR NUMBER COMMA NUMBER STOP')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('ASSIGN_ERR NUMBER TO_ERR NUMBER COMMA NUMBER STOP')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('ASSIGN_ERR NUMBER TO NUMBER COMMA NUMBER STOP')
    def output(self, p):
        print("Syntax Error")
        return -1
    
    @_('NUMBER COMMA NUMBER IS VAR') 
    def output(self, p):
        print("You need to end a command with a full-stop.")
        return -1


    @_('NUMBER COMMA NUMBER IS OPERATION_ERR STOP') # correct command
    def output(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=game.assignName(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:
                    print("Thanks, naming done.")
                    return 0
                elif flag==0:
                    print("Error. Tile Naming cannot be named")
                    return -1
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1




    @_('NUMBER COMMA NUMBER IS MOVEMENT_ERR STOP') # correct command
    def output(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=game.assignName(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:
                    print("Thanks, naming done.")
                    return 0
                elif flag==0:
                    print("Error. Tile Naming cannot be named")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1


    @_('NUMBER COMMA NUMBER IS ASSIGN_ERR STOP')# correct command
    def output(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=game.assignName(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:
                    print("Thanks, naming done.")
                    return 0
                elif flag==0:
                    print("Error. Tile Naming cannot be named")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1



    @_('NUMBER COMMA NUMBER IS TO_ERR STOP')# correct command
    def output(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=game.assignName(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:
                    print("Thanks, naming done.")
                    return 0
                elif flag==0:
                    print("Error. Tile Naming cannot be named")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1



    @_('NUMBER COMMA NUMBER IS IS_ERR STOP')# correct command
    def output(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=game.assignName(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:
                    print("Thanks, naming done.")
                    return 0
                elif flag==0:
                    print("Error. Tile Naming cannot be named")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1



    @_('NUMBER COMMA NUMBER IS VALUE_ERR STOP')# correct command
    def output(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=game.assignName(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:
                    print("Thanks, naming done.")
                    return 0
                elif flag==0:
                    print("Error. Tile Naming cannot be named")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1



    @_('NUMBER COMMA NUMBER IS IN_ERR STOP')# correct command
    def output(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=game.assignName(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:
                    print("Thanks, naming done.")
                    return 0
                elif flag==0:
                    print("Error. Tile Naming cannot be named")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1



    @_('NUMBER COMMA NUMBER IS VAR STOP')# correct command
    def output(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):
            if p[4]=="VAR": # check for "VAR" keyword
                print("NO, a keyword cannot be a variable name")
                return -1 
            else:

                flag=game.assignName(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:
                    print("Thanks, naming done.")
                    return 0
                elif flag==0:
                    print("Error. Tile Naming cannot be named")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1

    @_('NUMBER COMMA NUMBER IS_ERR VAR STOP')
    def output(self, p):
        print("Syntax Error")
        return -1



    @_('VALUE IN NUMBER COMMA NUMBER') # without fullstop
    def output(self, p):
        print("You need to end a command with a full-stop.")
        return -1






    @_('VALUE IN NUMBER COMMA NUMBER STOP') # correct command
    def output(self, p):
        if(int(p[2])>=1 and int(p[2])<=4 and int(p[4])>=1 and int(p[4])<=4):
            print("Value is:", end=' ')
            game.cellValue(int(p[2])-1,int(p[4])-1)
            return 0
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1

    @_('VALUE_ERR IN_ERR NUMBER COMMA NUMBER STOP')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('VALUE_ERR IN NUMBER COMMA NUMBER STOP')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('VALUE IN_ERR NUMBER COMMA NUMBER STOP')
    def output(self, p):
        print("Syntax Error")
        return -1


######################################
#main
def concat(X,Y):
    flattened_output = ""
    for i in range(4):
        for j in range(4):
            flattened_output+="{}".format(X[i][j])+" "
            
    for i in range(4):
        for j in range(4):
            if len(Y[i][j]) != 0:
                flattened_output+="{}".format(i+1) + "," + "{}".format(j+1)
                flag=0
                for name in Y[i][j]: 
                    if(flag==0):
                        flattened_output+=name
                    else:
                        flattened_output+=','+name
                    flag+=1
                flattened_output+=" "

    return flattened_output
    
if __name__ == '__main__':
    lexer = lexer_2048()
    parser = parser_2048()
    print("Hi, I am the 2048-game Engine.")
    print(concat(game.gridCell, game.tileName), file = sys.stderr)
    flag = 0
    while (flag!=1): 
        print('Please type a command.')
        text = input()
        try:
            flag = parser.parse(lexer.tokenize(text))
        except:
            print("Sorry, I don't understand that.")
            print("-1", file = sys.stderr)
            continue
            
        if(flag==1):
            print(concat(game.gridCell, game.tileName), file = sys.stderr)
            print("Congratulations.....You have won the game.")
            
        if(flag==-1):
            print("-1", file = sys.stderr)
        if(flag==0):
            print(concat(game.gridCell, game.tileName), file = sys.stderr)


        
        
    

    
    
