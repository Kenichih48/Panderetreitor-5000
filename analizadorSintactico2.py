from ply.yacc import yacc as yacc
import re
import codecs
import os
from sys import stdin
from analizadorLexico2 import tokens
from analizadorLexico2 import analizador
from pip._vendor.distlib.compat import raw_input

resultado_gramatica = []

#precedence = (
#    ('left','PLUS', 'MINUS')
#    ('left', 'TIMES', 'DIVIDE')
#     ('right', 'UMINUS')
#)

nombres = {}
rutinas = {}

def p_bloques(t):
    '''bloques : declaracion
                | movimientos
                | operBool
                | sentencia
    '''
    print('bloque')

def p_declaracion_variables(t):
    '''declaracion : SET ID COMMA expresion SEMICOLON
                    | SET ID COMMA expresionB SEMICOLON
    '''
    seguir = True
    if  not(bool(nombres)):
        if t[4] == ("True" or "False"):
            nombres[t[2]] = [t[4],'bool']
        else:
            nombres[t[2]] = [t[4],'num']
    else:
        for key, value in nombres.items():
            if key == t[2]:
                if t[4] != ("True" and "False") and value[1] == 'bool':
                    print("Variable {} is boolean and new value is a number".format(t[2]))
                    seguir = False
                    pass
                elif value[1] == 'num':
                    try:
                        int(t[4])
                    except:
                        print("Variable {} is a number and new value is boolean".format(t[2]))
                        seguir = False
                        pass
                    else:
                        pass

        if t[4] == ("True" and "False") and seguir:
            nombres[t[2]] = [t[4],'bool']
            pass
        elif seguir:
            nombres[t[2]] = [t[4],'num']
            pass
    print(nombres)

def p_sentencias(t):
    '''sentencia : FOR ID TO expresion STEP expresion LBRACKET RBRACKET SEMICOLON
                    | FOR ID TO ID STEP expresion LBRACKET RBRACKET SEMICOLON
    '''
    print(t[2])
    print(t[4])
    print(t[6])
    for key, value in nombres.items():
        for key2, value2 in nombres.items():
            print(key, key2)
            print(value, value2)
            if key == t[2] and value[1] == 'num' and key2 != t[4]:
                for x in range(value[0],int(t[4]) + 1,int(t[6])):
                    print(x)
            elif key == t[2] and key2 == t[4] and value[1] == 'num' and value2[1] == 'num':
                for x in range(value[0], value2[0], int(t[6])):
                    print(x)
            elif key2 == t[2] and key == t[4] and value[1] == 'num' and value2[1] == 'num':
                for x in range(value2[0], value[0], int(t[6])):
                    print(x)
            else:
                print('A variable used is not a number')#.format(t.lineno))
                pass
            #elif (key == t[2] or key2 == t[2]) and 
    print('sentencia For')
        
def p_sentencia2(t):
    'sentencia : IF condicion LBRACKET RBRACKET SEMICOLON'
    print(t)
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
    if t[2] == "<": t[0] = t[1] < t[3]
    elif t[2] == ">": t[0] = t[1] > t[3]
    elif t[2] == "<=": t[0] = t[1] <= t[3]
    elif t[2] == ">=": t[0] = t[1] >= t[3]
    elif t[2] == "==": t[0] = t[1] is t[3]
    elif t[2] == "!=": t[0] = t[1] != t[3]

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
    
def p_expresion_uminus(t):
    'expresion : MINUS expresion'
    t[0] = -t[2]

def p_expresion_operaciones_booleanas(t):
    'operBool : SET ID NEGATE SEMICOLON'
    for key, value in nombres.items():
        if key == t[2] and value[1] != 'bool':
            print('Las operaciones booleanas no pueden usarse en numeros')
        elif key != t[2]:
            print('La variable por negar no existe')
        elif key == t[2] and value[0] == 'True':
            value[0] = 'False'
        elif key == t[2] and value[0] == 'False':
            value[0] = 'True'
    print(nombres)

def p_expresion_operaciones_booleanas2(t):
    'operBool : SET ID MTRUE SEMICOLON'
    for key, value in nombres.items():
        if key == t[2] and value[1] != 'bool':
            print('Las operaciones booleanas no pueden usarse en numeros')
        elif key != t[2]:
            print('La variable por negar no existe')
        elif key == t[2] and value[0] == 'True':
            pass
        elif key == t[2] and value[0] == 'False':
            value[0] = 'True'
    print(nombres)

def p_expresion_operaciones_booleanas3(t):
    'operBool : SET ID MFALSE SEMICOLON'
    for key, value in nombres.items():
        if key == t[2] and value[1] != 'bool':
            print('Las operaciones booleanas no pueden usarse en numeros')
        elif key != t[2]:
            print('La variable por negar no existe')
        elif key == t[2] and value[0] == 'True':
            value[0] = 'False'
        elif key == t[2] and value[0] == 'False':
            pass
    print(nombres)

def p_expresion_movimientos(t):
    '''movimientos : ABANICO SEMICOLON
                    | VERTICAL SEMICOLON
                    | PERCUTOR SEMICOLON
                    | GOLPE SEMICOLON
                    | VIBRATO SEMICOLON
                    | METRONOMO SEMICOLON
    '''
    print('movimientos')

#def p_expresion_parametrosP(t):
#    '''parametrosP : STRING
#                    | expresion
#    '''
#    print(t[0])

def p_expresion_numero(t):
    'expresion : NUMBER'
    t[0] = t[1]

def p_expresion_numero2(t):
    'expresion : LPARENTHESES expresion RPARENTHESES'

def p_expresion_bool(t):
    'expresionB : BOOL'
    t[0] = t[1]

def p_expresion_nombre(t):
    'expresion : ID'
    try:
        t[0] = nombres[t[1]]
    except LookupError:
        print('Nombre desconocido', t[1])
        t[0] = 0

def p_error(t):
    global resultado_gramatica
    print(t)
    if t:
        resultado = "Error sintactico de tipo {} en el valor {}".format(str(t.type),str(t.value))
    else:
        resultado = "Error sintactico {}".format(t)
        print(resultado)
    resultado_gramatica.append(resultado)

parser = yacc()

def prueba_sintactica(data):
    global resultado_gramatica
    resultado_gramatica.clear()

    for item in data.splitlines():
        if item:
            gram = parser.parse(item)
            if gram:
                resultado_gramatica.append(str(gram))
        else: print("data vacia")

    print("result: ", resultado_gramatica)
    return resultado_gramatica

if __name__ == '__main__':
    while True:
        try:
            s = input(' ingresa dato >>> ')
        except EOFError:
            continue
        if not s: continue

        # gram = parser.parse(s)
        # print("Resultado ", gram)

        prueba_sintactica(s)