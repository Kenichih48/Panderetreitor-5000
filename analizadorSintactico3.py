from ply.yacc import yacc
import re
import codecs
import os
from sys import stdin
from analizadorLexico import tokens
from pip._vendor.distlib.compat import raw_input

precedence = (
   ('right','ID','IF'),
   ('right','DEF', 'EXEC'),
   ('right', 'SET'),
   ('left','NEQUAL','EQUAL'),
   ('left','LT','LTE','GT','GTE'),
   ('left','PLUS','MINUS'),
   ('left','TIMES','DIVIDE','WDIVIDE'),
   ('left', 'MODULE'),
   ('left','EXPONENT'),
   ('left','LPARENTHESES','RPARENTHESES'),
   )

def p_program(p):
	'''program : block'''
	print ("program")

def p_block(p):
	'''block : varDecl moveDecl procDecl statement'''
	print ("block")

def p_varDecl1(p):
    '''varDecl : varDeclList SEMICOLON'''
    print ("varDecl 1")

def p_varDeclEmpty(p):
	'''varDecl : empty'''
	print ("nulo")

def p_varDeclSt1(p):
	'''varDeclSt : SET ID COMMA BOOL'''
	print ("varDeclSt 1")

def p_varDeclSt2(p):
	'''varDeclSt : SET ID COMMA NUMBER'''
	print ("varDeclSt 2")

def p_varDeclSt3(p):
    '''varDeclSt : SET ID COMMA arithOperation'''
    print ("varDeclSt 3")

def p_varDeclSt4(p):
    '''varDeclSt : SET ID boolOperation'''
    print ("varDeclSt 4")

def p_varDeclList1(p):
    '''varDeclList : varDeclSt'''
    print ("varDeclList 1")

def p_varDeclList2(p):
    '''varDeclList : varDeclList SEMICOLON varDeclSt'''
    print ("varDeclList 2")

def p_arithOper1(p):
    '''arithOperation : factor addingOperator factor'''
    print('arithOper 1')

def p_arithOper2(p):
    '''arithOper : factor multiplyingOperator factor'''
    print('arithOper 2')

def p_arithOper3(p):
    '''arithOper : factor MODULE factor'''
    print('arithOper 3')

def p_arithOper4(p):
    '''arithOper : factor EXPONENT factor'''
    print('arithOper 4')

def p_arithOper5(p):
    '''arithOper : MINUS factor'''
    print('arithOper 5')

def p_boolOper1(p):
    '''boolOperation : NEGATE'''
    print('boolOper 1')

def p_boolOper2(p):
    '''boolOperation : MTRUE'''
    print('boolOper 2')

def p_boolOper3(p):
    '''boolOperation : MFALSE'''
    print('boolOper 3')

def p_moveDecl1(p):
    '''moveDecl : moveDeclList SEMICOLON'''
    print('moveDecl 1')

def p_moveDeclEmpty(p):
	'''moveDecl : empty'''
	print ("nulo")

def p_moveDeclList1(p):
    '''moveDeclList : moveDeclSt'''
    print('moveDeclList 1')

def p_moveDeclList2(p):
    '''moveDeclList : moveDeclList SEMICOLON moveDeclSt'''
    print('moveDeclList 2')

def p_moveDeclSt1(p):
    '''moveDeclSt : ABANICO'''
    print('moveDeclSt 1')

def p_moveDeclSt2(p):
    '''moveDeclSt : VERTICAL'''
    print('moveDeclSt 2')

def p_moveDeclSt3(p):
    '''moveDeclSt : PERCUTOR'''
    print('moveDeclSt 3')

def p_moveDeclSt4(p):
    '''moveDeclSt : GOLPE'''
    print('moveDeclSt 4')

def p_moveDeclSt5(p):
    '''moveDeclSt : VIBRATO'''
    print('moveDeclSt 5')

def p_moveDeclSt6(p):
    '''moveDeclSt : METRONOMO'''
    print('moveDeclSt 6')

def p_procDecl1(p):
	'''procDecl : procDecl PRINTLN LPARENTHESES toPrint RPARENTHESES SEMICOLON'''
	print ("procDecl 1")

def p_procDecl2(p):
	'''procDecl : procDecl IF condition LBRACKET block RBRACKET SEMICOLON'''
	print ("procDecl 2")

def p_procDeclEmpty(p):
	'''procDecl : empty'''
	print ("nulo")

def p_toPrint1(p):
    '''toPrint : toPrintList'''
    print('toPrint 1')

def p_toPrintList1(p):
    '''toPrintList : toPrintSt'''
    print('toPrintList 1')

def p_toPrintList1(p):
    '''toPrintList : toPrintList COMMA toPrintSt'''
    print('toPrintList 2')

def p_toPrintSt1(p):
    '''toPrintSt : STRING'''
    print('toPrintSt 1')

def p_toPrintSt2(p):
    '''toPrintSt : factor'''
    print('toPrintSt 2')

def p_toPrintSt3(p):
    '''toPrintSt : arithOperation'''
    print('toPrintSt 3')

#def p_statement1(p):
#	'''statement : ID UPDATE expression'''
#	print ("statement 1")

#def p_statement2(p):
#	'''statement : CALL ID'''
#	print ("statement 2")

#def p_statement3(p):
#	'''statement : BEGIN statementList END'''
#	print ("statement 3")

def p_statement1(p):
	'''statement : IF condition LBRACKET block RBRACKET'''
	print ("statement 4")

#def p_statement5(p):
#	'''statement : WHILE condition DO statement'''
#	print ("statement 5")

def p_statementEmpty(p):
	'''statement : empty'''
	print ("nulo")

def p_statementList1(p):
	'''statementList : statement'''
	print ("statementList 1")

def p_statementList2(p):
	'''statementList : statementList SEMICOLON statement SEMICOLON'''
	print ("statementList 2")

#def p_condition1(p):
#	'''condition : ODD expression'''
#	print ("condition 1")

def p_condition1(p):
	'''condition : expression relation expression'''
	print ("condition 1")

def p_relation1(p):
	'''relation : EQUAL'''
	print ("relation 1")

def p_relation2(p):
	'''relation : NEQUAL'''
	print ("relation 2")

def p_relation3(p):
	'''relation : LT'''
	print ("relation 3")

def p_relation4(p):
	'''relation : GT'''
	print ("relation 4")

def p_relation5(p):
	'''relation : LTE'''
	print ("relation 5")

def p_relation6(p):
	'''relation : GTE'''
	print ("relation 6")

def p_addingOperator1(p):
	'''addingOperator : PLUS'''
	print ("addingOperator 1")

def p_addingOperator2(p):
	'''addingOperator : MINUS'''
	print ("addingOperator 1")

def p_multiplyingOperator1(p):
	'''multiplyingOperator : TIMES'''
	print ("multiplyingOperator 1")

def p_multiplyingOperator2(p):
	'''multiplyingOperator : DIVIDE'''
	print ("multiplyingOperator 2")

def p_multiplyingOperator3(p):
    '''multiplyingOperator : WDIVIDE'''
    print ("multiplyingOperator 3")

def p_factor1(p):
	'''factor : ID'''
	print ("factor 1")

def p_factor2(p):
	'''factor : NUMBER'''
	print ("factor 2")

def p_factor3(p):
	'''factor : LPARENTHESES arithOperation RPARENTHESES'''
	print ("factor 3")

def p_empty(p):
	'''empty :'''
	pass

def p_error(p):
	print ("Error de sintaxis ", p)
	#print ("Error en la linea "+str(p.lineno)

def buscarFicheros(directorio):
	ficheros = []
	numArchivo = ''
	respuesta = False
	cont = 1

	for base, dirs, files in os.walk(directorio):
		ficheros.append(files)

	for file in files:
		print (str(cont)+". "+file)
		cont = cont+1

	while respuesta == False:
		numArchivo = raw_input('\nNumero del test: ')
		for file in files:
			if file == files[int(numArchivo)-1]:
				respuesta = True
				break

	print ("Has escogido \"%s\" \n" %files[int(numArchivo)-1])

	return files[int(numArchivo)-1]

directorio = '/home/kash/Documents/GitHub/Tambarduine/Pruebas/'
archivo = buscarFicheros(directorio)
test = directorio+archivo
fp = codecs.open(test,"r","utf-8")
cadena = fp.read()
fp.close()

parser = yacc()
result = parser.parse(cadena)

print (result)