#Lexer 

from sly import Lexer
import sys
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