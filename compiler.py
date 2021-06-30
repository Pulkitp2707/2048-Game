#####################################
        #Lexer 
from game import *
class BasicLexer(Lexer):
    tokens = {VAR,NUMBER,OPERATION,DIRECTION,ASSIGN,TO,IS,VALUE,IN,OPERATION_ERR,DIRECTION_ERR,ASSIGN_ERR,IN_ERR,VALUE_ERR,IS_ERR,TO_ERR}
    ignore = '\t '
    literals = {'.',','}
    
    # Regular expression rules for tokens
    
    #tokens_ERR is for error handling in tokens
    
  
    OPERATION = r'ADD|SUBTRACT|MULTIPLY|DIVIDE'
    DIRECTION = r'LEFT|RIGHT|UP|DOWN'
    OPERATION_ERR=r'[aA][dD][dD]|[sS][uU][bB][tT][rR][aA][cC][tT]|[mM][uU][lL][tT][iI][pP][lL][yY]|[dD][iI][vV][iI][dD][eE]' 
    DIRECTION_ERR=r'[lL][eE][fF][tT]|[rR][iI][gG][hH][tT]|[uU][pP]|[dD][oO][wW][nN]'
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
gamepanel = Board()
game2048 = Game(gamepanel)
game2048.start()


class BasicParser(Parser):
    tokens = BasicLexer.tokens
    
    def error(self, token):
        '''
        Default error handling function.  This may be subclassed.
        Over ride the sly error handler.
        '''
        
        raise Exception #raising an exception to be caught by the error handler... It detects all commnads not in grammer

    def __init__(self):
        self.env = { }
        
    @_('')
    def statement(self, p):
        pass

    
    


    @_('OPERATION DIRECTION') # without fullstop
    def statement(self, p):
        print("You need to end a command with a full-stop.")
        return -1

    @_('OPERATION DIRECTION "."') # correct command
    def statement(self, p):
        print("Thanks,move done,random tile added.")
        game2048.link_keys(p[0], p[1])
        return 0


    @_('OPERATION_ERR DIRECTION_ERR "."')
    def statement(self, p):
        print("Syntax Error")
        return -1

    @_('OPERATION_ERR DIRECTION "."')
    def statement(self, p):
        print("Syntax Error")
        return -1

    @_('OPERATION DIRECTION_ERR "."')
    def statement(self, p):
        print("Syntax Error")
        return -1

    @_('ASSIGN NUMBER TO NUMBER "," NUMBER') # without fullstop
    def statement(self, p):
        print("You need to end a command with a full-stop.")
        return -1



    @_('ASSIGN NUMBER TO NUMBER "," NUMBER "."') # correct command
    def statement(self, p):
        if(int(p[3])>=1 and int(p[3])<=4 and int(p[5])>=1 and int(p[5])<=4):
            print("Thanks, assignment done.")
            gamepanel.valueAssign(int(p[1]), int(p[3])-1, int(p[5])-1)

            if(int(p[1])==2048):
                return 1
            else:
                return 0
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1



    @_('ASSIGN NUMBER TO_ERR NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Syntax Error")
        return -1

    @_('ASSIGN_ERR NUMBER TO NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Syntax Error")
        return -1
    
    @_('ASSIGN_ERR NUMBER TO_ERR NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Syntax Error")
        return -1


    @_('NUMBER "," NUMBER IS VAR') # without fullstop
    def statement(self, p):
        print("You need to end a command with a full-stop.")
        return -1

    @_('NUMBER "," NUMBER IS OPERATION "."')
    def statement(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER "," NUMBER IS DIRECTION "."')
    def statement(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER "," NUMBER IS ASSIGN "."')
    def statement(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER "," NUMBER IS TO "."')
    def statement(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1


    @_('NUMBER "," NUMBER IS IS "."')
    def statement(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1



    @_('NUMBER "," NUMBER IS VALUE "."')
    def statement(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1

    @_('NUMBER "," NUMBER IS IN "."')
    def statement(self, p):
        print("NO, a keyword cannot be a variable name")
        return -1

    @_('NUMBER "," NUMBER IS OPERATION_ERR "."') # correct command
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=gamepanel.nameAssign(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:

                    print("Thanks, naming done.")

                    return 0
                elif flag==0:
                    print("Sorry the tile mentioned is empty and cannot be named")
                    return -1
                elif flag==-1:
                    print("Sorry the name mentioned already exists")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1




    @_('NUMBER "," NUMBER IS DIRECTION_ERR "."') # correct command
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=gamepanel.nameAssign(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:

                    print("Thanks, naming done.")

                    return 0
                elif flag==0:
                    print("Sorry the tile mentioned is empty and cannot be named")
                    return -1
                elif flag==-1:
                    print("Sorry the name mentioned already exists")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1


    @_('NUMBER "," NUMBER IS ASSIGN_ERR "."')# correct command
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=gamepanel.nameAssign(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:

                    print("Thanks, naming done.")

                    return 0
                elif flag==0:
                    print("Sorry the tile mentioned is empty and cannot be named")
                    return -1
                elif flag==-1:
                    print("Sorry the name mentioned already exists")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1



    @_('NUMBER "," NUMBER IS TO_ERR "."')# correct command
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=gamepanel.nameAssign(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:

                    print("Thanks, naming done.")

                    return 0
                elif flag==0:
                    print("Sorry the tile mentioned is empty and cannot be named")
                    return -1
                elif flag==-1:
                    print("Sorry the name mentioned already exists")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1



    @_('NUMBER "," NUMBER IS IS_ERR "."')# correct command
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=gamepanel.nameAssign(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:

                    print("Thanks, naming done.")

                    return 0
                elif flag==0:
                    print("Sorry the tile mentioned is empty and cannot be named")
                    return -1
                elif flag==-1:
                    print("Sorry the name mentioned already exists")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1



    @_('NUMBER "," NUMBER IS VALUE_ERR "."')# correct command
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=gamepanel.nameAssign(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:

                    print("Thanks, naming done.")

                    return 0
                elif flag==0:
                    print("Sorry the tile mentioned is empty and cannot be named")
                    return -1
                elif flag==-1:
                    print("Sorry the name mentioned already exists")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1



    @_('NUMBER "," NUMBER IS IN_ERR "."')# correct command
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):

                flag=gamepanel.nameAssign(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:

                    print("Thanks, naming done.")

                    return 0
                elif flag==0:
                    print("Sorry the tile mentioned is empty and cannot be named")
                    return -1
                elif flag==-1:
                    print("Sorry the name mentioned already exists")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1



    @_('NUMBER "," NUMBER IS VAR "."')# correct command
    def statement(self, p):
        if(int(p[0])>=1 and int(p[0])<=4 and int(p[2])>=1 and int(p[2])<=4):
            if p[4]=="VAR": # check for "VAR" keyword
                print("NO, a keyword cannot be a variable name")
                return -1 
            else:

                flag=gamepanel.nameAssign(p[4],int(p[0])-1,int(p[2])-1)
                if flag==1:

                    print("Thanks, naming done.")

                    return 0
                elif flag==0:
                    print("Sorry the tile mentioned is empty and cannot be named")
                    return -1
                elif flag==-1:
                    print("Sorry the name mentioned already exists")
                    return -1


        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1

    @_('NUMBER "," NUMBER IS_ERR VAR "."')
    def statement(self, p):
        print("Syntax Error")
        return -1



    @_('VALUE IN NUMBER "," NUMBER') # without fullstop
    def statement(self, p):
        print("You need to end a command with a full-stop.")
        return -1






    @_('VALUE IN NUMBER "," NUMBER "."') # correct command
    def statement(self, p):
        if(int(p[2])>=1 and int(p[2])<=4 and int(p[4])>=1 and int(p[4])<=4):
            print("Value is:", end=' ')
            gamepanel.valueIn(int(p[2])-1,int(p[4])-1)
            return 0
        else:
            print("There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            return -1

    @_('VALUE_ERR IN_ERR NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Syntax Error")
        return -1

    @_('VALUE_ERR IN NUMBER "," NUMBER "."')
    def statement(self, p):
        print("Syntax Error")
        return -1

    @_('VALUE IN_ERR NUMBER "," NUMBER "."')
    def statement(self, p):
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
    print_to_stderr(combine(gamepanel.gridCell, gamepanel.gridVar))
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
            print_to_stderr(combine(gamepanel.gridCell, gamepanel.gridVar))
            print("Game Won.... EXITING")
        if(won==-1):
            print_to_stderr("-1")
        if(won==0):
            print_to_stderr(combine(gamepanel.gridCell, gamepanel.gridVar))
