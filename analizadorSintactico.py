from ply.yacc import yacc as yacc
import re
import codecs
import os
from sys import stdin
from analizadorLexico import tokens
from pip._vendor.distlib.compat import raw_input

precedence = (
	('right','ID','PRINCIPAL','IF'),
	('left','NEQUAL', 'EQUAL'),
	('left','LT','LTE','GT','GTE'),
	('left','PLUS','MINUS'),
	('left','TIMES','DIVIDE'),
	('left','LPARENTHESES','RPARENTHESES')	
)

def p_program(p):
    'program : block'
    print('program')
    #p[0] = program(p[1], 'program')

def p_block(p):
    'block : varDecl procDecl statement'
    print('block')

def p_varDecl(p):
    '''varDecl : SET ID COMMA BOOL SEMICOLON'''
    #p[0] = varDecl()
    print('varDeclBool')

#def p_varDecl2(p):
#    '''varDecl : SET ID COMMA NUMBER SEMICOLON'''
#    print('varDeclNumber')    

def p_varDeclEmpty(p):
    '''varDecl : empty'''
    print('nulo')

def p_procDecl(p):
    '''procDecl : procDecl PERCUTOR SEMICOLON'''
    print('procDecl5')

def p_procDecl2(p):
    '''procDecl : procDecl GOLPE SEMICOLON'''
    print('procDecl6')

def p_procDecl3(p):
    '''procDecl : procDecl VIBRATO SEMICOLON'''
    print('procDecl7')

def p_procDecl4(p):
    '''procDecl : procDecl METRONOMO SEMICOLON'''
    print('procDecl8')

def p_procDecl5(p):
    '''procDecl : procDecl PRINTLN LPARENTHESES print RPARENTHESES SEMICOLON'''
    print('procDecl9')

def p_procDecl6(p):
    '''procDecl : procDecl ENCASO sentenciaCondicional SINO block FINENCASO SEMICOLON'''
    print('procDecl10')

def p_procDecl7(p):
    '''procDecl : procDecl PRINCIPAL LPARENTHESES RPARENTHESES'''
    print('procDecl11')

def p_procDeclEmpty(p):
    '''procDecl : empty'''
    print('nulo')

def p_sentenciaCondicional(p):
    '''sentenciaCondicional : CUANDO statementSC ENTONS LBRACKET block RBRACKET'''
    print('sentenciaCondicional')

def p_statementSC(p):
    '''statementSC : IF condition'''

def p_sentenciaCondicionalEmpty(p):
    '''sentenciaCondicional : empty'''
    print('nulo')

def p_statement(p):
    '''statement : IF condition LBRACKET block RBRACKET SEMICOLON'''
    print('statement1')

def p_statement2(p):
    '''statement : FOR ID TO ID STEP NUMBER LBRACKET block RBRACKET SEMICOLON'''
    print('statement2')

def p_statement3(p):
    '''statement : FOR ID TO NUMBER STEP NUMBER LBRACKET block RBRACKET SEMICOLON'''
    print('statement3')

def p_statementEmpty(p):
    '''statement : empty'''
    print('nulo')

def p_condition(p):
    '''condition : expression relation expression'''
    print('condition1')

def p_condition2(p):
    '''condition : ID NEGATE'''
    print('condition2')

def p_condition3(p):
    '''condition : ID MTRUE'''
    print('condition3')

def p_condition4(p):
    '''condition : ID MFALSE'''
    print('condition4')

def p_relation(p):
    '''relation : EQUAL'''
    print('relation1')

def p_relation2(p):
    '''relation : NEQUAL'''
    print('relation2')

def p_relation3(p):
    '''relation : LT'''
    print('relation3')

def p_relation4(p):
    '''relation : GT'''
    print('relation4')

def p_relation5(p):
    '''relation : LTE'''
    print('relation5')

def p_relation6(p):
    '''relation : GTE'''
    print('relation6')

def p_expression(p):
    '''expression : term'''
    print('expression1')

def p_expression2(p):
    '''expression : addingOperator term'''
    print('expression2')

def p_expression3(p):
    '''expression : expression addingOperator term'''
    print('expression3')

def p_addingOperator(p):
    '''addingOperator : PLUS'''
    print("addingOperator1")

def p_addingOperator2(p):
    '''addingOperator : MINUS'''
    print("addingOperator2")

def p_term(p):
    '''term : factor'''
    print('term1')

def p_term2(p):
    '''term : term multiplyingOperator factor'''
    print('term2')

def p_multiplyingOperator(p):
    '''multiplyingOperator : TIMES'''
    print('multiplyingOperator1')

def p_multiplyingOperator2(p):
    '''multiplyingOperator : DIVIDE'''
    print('multiplyingOperator2')

def p_multiplyingOperator3(p):
    '''multiplyingOperator : EXPONENT'''
    print('multiplyingOperator2')

def p_multiplyingOperator4(p):
    '''multiplyingOperator : WDIVIDE'''
    print('multiplyingOperator3')

def p_multiplyingOperator5(p):
    '''multiplyingOperator : MODULE'''
    print('multiplyingOperator4')

def p_factor(p):
    '''factor : ID'''
    print('factor1')

def p_factor2(p):
    '''factor : NUMBER'''
    print('factor2')

def p_factor3(p):
    '''factor : LPARENTHESES expression RPARENTHESES'''
    print('factor3')

def p_print(p):
    '''print : STRING'''
    print('print1')

def p_print2(p):
    '''print : factor'''
    print('print2')

def p_parameters(p):
    '''parameters : factor'''
    print('parameters')

def p_parameters2(p):
    '''parameters : BOOL'''
    print('parameters2')

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print('Error de sintaxis ', p)#, 'en la linea ' + str(p.lineno))

def buscarFicheros(directorio):
    ficheros = []
    numArchivo = ''
    respuesta = False
    cont = 1

    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)

    for file in files:
        print(str(cont) + ". " + file)
        cont = cont + 1

    while respuesta == False:
        numArchivo = raw_input('\nNumero del test: ')
        for file in files:
            if file == files[int(numArchivo) - 1]:
                respuesta = True
                break

    print("Has escogido \"%s\" \n" % files[int(numArchivo) - 1])

    return files[int(numArchivo) - 1]

directorio = "/home/kash/Documents/GitHub/Tambarduine/Pruebas/"
archivo = buscarFicheros(directorio)
test = directorio + archivo
fp = codecs.open(test, "r", "utf-8")
cadena = fp.read()
fp.close()

parser = yacc()
result = parser.parse(cadena)

print (result)