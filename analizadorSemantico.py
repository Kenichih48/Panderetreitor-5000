import re
variables = {}
moves = []
metronomoOn = False
printParameters = ''
        
class varDeclaration:
    def __init__(self, id, value_):
        check = True
        self.name = id
        self.value = value_
        if (value_ == 'True') or (value_ == 'False'):
            self.type = 'bool'
        else:
            try:
                float(value_)
            except:
                self.type = ''
                print('Error semantico, la variable por definir no es aceptable')
                check = False
            else:
                self.type = 'num'

        if  not(bool(variables)) and check == True:
            variables[self.name] = [self.value, self.type]
        elif check == True:
            for key, value in variables.items():
                if key == id and value[1] == self.type:
                    variables[self.name] = [self.value, self.type]
                    break
                elif key == id and value[1] != self.type:
                    print("Error semantico, la variable ya existe y se le quiere cambiar el tipo")
                    break 
            else:
                variables[self.name] = [self.value, self.type]

        print(variables)

def arithOperation(operation):
    newOper = operation

    variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', newOper)

    for key, value in variables.items():
        for var in variable:
            if key == var and value[1] == 'num':
                newOper = newOper.replace(var, value[0])
            elif ((newOper.find('True')) != -1) or ((newOper.find('False')) != -1):
                print("Error semantico, no se pueden hacer operaciones aritmeticas con booleanos")
            elif key == var and value[1] == 'bool':
                print("Error semantico, no se pueden hacer operaciones aritmeticas con booleanos 2")
            elif key == var:
                pass

    for element in newOper:
        if element == '@':
            return ''
    else:
        return eval(newOper)

def boolOperation(id, operation):
    for key, value in variables.items():
        if key == id and value[1] == 'bool' and operation == '.Neg':
            if value[0] == 'True':
                value[0] = 'False'
            elif value[0] == 'False':
                value[0] = 'True'
        elif key == id and value[1] == 'bool' and operation == '.T':
            value[0] = 'True'
        elif key == id and value[1] == 'bool' and operation == '.F':
            value[0] = 'False'
        elif key == id and value[1] == 'num':
            print("Error semantico, no se pueden hacer operaciones booleanas con numeros")
    print(variables)

def Metronomo(movimiento):

    global metronomoOn

    start = movimiento.find("(") + 1
    end = movimiento.find(")")
    value = movimiento[start:end]
    state = value[0]
    if value[2] == ' ':
        seconds = value[3:len(value)]
    else:
        seconds = value[2:len(value)]

    value1 = [state, seconds]
    movimiento = value1

    if movimiento[0] == 'A':
        metronomoOn = True
        moves.append('M' + str(movimiento[1]))

    elif movimiento[0] == 'D':
        metronomoOn = False
        print('Metronomo is not activated')

def Abanico(movimiento):
    movimiento = movimiento[len(movimiento)-2]
    if metronomoOn:
        moves.append(movimiento)
    else:
        print('Metronomo is not activated')

    #print(movimiento)

def Vertical(movimiento):
    movimiento = movimiento[len(movimiento)-2]
    if metronomoOn:
        moves.append(movimiento)
    else:
        print('Metronomo is not activated')

    #print(movimiento)

def Percutor(movimiento):
    if len(movimiento) != 11:
        movimiento = movimiento[len(movimiento)-3] + movimiento[len(movimiento)-2]
    else:
        movimiento = movimiento[len(movimiento)-2]

    if metronomoOn:
        moves.append(movimiento)
    else:
        print('Metronomo is not activated')

    #print(movimiento)

def Golpe(movimiento):
    
    if metronomoOn:
        moves.append(movimiento)
    else:
        print('Metronomo is not activated')

def Vibrato(movimiento):
    value = ''
    for n in range(8, len(movimiento)-1):
        value += movimiento[n]
    movimiento = int(value)
    todo = ''
    if metronomoOn:
        for i in range(movimiento):
            todo += 'A'
        moves.append(todo)
    else:
        print('Metronomo is not activated')

    print(moves)

def isNum(num):
    try:
        int(num) or float(num)
    except ValueError:
        return False
    else:
        return True

def toPrint():
    global printParameters

    print(printParameters)

    printParameters = ''

def addPrintPar(string):
    global printParameters

    newStr = string

    newStr = newStr.strip("\"")
    printParameters += newStr
    
    return newStr

def addPrintPar2(variable):
    global printParameters

    for key, value in variables.items():
        if key == variable:
            variable = variable.replace(str(key), str(value[0]))
        elif key != variable:
            pass

    if not(isNum(variable)) and variable.find('@') != -1:
        print("Error semantico, la variable por imprimir no ha sido definida")
    else:
        printParameters += str(variable)

    return str(variable)

def conditionVerifier(condition):
    variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', condition)

    for key, value in variables.items():
        for var in variable:
            if key == var:
                #print("Condition: " + str(condition) + ", Key: " + str(key) + ", Value: " + str(value[0]))
                condition = condition.replace(str(key), str(value[0]))
            elif key != var:
                pass

    #print("Condition: " + str(condition))

    for element in condition:
        if element == '@':
            print("Error semantico, la variable por imprimir no ha sido definida")
    else:
        return eval(condition)    

def ifVerifier(condition):
    print(str(conditionVerifier(condition)))
    #print(moves)
    #if conditionVerifier(condition):
    #    print(conditionVerifier)






    

def p_procDeclSt2(p):
    '''procDeclSt : DEF ID LPARENTHESES parameter RPARENTHESES LBRACKET blockList RBRACKET'''
    print('procDeclSt 2')

def p_procDeclSt3(p):
    '''procDeclSt : DEF PRINCIPAL LBRACKET blockList RBRACKET'''
    print("procDeclSt 3")

def p_procDeclSt4(p):
    '''procDeclSt : EXEC ID LPARENTHESES parameter RPARENTHESES'''
    print("procDeclSt 4")

def p_parameter1(p):
    '''parameter : parameterList'''
    print('parameter 1')

def p_parameter2(p):
    '''parameter : empty'''
    print('parameter 2')

def p_parameterList1(p):
    '''parameterList : factor'''
    print('parameterList 1')

def p_parameterList2(p):
    '''parameterList : parameterList COMMA factor'''
    print('parameterList 2')   

def p_statementDecl1(p):
    '''statementDecl : statementList SEMICOLON'''
    print ("statementDecl 1")

def p_statementDeclEmpty(p):
	'''statementDecl : empty'''
	print ("nulo")

def p_statement1(p):
	'''statement : IF condition LBRACKET blockList RBRACKET'''
	print ("statement 1")

def p_statement2(p):
	'''statement : IF condition LBRACKET blockList RBRACKET ELSE LBRACKET blockList RBRACKET'''
	print ("statement 2")

def p_statement3(p):
	'''statement : FOR ID TO factor STEP NUMBER LBRACKET blockList RBRACKET'''
	print ("statement 3")

def p_statement4(p):
    '''statement : FOR ID TO factor LBRACKET blockList RBRACKET'''
    print ("statement 4")

def p_statement4(p):
    '''statement : ENCASO cuandoEntonsList SEMICOLON SINO LBRACKET blockList RBRACKET SEMICOLON FINENCASO'''
    print ("statement 4")

def p_statement5(p):
    '''statement : ENCASO ID cuandoEntonsListAux SEMICOLON SINO LBRACKET blockList RBRACKET SEMICOLON FINENCASO'''
    print ("statement 5")

def p_statementList1(p):
	'''statementList : statement'''
	print ("statementList 1")

def p_statementList2(p):
	'''statementList : statementList SEMICOLON statement'''
	print ("statementList 2")

def p_cuandoEntonsList1(p):
    '''cuandoEntonsList : cuandoEntons'''
    print ("cuandoEntonsList 1")

def p_cuandoEntonsList2(p):
    '''cuandoEntonsList : cuandoEntonsList SEMICOLON cuandoEntons'''
    print ("cuandoEntonsList 2")

def p_cuandoEntons1(p):
    '''cuandoEntons : CUANDO ID relation factor ENTONS LBRACKET blockList RBRACKET'''
    print ("cuandoEntons 1")

def p_cuandoEntonsAux1(p):
    '''cuandoEntonsAux : CUANDO relation factor ENTONS LBRACKET blockList RBRACKET'''
    print ("cuandoEntons 1")

def p_cuandoEntonsListAux1(p):
    '''cuandoEntonsListAux : cuandoEntonsAux'''
    print ("cuandoEntonsList 1")

def p_cuandoEntonsListAux2(p):
    '''cuandoEntonsListAux : cuandoEntonsListAux SEMICOLON cuandoEntonsAux'''
    print ("cuandoEntonsList 2")    

def p_condition1(p):
	'''condition : arithOperation relation arithOperation'''
	print ("condition 1")

def p_condition2(p):
	'''condition : arithOperation relation factor'''
	print ("condition 2")

def p_condition3(p):
	'''condition : factor relation arithOperation'''
	print ("condition 3")

def p_condition4(p):
	'''condition : factor relation factor'''
	print ("condition 4")

def p_condition5(p):
    '''condition : factor'''
    print ("condition 5")