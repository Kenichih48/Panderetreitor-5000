from ply.lex import lex as lex
import re
import codecs
import os
import sys
from pip._vendor.distlib.compat import raw_input

resultado_lexema = []

reservadas = ['NEGATE', 'MTRUE', 'MFALSE', 'ABANICO', 'VERTICAL', 'PERCUTOR', 'GOLPE',
              'VIBRATO', 'METRONOMO', 'PRINTLN', 'FOR', 'IF', 'ENCASO', 'SINO', 'FINENCASO', 'DEF',
              'EXEC', 'TO', 'STEP', 'ENTONS', 'CUANDO', 'PRINCIPAL']

tokens = reservadas + ['ID', 'SET', 'NUMBER', 'BOOL', 'COMMA', 'SEMICOLON',
                       'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EXPONENT', 'WDIVIDE',
                       'MODULE', 'LPARENTHESES', 'RPARENTHESES', 'LBRACKET', 'RBRACKET', 'STRING',
                       'EQUAL', 'NEQUAL', 'GT', 'GTE', 'LT', 'LTE']

t_ignore = '\t '
t_BOOL = r'(True|False)'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EXPONENT = r'\*\*'
t_WDIVIDE = r'//'
t_MODULE = r'%'
t_LPARENTHESES = r'\('
t_RPARENTHESES = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_EQUAL = r'=='
t_NEQUAL = r'\!='
t_GT = r'>'
t_GTE = r'>='
t_LT = r'<'
t_LTE = r'<='
t_STRING = r'"[\w\W\s\S\d]*"'
t_ENCASO = r'EnCaso'
t_SINO = r'SiNo'
t_FINENCASO = r'Fin-EnCaso'
t_CUANDO = r'Cuando'
t_ENTONS = r'EnTons'
t_SET = r'SET'
t_NEGATE = r'\.Neg'
t_MTRUE = r'\.T'
t_MFALSE = r'\.F'
t_DEF = r'Def'
t_EXEC = r'Exec'
t_PRINTLN = r'println!'
t_TO = r'to'
t_FOR = r'For'
t_STEP = r'Step'
t_IF = r'If'
t_PRINCIPAL = r'Principal\(\)'
t_ABANICO = r'Abanico\((A|B)\)'
t_VERTICAL = r'Vertical\((D|I)\)'
t_PERCUTOR = r'Percutor\((D|I|DI|A|B|AB)\)'
t_GOLPE = r'Golpe\(\)'
t_VIBRATO = r'Vibrato\(\d+\)'
t_METRONOMO = r'Metronomo\((A|B),\d+.*(\d+)*\)|Metronomo\((A|B),\s\d+.*(\d+)*\)'

def t_ID(t):
    r'\@[a-zA-Z0-9\?\_]{2,9}'
    if t.value.upper() in reservadas:
        t.value = t.value.upper()
        t.type = t.value

    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    #print('comment written ' + t.value)
    pass

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

def prueba(data):
    global resultado_lexema

    analizador = lex()
    analizador.input(data)

    resultado_lexema.clear()
    while True:
        tok = analizador.token()
        if not tok:
            break
        # print("lexema de "+tok.type+" valor "+tok.value+" linea "tok.lineno)
        estado = "Linea:{:3}, Tipo:{:16}, Valor:{:16}, Posicion:{:4}".format(str(tok.lineno),str(tok.type) ,str(tok.value), str(tok.lexpos) )
        resultado_lexema.append(estado)
    return resultado_lexema

 # instanciamos el analizador lexico
analizador = lex()

if __name__ == '__main__':
    while True:
        data = input("ingrese: ")
        prueba(data)
        print(resultado_lexema)