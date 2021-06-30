#2048
import random
import sys
from sly import Parser,Lexer

def printGrid():               
    for i in range(4):
        for j in range(4): 
            print(game.gridCell[i][j],end='  ')
        print()
        print()

class Board:
    def __init__(self):
        self.n=4
        self.gridCell=[[0]*4 for i in range(4)] 
        self.compress=False
        self.merge=False
        self.moved=False
        self.score=0
        self.tileName=[[[]]*4 for i in range(4)] 
                 
    def transpose(self):
        self.gridCell=[list(t)for t in zip(*self.gridCell)]
        self.tileName=[list(t)for t in zip(*self.tileName)]

    def reverse(self):
        for pos in range(4):
            i=0
            j=3
            while(i<j):
                self.gridCell[pos][i],self.gridCell[pos][j]=self.gridCell[pos][j],self.gridCell[pos][i]
                i+=1
                j-=1
        
        for pos in range(4):
            i=0
            j=3
            while(i<j):
                self.tileName[pos][i],self.tileName[pos][j]=self.tileName[pos][j],self.tileName[pos][i]
                i+=1
                j-=1
        
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

            
        
        
        
    def cellValue(self,x,y):
        print(self.gridCell[x][y])
        
    def assignValue(self,value,x,y):
        self.gridCell[x][y]=value 
        if value==0:
            self.tileName[x][y]=[] 
        printGrid()
        
         
                    
                    
class Game:
    def __init__(self,game):
        self.game=game
        self.end=False
        self.won=False
    
    def start(self):
        self.game.random_cell()
        self.game.random_cell()
        print("Game started... This is the initial state.")
        printGrid()  
    
    def movement(self,operation,direction): # to perform commands
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
                if(self.game.gridCell[i][j]==2048):
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
            print("You have lost. GAME OVER.........")
        if self.game.moved:
            self.game.random_cell()
        printGrid()



#####################################
        #Lexer 


class BasicLexer(Lexer):
    tokens = {VAR,NUMBER,operation,MOVEMENT,STOP,ASSIGN,TO,IS,VALUE,IN,operation_ERR,MOVEMENT_ERR,ASSIGN_ERR,IN_ERR,VALUE_ERR,IS_ERR,TO_ERR}
    ignore = '\t '
    literals = {','}


    #make the tokens lowercase, add another token stop and comma if possible.change the code on line 330
    
    # Regular expression rules for tokens
    
    #tokens_ERR is for error handling in tokens
    
  
    operation = r'ADD|SUBTRACT|DIVIDE|MULTIPLY'
    MOVEMENT = r'UP|DOWN|LEFT|RIGHT'
    STOP = r'.'
    operation_ERR=r'[mM][uU][lL][tT][iI][pP][lL][yY]|[aA][dD][dD]|[dD][iI][vV][iI][dD][eE]|[sS][uU][bB][tT][rR][aA][cC][tT]' 
    MOVEMENT_ERR=r'[lL][eE][fF][tT]|[uU][pP]|[dD][oO][wW][nN]|[rR][iI][gG][hH][tT]'
    ASSIGN = r'ASSIGN'
    ASSIGN_ERR=r'[aA][sS][sS][iI][gG][nN]'
    TO = r'TO'
    TO_ERR=r'[tT][oO]'
    IS = r'IS'
    IS_ERR=r'[iI][sS]'
    VALUE = r'VALUE'
    VALUE_ERR=r'[vV][aA][lL][uU][eE]'
    IN = r'IN'
    IN_ERR=r'[iI][nN]'
    VAR = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'



############################################
    #Parser

    
#making game objects
game = Board()
game2048 = Game(game)
game2048.start()


class BasicParser(Parser):
    tokens = BasicLexer.tokens
    
    def error(self, token):
        '''
        Default error handling function.  This may be subclassed.
        Over ride the sly error handler.
        '''
        
        raise Exception 

    def __init__(self):
        self.env = { }
        
    @_('')
    def output(self, p):
        pass

    
    


    @_('operation MOVEMENT') # without fullstop
    def output(self, p):
        print("You need to end a command with a full-stop.")
        return -1

    @_('operation MOVEMENT STOP') # correct command
    def output(self, p):
        print("Thanks,move done,random tile added.")
        game2048.movement(p[0], p[1])
        return 0


    @_('operation_ERR MOVEMENT_ERR STOP')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('operation_ERR MOVEMENT STOP')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('operation MOVEMENT_ERR STOP')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('ASSIGN NUMBER TO NUMBER "," NUMBER') # without fullstop
    def output(self, p):
        print("You need to end a command with a full-stop.")
        return -1



    @_('ASSIGN NUMBER TO NUMBER "," NUMBER "."') # correct command
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



    @_('ASSIGN NUMBER TO_ERR NUMBER "," NUMBER "."')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('ASSIGN_ERR NUMBER TO NUMBER "," NUMBER "."')
    def output(self, p):
        print("Syntax Error")
        return -1
    
    @_('ASSIGN_ERR NUMBER TO_ERR NUMBER "," NUMBER "."')
    def output(self, p):
        print("Syntax Error")
        return -1


    @_('NUMBER "," NUMBER IS VAR') # without fullstop
    def output(self, p):
        print("You need to end a command with a full-stop.")
        return -1

    @_('NUMBER "," NUMBER IS operation "."')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER "," NUMBER IS MOVEMENT "."')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER "," NUMBER IS ASSIGN "."')      //doubt
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER "," NUMBER IS TO "."')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER "," NUMBER IS IS "."')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1



    @_('NUMBER "," NUMBER IS VALUE "."')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1

    @_('NUMBER "," NUMBER IS IN "."')
    def output(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1

    @_('NUMBER "," NUMBER IS operation_ERR "."') # correct command
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




    @_('NUMBER "," NUMBER IS MOVEMENT_ERR "."') # correct command
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


    @_('NUMBER "," NUMBER IS ASSIGN_ERR "."')# correct command
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



    @_('NUMBER "," NUMBER IS TO_ERR "."')# correct command
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



    @_('NUMBER "," NUMBER IS IS_ERR "."')# correct command
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



    @_('NUMBER "," NUMBER IS VALUE_ERR "."')# correct command
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



    @_('NUMBER "," NUMBER IS IN_ERR "."')# correct command
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



    @_('NUMBER "," NUMBER IS VAR "."')# correct command
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

    @_('NUMBER "," NUMBER IS_ERR VAR "."')
    def output(self, p):
        print("Syntax Error")
        return -1


    @_('VALUE IN NUMBER "," NUMBER') # without fullstop
    def output(self, p):
        print("You need to end a command with a full-stop.")
        return -1


    @_('VALUE IN NUMBER "," NUMBER "."') # correct command
    def output(self, p):
        if(int(p[2])>=1 and int(p[2])<=4 and int(p[4])>=1 and int(p[4])<=4):
            print("Value is:", end=' ')
            game.cellValue(int(p[2])-1,int(p[4])-1)
            return 0
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1

    @_('VALUE_ERR IN_ERR NUMBER "," NUMBER "."')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('VALUE_ERR IN NUMBER "," NUMBER "."')
    def output(self, p):
        print("Syntax Error")
        return -1

    @_('VALUE IN_ERR NUMBER "," NUMBER "."')
    def output(self, p):
        print("Syntax Error")
        return -1


######################################
    #main





# to print to stderr
def print_to_stderr(*a):
    print(*a, file = sys.stderr)
    return


#returns string to be printed in stderr
def combine(Value,Names):
    s = ""
    for i in range(4):
        for j in range(4):
            s+=str(Value[i][j])
            s+=" "
            
    for i in range(4):
        for j in range(4):
            if len(Names[i][j]) != 0:
                s+=str(i+1)
                s+=","
                s+=str(j+1)
                a=0
                for name in Names[i][j]: 
                    if(a==0):
                        s+=name
                    else:
                        s+=','
                        s+=name
                    a=a+1
                s+=" "
    return s
    
if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    print("Hi, I am the 2048-game Engine.")
    print_to_stderr(combine(game.gridCell, game.tileName))
    won = 0
    while (won!=1): 
        print('Please type a command.')
        text = input()
        if text=="EXIT" or text=="exit": # Type EXIT or exit to stop running in between
            print("EXITING")
            break
        
        try:
            won = parser.parse(lexer.tokenize(text))
        except:
            print("Sorry I don't understand that.")
            print_to_stderr("-1")
            continue
            
        if(won==1):
            print_to_stderr(combine(game.gridCell, game.tileName))
            print("Game Won.... EXITING")
        if(won==-1):
            print_to_stderr("-1")
        if(won==0):
            print_to_stderr(combine(game.gridCell, game.tileName))


        
        
    

    
    
