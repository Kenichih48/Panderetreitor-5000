from ply.lex import lex as lex
import re
import codecs
import os
import sys

from pip._vendor.distlib.compat import raw_input


reservadas = ['NEGATE', 'MTRUE', 'MFALSE', 'ABANICO', 'VERTICAL', 'PERCUTOR', 'GOLPE',
              'VIBRATO', 'METRONOMO', 'PRINTLN', 'FOR', 'IF', 'ENCASO', 'DEF',
              'EXEC', 'TO', 'STEP']

tokens = reservadas + ['NEWLINE', 'ID', 'SET', 'NUMBER', 'BOOL', 'COMMA', 'SEMICOLON',
                       'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EXPONENT', 'WDIVIDE',
                       'MODULE', 'LPARENTHESES', 'RPARENTHESES', 'LBRACKET', 'RBRACKET', 'TEXT',
                       'EQUAL', 'GT', 'GTE', 'LT', 'LTE']

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
t_GT = r'>'
t_GTE = r'>='
t_LT = r'<'
t_LTE = r'<='
t_TEXT = r'"[\w\W\s\S\d]*"'


def t_ID(t):
    r'\@[a-zA-Z0-9\?\_]{2,9}'
    if t.value.upper() in reservadas:
        t.value = t.value.upper()
        t.type = t.value

    return t

def t_ABANICO(t):
    r'Abanico\((A|B)\)'
    t.value = t.value[len(t.value)-2]

    return t

def t_VERTICAL(t):
    r'Vertical\((D|I)\)'
    t.value = t.value[len(t.value)-2]

    return t

def t_PERCUTOR(t):
    r'Percutor\((D|I|DI|A|B|AB)\)'
    if len(t.value) != 11:
        t.value = t.value[len(t.value)-3] + t.value[len(t.value)-2]
    else:
        t.value = t.value[len(t.value)-2]

    return t

def t_GOLPE(t):
    r'Golpe\(\)'
    t.value = ''

    return t

def t_VIBRATO(t):
    r'Vibrato\(\d+\)'
    value = ''
    for n in range(8, len(t.value)-1):
        value += t.value[n]
    t.value = int(value)
    return t

def t_METRONOMO(t):
    r'Metronomo\((A|B),\d+.*(\d+)*\)|Metronomo\((A|B),\s\d+.*(\d+)*\)'
    start = t.value.find("(") + 1
    end = t.value.find(")")
    value = t.value[start:end]
    state = value[0]
    if value[2] == ' ':
        seconds = float(value[3:len(value)])
    else:
        seconds = float(value[2:len(value)])

    value1 = [state, seconds]
    t.value = value1

    return t

def t_NEWLINE(t):
    r'\n+'
    #t.lexer.lineno += len(t.value)
    t.value = ''

    return t

def t_SET(t):
    r'SET'
    t.value = ''

    return t

def t_NEGATE(t):
    r'\.Neg'
    t.value = ''

    return t

def t_MTRUE(t):
    r'\.T'
    t.value = ''

    return t

def t_MFALSE(t):
    r'\.F'
    t.value = ''

    return t

def t_DEF(t):
    r'Def'
    t.value = ''

    return t

def t_EXEC(t):
    r'Exec'
    t.value = ''

    return t

def t_PRINTLN(t):
    r'println!'
    t.value = ''

    return t

def t_TO(t):
    r'to'
    t.value = ''

    return t

def t_FOR(t):
    r'For'
    t.value = ''

    return t

def t_STEP(t):
    r'Step'
    t.value = ''

    return t

def t_IF(t):
    r'If'
    t.value = ''

    return t

def t_COMMENT(t):
    r'\#.*'
    print('comment written ' + t.value)
    pass

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_error(t):
    print("caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)


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


#directorio = "C:/Users/quigo/AndroidStudioProjects/TareaExtraclase42/Tambarduine/Pruebas/"
directorio = "/home/kash/Documents/GitHub/Tambarduine/Pruebas/"
archivo = buscarFicheros(directorio)
test = directorio + archivo
fp = codecs.open(test, "r", "utf-8")
cadena = fp.read()
fp.close()

analizador = lex()

analizador.input(cadena)

while True:
    tok = analizador.token()
    if not tok: break
    print(tok)