#import ply.yacc as yacc
from ply.yacc import yacc
import re
import codecs
import os
from sys import stdin
from analizadorLexico import tokens
from pip._vendor.distlib.compat import raw_input

nombres = {}

precedence = (
   ('right','ID','IF'),
   ('right','DEF', 'EXEC'),
   ('right', 'SET'),
   ('left','NEQUAL','EQUAL'),
   ('left','LT','LTE','GT','GTE'),
   ('left','PLUS','MINUS'),
   ('left','TIMES','DIVIDE','WDIVIDE'),
   ('left','EXPONENT'),
   ('left','LPARENTHENSES','RPARENTHESES'),
   )

def p_bloques(t):
    '''bloques : declaracion
                | procedimiento
    '''
    print('bloque')

def p_declaracion_variables(t):
    '''declaracion : SET ID COMMA expresion SEMICOLON
                    | SET ID COMMA expresionB SEMICOLON
    '''
    #seguir = True
    #if  not(bool(nombres)):
    #    if t[4] == ("True" or "False"):
    #        nombres[t[2]] = [t[4],'bool']
    #    else:
    #        nombres[t[2]] = [t[4],'num']
    #else:
    #    for key, value in nombres.items():
    #        if key == t[2]:
    #            if t[4] != ("True" and "False") and value[1] == 'bool':
    #                print("Variable {} is boolean and new value is a number".format(t[2]))
    #                seguir = False
    #                pass
    #            elif value[1] == 'num':
    #                try:
    #                    int(t[4])
    #                except:
    #                    print("Variable {} is a number and new value is boolean".format(t[2]))
    #                    seguir = False
    #                    pass
    #                else:
    #                    pass
    #
    #    if t[4] == ("True" and "False") and seguir:
    #        nombres[t[2]] = [t[4],'bool']
    #        pass
    #    elif seguir:
    #        nombres[t[2]] = [t[4],'num']
    #        pass
    print('declaracion')
    #print(nombres)

def p_procedimientos(t):
    '''procedimiento : sentencia
                        | movimientos
                        | operBool
                        | creacionRutinas
                        | correrRutinas
    '''
    print('procedimientos')

def p_creacion_rutinas(t):
    '''creacionRutinas : DEF ID LPARENTHESES RPARENTHESES LBRACKET bloques RBRACKET SEMICOLON
                        | DEF ID LPARENTHESES expresion RPARENTHESES LBRACKET bloques RBRACKET SEMICOLON
                        | DEF ID LPARENTHESES listExpresion RPARENTHESES LBRACKET bloques RBRACKET SEMICOLON
    '''
    print('creacion rutinas')

def p_correr_rutinas(t):
    '''correrRutinas : EXEC ID LPARENTHESES RPARENTHESES LBRACKET SEMICOLON
                        | EXEC ID LPARENTHESES expresion RPARENTHESES SEMICOLON
                        | EXEC ID LPARENTHESES listExpresion RPARENTHESES SEMICOLON
    '''
    print('correr rutinas')

def p_sentencias(t):
    '''sentencia : FOR ID TO expresion STEP expresion LBRACKET bloques RBRACKET SEMICOLON
                    | FOR ID TO ID STEP expresion LBRACKET bloques RBRACKET SEMICOLON
    '''
    #if  not(bool(nombres)):
    #    nombres[t[2]] = [1,'num']
    #else:
    #    for key in nombres.keys():
    #        if key == t[2]:
    #            break
    #    else:
    #        nombres[t[2]] = [1,'num']

    #for key, value in nombres.items():
    #    for key2, value2 in nombres.items():
    #        if key == t[2] and value[1] == 'num' and key2 != t[4]:
    #            for x in range(value[0],int(t[4]) + 1,int(t[6])):
    #                print(x)
    #            break
    #        elif key == t[2] and key2 == t[4] and value[1] == 'num' and value2[1] == 'num':
    #            for x in range(value[0], value2[0] + 1, int(t[6])):
    #                print(x)
    #            break
    #        elif (key == t[2] and value[1] == 'bool') or (key2 == t[4] and value2[1] == 'bool'):
    #            print('A variable used is not a number')#.format(t.lineno))
    #            break
    print('sentencia For')
        
def p_sentencia2(t):
    'sentencia : IF condicion LBRACKET declaracion RBRACKET SEMICOLON'
    #if t[2] == True:
    #    print('True, can run block')
    #else:
    #    print('False, can\'t run block')
    print('sentencia If')

def p_condiciones(t):
    '''
    condicion : expresion LT expresion
                | expresion GT expresion
                | expresion LTE expresion
                | expresion GTE expresion
                | expresion EQUAL expresion
                | expresion NEQUAL expresion
    '''
    #if t[2] == "<": t[0] = t[1] < t[3]
    #elif t[2] == ">": t[0] = t[1] > t[3]
    #elif t[2] == "<=": t[0] = t[1] <= t[3]
    #elif t[2] == ">=": t[0] = t[1] >= t[3]
    #elif t[2] == "==": t[0] = t[1] is t[3]
    #elif t[2] == "!=": t[0] = t[1] != t[3]

def p_expresion_operaciones(t):
    '''
    expresion : expresion PLUS expresion
                | expresion MINUS expresion
                | expresion TIMES expresion
                | expresion DIVIDE expresion
                | expresion EXPONENT expresion
                | expresion MODULE expresion
                | expresion WDIVIDE expresion
    '''
    if t[2] == '+': t[0] = t[1]+t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]
    elif t[2] == '%': t[0] = t[1] % t[3]
    elif t[2] == '//': t[0] == t[1] // t[3]
    elif t[2] == '**':
        i = t[3]
        t[0] = t[1]
        while i > 1:
            t[0] *= t[1]
            i -= 1
    
#def p_expresion_uminus(t):
#    'expresion : MINUS expresion'
#    t[0] = -t[2]

def p_list_expresiones(t):
    '''listExpresion : expresion COMMA expresion
                        | listExpresion COMMA expresion
    '''

def p_expresion_operaciones_booleanas(t):
    'operBool : SET ID NEGATE SEMICOLON'
    #for key, value in nombres.items():
    #    if key == t[2] and value[1] != 'bool':
    #        print('Las operaciones booleanas no pueden usarse en numeros')
    #    elif key != t[2]:
    #        print('La variable por negar no existe')
    #    elif key == t[2] and value[0] == 'True':
    #        value[0] = 'False'
    #    elif key == t[2] and value[0] == 'False':
    #        value[0] = 'True'
    #print(nombres)
    print('OperBool Negate')

def p_expresion_operaciones_booleanas2(t):
    'operBool : SET ID MTRUE SEMICOLON'
    #for key, value in nombres.items():
    #    if key == t[2] and value[1] != 'bool':
    #        print('Las operaciones booleanas no pueden usarse en numeros')
    #    elif key != t[2]:
    #        print('La variable por negar no existe')
    #    elif key == t[2] and value[0] == 'True':
    #        pass
    #    elif key == t[2] and value[0] == 'False':
    #        value[0] = 'True'
    #print(nombres)
    print('Make True')

def p_expresion_operaciones_booleanas3(t):
    'operBool : SET ID MFALSE SEMICOLON'
    #for key, value in nombres.items():
    #    if key == t[2] and value[1] != 'bool':
    #        print('Las operaciones booleanas no pueden usarse en numeros')
    #    elif key != t[2]:
    #        print('La variable por negar no existe')
    #    elif key == t[2] and value[0] == 'True':
    #       value[0] = 'False'
    #    elif key == t[2] and value[0] == 'False':
    #        pass
    #print(nombres)
    print('Make False')

def p_expresion_movimientos(t):
    '''movimientos : ABANICO SEMICOLON
                    | VERTICAL SEMICOLON
                    | PERCUTOR SEMICOLON
                    | GOLPE SEMICOLON
                    | VIBRATO SEMICOLON
                    | METRONOMO SEMICOLON
    '''
    print('movimientos')

def p_expresion_numero(t):
    'expresion : NUMBER'
    t[0] = t[1]

#def p_expresion_numero2(t):
#    'expresion : LPARENTHESES expresion RPARENTHESES'

def p_expresion_bool(t):
    'expresionB : BOOL'
    t[0] = t[1]

def p_expresion_nombre(t):
    'expresion : ID'
    #try:
    #    t[0] = nombres[t[1]]
    #except LookupError:
    #    print('Nombre desconocido', t[1])
    #    t[0] = 0

def p_error(p):
    if p:
        print('Error de sintaxis ', p.type)#, 'en la linea ' + str(p.lineno))
        #parser.errork()
    else:
        print('Syntax error at EOF')
    

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
print()

parser = yacc()
result = parser.parse(cadena)
print (result)