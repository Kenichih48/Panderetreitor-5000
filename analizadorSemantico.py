import re
variables = {}
variablesTemp = []
varsTemp = {}
moves = []
metronomoOn = True
printParameters = ''
printList = []
errorList = []
cuandoEntonsList = []
defRutinasDict = {}
contador = 0

#Function to return variables
def returnVariables():
    #print(bool(variables))
    for key, value in variables.items():
        for idx, i in enumerate(variablesTemp):
            if key == i[0]:
                variablesTemp.pop(idx)
                break
    if variablesTemp:
        for idx, i in enumerate(variablesTemp):
            errorList.append("Error semantico, la variable %s nunca fue definida" % variablesTemp[idx][0])

    #if variablesTemp:
    #    for i in range(len(variablesTemp)):
    #        print("Error semantico, la variable %s nunca fue definida" % variablesTemp[i][0])
    return variables

#Function to return moves
def returnMoves():
    return moves

#Function to return printList
def returnPrintList():
    printListTemp = []

    for i in printList:
        iTemp = re.findall(r'\-\-\@[a-zA-Z0-9\?\_]{2,9}', i)
        for j in iTemp:
            #print("j: " + str(j))
            #if j.startswith("--"):
                #j = j.replace("--", "")
                #i = i.replace("--", "")
            for key, value in variables.items():
                if "--" + key == j:
                    #print("key: " + "--" + str(key))
                    i = i.replace("--" + str(key), str(value[0]))
                elif key != j:
                    pass
                #elif key == j:
                #    i = i.replace(str(key), str(value[0]))

        printListTemp.append(i)

    #if not(isNum(variable)) and variable.find('@') != -1:
    #    print("Error semantico, la variable por imprimir no ha sido definida")
    #else:

    return printListTemp
        
#class varDeclaration:
#    def __init__(self, id, value_):
#        check = True
#        self.name = id
#        self.value = value_
        
#        if (value_ == 'True') or (value_ == 'False'):
#            self.type = 'bool'
#        else:
#            try:
#                #print(self.name + ": " + str(float(self.value)))
#                float(self.value)
#            except ValueError:
#                self.type = ''
#                print('Error semantico, la variable por definir no es aceptable: ' + self.name)
#                check = False
#            else:
#                #print('Entered here')
#                self.type = 'num'

#        if  not(bool(variables)) and check == True:
#            variables[self.name] = [self.value, self.type]
#        elif check == True:
#            for key, value in variables.items():
#                if key == id and value[1] == self.type:
#                    variables[self.name] = [self.value, self.type]
#                    break
#                elif key == id and value[1] != self.type:
#                    print("Error semantico, la variable ya existe y se le quiere cambiar el tipo")
#                    break 
#            else:
#                variables[self.name] = [self.value, self.type]

        #print(variables)

#    def returnVariable(self):
#        return 'SET' + self.name

def varDeclarationTemp(id, val):
    global varsTemp
    check = True

    if  not(bool(varsTemp)):
        varsTemp[id] = val
    elif check == True:
        for key, value in varsTemp.items():
            if key == id:
                varsTemp[id] = val
                break
        else:
            varsTemp[id] = val

    #print(varsTemp)

    #return 'SET' + id

def varDeclaration(id, val, line):
    global variables
    typeV = ''
    check = True
    valTemp = str(val)
    if (val == 'True') or (val == 'False'):
        typeV = 'bool'
    elif (valTemp.count("@") == 1):
        variablesTemp.append([id, valTemp])
        print("Variables temp: " + str(variablesTemp))
        return 'SET' + id
    else:
        try:
            float(valTemp)
        except ValueError as e:
            typeV = ''
            check = False
        else:
            typeV = 'num'

    if  not(bool(variables)) and check == True:
        variables[id] = [val, typeV]
    elif check == True:
        for key, value in variables.items():
            if key == id and value[1] == typeV:
                varDeclarationTemp(id, [value[0], value[1]])
                variables[id] = [val, typeV]
                break
            elif key == id and value[1] != typeV:
                errorList.append(["Error semantico, la variable %s ya existe y se le quiere cambiar el tipo" % id, line])
                #print("Error semantico, la variable %s ya existe y se le quiere cambiar el tipo %d" % (id,line))
                #print("Error semantico, la variable " + str(id) + " ya existe y se le quiere cambiar el tipo, Line: " + str(line))
                break 
        else:
            variables[id] = [val, typeV]

    #print(variables)

    return 'SET' + id


def arithOperation(operation, line):
    newOper = operation

    variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', newOper)

    for key, value in variables.items():
        for var in variable:
            if key == var and value[1] == 'num':
                newOper = newOper.replace(var, value[0])
            elif ((newOper.find('True')) != -1) or ((newOper.find('False')) != -1):
                errorList.append(["Error semantico, no se pueden hacer operaciones aritmeticas con booleanos", line])
            elif key == var and value[1] == 'bool':
                errorList.append(["Error semantico, no se pueden hacer operaciones aritmeticas con booleanos 2", line])
            elif key == var:
                pass

    for element in newOper:
        if element == '@':
            return ''
    else:
        return eval(newOper)

def boolOperation(id, operation, line):
    tempValue = ''
    for key, value in variables.items():
        tempValue = value[0]
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
            errorList.append(["Error semantico, no se pueden hacer operaciones booleanas con numeros", line])
    #print(variables)

    if tempValue == '':
        errorList.append(["Error semantico, no se pueden hacer operaciones booleanas con variables no existentes", line])
        return "Error"
    else:
        return 'bool' + id + operation + '&' + tempValue

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
        return 'move' + 'M' + str(movimiento[1])

    elif movimiento[0] == 'D':
        metronomoOn = False
        moves.append('P')
        print('Metronomo is not activated')
        return 'move' + 'P'
        

    #print(moves)

def Abanico(movimiento):
    movimiento = movimiento[len(movimiento)-2]
    if metronomoOn:
        moves.append(movimiento)
    else:
        print('Metronomo is not activated')

    #print(moves)

    return 'move' + movimiento

def Vertical(movimiento):
    movimiento = movimiento[len(movimiento)-2]
    if metronomoOn:
        moves.append(movimiento)
    else:
        print('Metronomo is not activated')

    return 'move' + movimiento

def Percutor(movimiento):
    if len(movimiento) != 11:
        movimiento = movimiento[len(movimiento)-3] + movimiento[len(movimiento)-2]
    else:
        movimiento = movimiento[len(movimiento)-2]

    movimiento = movimiento.replace('D', 'R')
    movimiento = movimiento.replace('I', 'L')
    movimiento = movimiento.replace('A', 'O')
    movimiento = movimiento.replace('B', 'U')

    if metronomoOn:
        moves.append(movimiento)
    else:
        print('Metronomo is not activated')

    return 'move' + movimiento

def Golpe(movimiento):
    movimiento = 'G'
    if metronomoOn:
        moves.append(movimiento)
    else:
        print('Metronomo is not activated')

    #print(moves)

    return 'move' + movimiento

def Vibrato(movimiento):
    value = ''
    for n in range(8, len(movimiento)-1):
        value += movimiento[n]
    movimiento = int(value)
    todo = 'DI'
    if metronomoOn:
        todo = todo * movimiento
        moves.append(todo)
    else:
        print('Metronomo is not activated')

    return 'move' + todo

def isNum(num):
    try:
        int(num) or float(num)
    except ValueError:
        return False
    else:
        return True

def toPrint():
    global printParameters, printList
    
    printList.append(printParameters)
    #print(printParameters)

    printParametersTemp = printParameters
    printParameters = ''

    return 'print' + printParametersTemp

def addPrintPar(string):
    global printParameters

    newStr = string

    newStr = newStr.strip("\"")
    printParameters += newStr
    
    return newStr

def addPrintPar2(variable):
    global printParameters

    #for key, value in variables.items():
    #    if key == variable:
    #        variable = variable.replace(str(key), str(value[0]))
    #    elif key != variable:
    #        pass

    #if not(isNum(variable)) and variable.find('@') != -1:
    #    print("Error semantico, la variable por imprimir no ha sido definida")
    #else:
    if not(isNum(variable)):
        for key, value in variables.items():
            if key == variable:
                printParameters += value[0]
                break
        else:
            printParameters += '--' + str(variable)
    else:
        printParameters += str(variable)

    return str(variable)

def conditionVerifier(condition):
    variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', condition)

    for key, value in variables.items():
        for var in variable:
            if key == var and (value[1] == "num" or value[1] == "bool"):
                #print("Condition: " + str(condition) + ", Key: " + str(key) + ", Value: " + str(value[0]))
                condition = condition.replace(str(key), str(value[0]))
            elif key != var:
                pass

    #print("Condition: " + str(condition))

    for element in condition:
        if element == '@':
            errorList.append("Error semantico, la variable %s no ha sido definida" % element)
    else:
        return eval(condition)    

def ifVerifier(condition, block, block2, line):

    checkBlock2 = True
    block = block.replace(";", ",")
    block = block.split(",")
    try:
        block2 = block2.replace(";", ",")
        block2 = block2.split(",")
    except:
        checkBlock2 = False

    
    for i in block:
        if i == 'None':
            block.remove(i)
    try:
        block.remove('None')
    except:
        pass

    if checkBlock2:
        for i in block2:
            if i == 'None':
                block2.remove(i)
        try:
            block2.remove('None')
        except:
            pass


    #print('Block: ' + str(block))

    if not(conditionVerifier(condition)):
        #print('--Entered if is false--')
        for i in block:
            if i.startswith('SET'):
                i = i.replace('SET', '')
                for key, value in variables.items():
                    if key == i:
                        variables.pop(i)
                        break

                #print(variables)

            elif i.startswith('bool'):
                i = i.replace('bool', '')
                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', i)
                #print('Variable: ' + str(variable))
                variableTemp = variable[0]
                i = i[len(variableTemp):len(i)]
                i = i.split('&')
                #print('variable: ' + str(variable) + ' i: ' + str(i))
                for key, value in variables.items():
                    if key == variableTemp:
                        if i[0] == '.Neg' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.Neg' and value[0] == 'False':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'True' and value[0] == 'True':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'False' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'False' and value[0] == 'False':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'True' and value[0] == 'False':
                            value[0] = 'True'
                #print('Variables after if is false: ' + str(variables))
            elif i.startswith('print'):
                i = i.replace('print', "")
                #print(i)
                for j in printList:
                    if j == i:
                        printList.remove(j)
                        break
                #print(printList)

            elif i.startswith('move'):
                i = i.replace('move', '')
                moves.reverse()
                moves.remove(i)
                moves.reverse()

                #print(moves)

            elif i.startswith('exec'):
                i = i.replace('exec', '')
                parametersTemp = i.split('&')
                id = parametersTemp[0]
                parametersTemp.pop(0)
                for x in parametersTemp:
                    if x == '':
                        parametersTemp.remove(x)
                #print('params: ' + str(parametersTemp) + ', id: ' + str(id))
                for key, value in defRutinasDict.items():
                    #print('key: ' + str(key) + ', value' + str(value[1]))
                    if id == key:
                        for j in value[1]:
                            for idx, k in enumerate(value[0]):
                                #print(k)
                                #print(j.find(k) != -1)
                                if j.find(k) != -1:
                                    #print(k, parametersTemp[idx])
                                    j = j.replace(k, parametersTemp[idx])
                            #print('j: ' + str(j))
                            if j.startswith('SET'):
                                jTemp = j.replace('SET', '')
                                jTemp = re.match(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                for key2, value2 in variables.items():
                                    if key2 == jTemp[0]:
                                        variables.pop(jTemp[0])
                                        break

                                #print(variables)

                            elif j.startswith('bool'):
                                jTemp = j.replace('bool', '')
                                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                #print('Variable: ' + str(variable))
                                variableTemp = variable[0]
                                jTemp = jTemp[len(variableTemp):len(i)]
                                jTemp = jTemp.split('&')
                                #print('variable: ' + str(variable) + ' i: ' + str(i))
                                for key2, value2 in variables.items():
                                    if key2 == variableTemp:
                                        if jTemp[0] == '.Neg' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.Neg' and value[0] == 'False':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'True' and value[0] == 'True':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'False' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'False' and value[0] == 'False':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'True' and value[0] == 'False':
                                            value[0] = 'True'
                                #print('Variables after if is false: ' + str(variables))
                            elif j.startswith('print'):
                                jTemp = j.replace('print', "")
                                
                                try:
                                    jTemp = jTemp.replace("--", "")
                                except:
                                    pass
                                #print(jTemp)
                                for k in printList:
                                    if k == jTemp:
                                        printList.remove(jTemp)
                                        break
                                #print(printList)

                            elif j.startswith('move'):
                                jTemp = j.replace('move', '')
                                #print(j)
                                moves.reverse()
                                moves.remove(jTemp)
                                moves.reverse()


        blockTemp = ''
        for x in block2:
            blockTemp += x + ';'

        #print(str(conditionVerifier(condition)) + ';' + blockTemp)

        return str(conditionVerifier(condition)) + ';' + blockTemp

    elif conditionVerifier(condition):
        #print('--Entered if is true--')
        for i in block2:
            if i.startswith('SET'):
                i = i.replace('SET', '')
                for key, value in variables.items():
                    if key == i:
                        variables.pop(i)
                        break

                #print(variables)

            elif i.startswith('bool'):
                i = i.replace('bool', '')
                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', i)
                #print('Variable: ' + str(variable))
                variableTemp = variable[0]
                i = i[len(variableTemp):len(i)]
                i = i.split('&')
                #print('variable: ' + str(variable) + ' i: ' + str(i))
                for key, value in variables.items():
                    if key == variableTemp:
                        if i[0] == '.Neg' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.Neg' and value[0] == 'False':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'True' and value[0] == 'True':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'False' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'False' and value[0] == 'False':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'True' and value[0] == 'False':
                            value[0] = 'True'
                #print('Variables after if is false: ' + str(variables))
            elif i.startswith('print'):
                i = i.replace('print', "")
                #print(i)
                for j in printList:
                    if j == i:
                        printList.remove(j)
                        break
                #print(printList)

            elif i.startswith('move'):
                i = i.replace('move', '')
                moves.reverse()
                moves.remove(i)
                moves.reverse()

                #print(moves)

            elif i.startswith('exec'):
                i = i.replace('exec', '')
                parametersTemp = i.split('&')
                id = parametersTemp[0]
                parametersTemp.pop(0)
                for x in parametersTemp:
                    if x == '':
                        parametersTemp.remove(x)
                #print('params: ' + str(parametersTemp) + ', id: ' + str(id))
                for key, value in defRutinasDict.items():
                    #print('key: ' + str(key) + ', value' + str(value[1]))
                    if id == key:
                        for j in value[1]:
                            for idx, k in enumerate(value[0]):
                                #print(k)
                                #print(j.find(k) != -1)
                                if j.find(k) != -1:
                                    #print(k, parametersTemp[idx])
                                    j = j.replace(k, parametersTemp[idx])
                            #print('j: ' + str(j))
                            if j.startswith('SET'):
                                jTemp = j.replace('SET', '')
                                jTemp = re.match(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                for key2, value2 in variables.items():
                                    if key2 == jTemp[0]:
                                        variables.pop(jTemp[0])
                                        break

                                #print(variables)

                            elif j.startswith('bool'):
                                jTemp = j.replace('bool', '')
                                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                #print('Variable: ' + str(variable))
                                variableTemp = variable[0]
                                jTemp = jTemp[len(variableTemp):len(i)]
                                jTemp = jTemp.split('&')
                                #print('variable: ' + str(variable) + ' i: ' + str(i))
                                for key2, value2 in variables.items():
                                    if key2 == variableTemp:
                                        if jTemp[0] == '.Neg' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.Neg' and value[0] == 'False':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'True' and value[0] == 'True':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'False' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'False' and value[0] == 'False':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'True' and value[0] == 'False':
                                            value[0] = 'True'
                                #print('Variables after if is false: ' + str(variables))
                            elif j.startswith('print'):
                                jTemp = j.replace('print', "")
                                
                                try:
                                    jTemp = jTemp.replace("--", "")
                                except:
                                    pass
                                #print(jTemp)
                                for k in printList:
                                    if k == jTemp:
                                        printList.remove(jTemp)
                                        break
                                #print(printList)

                            elif j.startswith('move'):
                                jTemp = j.replace('move', '')
                                #print(j)
                                moves.reverse()
                                moves.remove(jTemp)
                                moves.reverse()

        blockTemp = ''
        for x in block:
            blockTemp += x + ';'

        #print(str(conditionVerifier(condition)) + ';' + blockTemp)

        return str(conditionVerifier(condition)) + ';' + blockTemp        
                        
    #return str(conditionVerifier(condition))

def ifVerifier2(condition, block, line):
    #print(str(conditionVerifier(condition)))
    global cuandoEntonsList

    block = block.replace(";", ",")
    block = block.split(",")

    #print('Condition: ' + str(condition) + ' block: ' + str(block))

    for i in block:
        if i == 'None':
            block.remove(i)
    try:
        block.remove('None')
    except:
        pass

    #print(block)


    if not(conditionVerifier(condition)):
        #print('--Entered if is false--')
        for i in block:
            if i.startswith('SET'):
                i = i.replace('SET', '')
                for key, value in variables.items():
                    if key == i:
                        variables.pop(i)
                        break

                #print(variables)

            elif i.startswith('bool'):
                i = i.replace('bool', '')
                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', i)
                #print('Variable: ' + str(variable))
                variableTemp = variable[0]
                i = i[len(variableTemp):len(i)]
                i = i.split('&')
                #print('variable: ' + str(variable) + ' i: ' + str(i))
                for key, value in variables.items():
                    if key == variableTemp:
                        if i[0] == '.Neg' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.Neg' and value[0] == 'False':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'True' and value[0] == 'True':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'False' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'False' and value[0] == 'False':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'True' and value[0] == 'False':
                            value[0] = 'True'
                #print('Variables after if is false: ' + str(variables))
            elif i.startswith('print'):
                i = i.replace('print', "")
                #print(i)
                for j in printList:
                    if j == i:
                        printList.remove(j)
                        break
                #print(printList)

            elif i.startswith('move'):
                i = i.replace('move', '')
                moves.reverse()
                moves.remove(i)
                moves.reverse()

                #print(moves)

            elif i.startswith('exec'):
                i = i.replace('exec', '')
                parametersTemp = i.split('&')
                id = parametersTemp[0]
                parametersTemp.pop(0)
                for x in parametersTemp:
                    if x == '':
                        parametersTemp.remove(x)
                #print('params: ' + str(parametersTemp) + ', id: ' + str(id))
                for key, value in defRutinasDict.items():
                    #print('key: ' + str(key) + ', value' + str(value[1]))
                    if id == key:
                        for j in value[1]:
                            for idx, k in enumerate(value[0]):
                                #print(k)
                                #print(j.find(k) != -1)
                                if j.find(k) != -1:
                                    #print(k, parametersTemp[idx])
                                    j = j.replace(k, parametersTemp[idx])
                            #print('j: ' + str(j))
                            if j.startswith('SET'):
                                jTemp = j.replace('SET', '')
                                jTemp = re.match(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                for key2, value2 in variables.items():
                                    if key2 == jTemp[0]:
                                        variables.pop(jTemp[0])
                                        break

                                #print(variables)

                            elif j.startswith('bool'):
                                jTemp = j.replace('bool', '')
                                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                #print('Variable: ' + str(variable))
                                variableTemp = variable[0]
                                jTemp = jTemp[len(variableTemp):len(i)]
                                jTemp = jTemp.split('&')
                                #print('variable: ' + str(variable) + ' i: ' + str(i))
                                for key2, value2 in variables.items():
                                    if key2 == variableTemp:
                                        if jTemp[0] == '.Neg' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.Neg' and value[0] == 'False':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'True' and value[0] == 'True':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'False' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'False' and value[0] == 'False':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'True' and value[0] == 'False':
                                            value[0] = 'True'
                                #print('Variables after if is false: ' + str(variables))
                            elif j.startswith('print'):
                                jTemp = j.replace('print', "")
                                
                                try:
                                    jTemp = jTemp.replace("--", "")
                                except:
                                    pass
                                #print(jTemp)
                                for k in printList:
                                    if k == jTemp:
                                        printList.remove(jTemp)
                                        break
                                #print(printList)

                            elif j.startswith('move'):
                                jTemp = j.replace('move', '')
                                #print(j)
                                moves.reverse()
                                moves.remove(jTemp)
                                moves.reverse()

        return str(conditionVerifier(condition))

    elif conditionVerifier(condition):
        for i in block:
            cuandoEntonsList.append(i)

        cuandoEntonsList.append('END')

        blockTemp = ''
        for x in block:
            blockTemp += x + ';'
        
        return str(conditionVerifier(condition)) + ';' + blockTemp

def forVerifier(id, factor, num, block, line):
    idTemp = id
    factorTemp = factor
    blockTemp = []

    #print(str(id) + ',' + str(factor) + ',' + str(num))

    for key, value in variables.items():
        if key == idTemp and value[1] == 'num':
            idTemp = value[0]
        elif key == idTemp and value[1] == 'bool':
            errorList.append(["Error semantico, no se pueden usar booleanos en ciclos For 1", line])
            return 'Error'
        elif key != idTemp:
            pass
        
    for key, value in variables.items():
        if key == factorTemp and value[1] == 'num':
            factorTemp = value[0]
        elif key == factorTemp and value[1] == 'bool':
            errorList.append(["Error semantico, no se pueden usar booleanos en ciclos For 2", line])
            return 'Error'
        elif key != factorTemp:
            pass

    if idTemp.find('@') != -1:
        idTemp = 1
    if factorTemp.find('@') != -1:
        errorList.append(["Error semantico, no se pueden usar booleanos en ciclos For o variable maxima no definida", line])
        return 'Error'

    block = block.replace(";", ",")
    block = block.split(",")

    for i in block:
        if i == 'None':
            block.remove(i)
    try:
        block.remove('None')
    except:
        pass

    for i in block:
        if i.startswith('SET'):
            i = i.replace('SET', '')
            keyTemp = ''
            valueTemp = ''
            for key, value in variables.items():
                if key == i:
                    keyTemp = key
                    valueTemp = value[0]
                    variables.pop(i)
                    break

            for idx, j in enumerate(variablesTemp):
                #print("id: " + id)
                if j[1] == id:
                    if int(idTemp) <= int(factorTemp) + 1:
                        for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
                            idTemp = x
                        varDeclaration(i, idTemp, line)
                        blockTemp.append('SET' + i)
                    else:
                        return ''
                    variablesTemp.pop(idx)
                    break
                else:
                    pass
            else:
                varDeclaration(keyTemp, valueTemp, line)
            
            

            #print(variables)

        elif i.startswith('bool'):
            blockTemp.append(i + '&' + str(idTemp) + '&' + str(factorTemp) + '&' + str(num))
            i = i.replace('bool', '')
            #print(i)
            variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', i)
            #print('Variable: ' + str(variable))
            variableTemp = variable[0]
            i = i[len(variableTemp):len(i)]
            i = i.split('&')
            #print('variable: ' + str(variable) + ' i: ' + str(i))
            for key, value in variables.items():
                if key == variableTemp:
                    if i[0] == '.Neg' and value[0] == 'True':
                        value[0] = 'False'
                    elif i[0] == '.Neg' and value[0] == 'False':
                        value[0] = 'True'
                    elif i[0] == '.T' and i[1] == 'True' and value[0] == 'True':
                        value[0] = 'True'
                    elif i[0] == '.T' and i[1] == 'False' and value[0] == 'True':
                        value[0] = 'False'
                    elif i[0] == '.F' and i[1] == 'False' and value[0] == 'False':
                        value[0] = 'False'
                    elif i[0] == '.F' and i[1] == 'True' and value[0] == 'False':
                        value[0] = 'True'
            #print('Variables after deleting past: ' + str(variables))
            
            if int(idTemp) <= int(factorTemp) + 1:
                varTemp = idTemp - 1
                for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
                    varTemp += 1
                    #print('varTemp: ' + str(varTemp))    
                if varTemp % 2 != 0:
                    for key, value in variables.items():
                        if key == variableTemp:
                            if i[0] == '.Neg' and value[0] == 'True':
                                value[0] = 'False'
                            elif i[0] == '.Neg' and value[0] == 'False':
                                value[0] = 'True'
                else:
                    pass
            else:
                return ''

            #print('Variables after for: ' + str(variables))

        elif i.startswith('print'):
            iTemp = i.replace('print', "")
            varTemp = []
            for j in printList:
                if j == iTemp:
                    varTemp = re.findall(r'\-\-\@[a-zA-Z0-9\?\_]{2,9}', j)
                    printList.remove(j)
                    break
            for j2 in varTemp:
                if j2 == "--" + id:
                    if int(idTemp) <= int(factorTemp) + 1:
                        for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
                            iTemp2 = iTemp.replace(j2, str(x))
                            #print('iTemp2: ' + iTemp2)
                            printList.append(iTemp2)
                            blockTemp.append('print' + iTemp2)

            #print(printList)

        elif i.startswith('move'):
            i = i.replace('move', '')
            moves.reverse()
            moves.remove(i)
            moves.reverse()

            if int(idTemp) <= int(factorTemp) + 1:
                for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
                    moves.append(i)
                    blockTemp.append('move' + i)
            else:
                return ''

        elif i.startswith('exec'):
            i = i.replace('exec', '')
            parametersTemp = i.split('&')
            id2 = parametersTemp[0]
            parametersTemp.pop(0)
            parTemp = []

            for x in parametersTemp:
                if x == '':
                    parametersTemp.remove(x)
            #print('params: ' + str(parametersTemp) + ', id: ' + str(id))
            for key, value in defRutinasDict.items():
                #print('key: ' + str(key) + ', value' + str(value[1]))
                if id2 == key:
                    for j in value[1]:
                        for idx, k in enumerate(value[0]):
                            #print(k)
                            #print(j.find(k) != -1)
                            if j.find(k) != -1 and not(j.startswith("print")):
                                #print(k, parametersTemp[idx])
                                j = j.replace(k, parametersTemp[idx])
                            elif j.find(k) != -1 and (j.startswith("print")):
                                parTemp.append([k,parametersTemp[idx]])
                                #print('j: ' + str(j))
                        #print('j: ' + str(j))
                        if j.startswith('SET'):
                            keyTemp = ''
                            valueTemp = ''
                            jTemp = j.replace('SET', '')
                            jTemp = re.match(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                            for key2, value2 in variables.items():
                                if key2 == jTemp[0]:
                                    keyTemp = key2
                                    valueTemp = value2[0]
                                    variables.pop(jTemp[0])
                                    break
                            for idx, j in enumerate(variablesTemp):
                                    #print("id: " + id)
                                if j[1] == id:
                                    if int(idTemp) <= int(factorTemp) + 1:
                                        for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
                                            #idTemp = x
                                            print("gay")
                                        #print(i, idTemp)
                                        varDeclaration(jTemp[0], idTemp, line)
                                        blockTemp.append('SET' + jTemp[0])
                                    else:
                                        return ''
                                    variablesTemp.pop(idx)
                                    break
                                else:
                                    pass
                            else:
                                varDeclaration(keyTemp, valueTemp, line)

                        elif j.startswith('bool'):
                            jTemp = j.replace('bool', '')
                            #print(jTemp)
                            variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                            #print('Variable: ' + str(variable))
                            variableTemp = variable[0]
                            jTemp = jTemp[len(variableTemp):len(i)+1]
                            jTemp = jTemp.split('&')
                            #print(jTemp)
                            #print('variable: ' + str(variable) + ' i: ' + str(i))
                            for key2, value2 in variables.items():
                                if key2 == variableTemp:
                                    if jTemp[0] == '.Neg' and value2[0] == 'True':
                                        value[0] = 'False'
                                    elif jTemp[0] == '.Neg' and value2[0] == 'False':
                                        value[0] = 'True'
                                    elif jTemp[0] == '.T' and jTemp[1] == 'True' and value[0] == 'True':
                                        value[0] = 'True'
                                    elif jTemp[0] == '.T' and jTemp[1] == 'False' and value[0] == 'True':
                                        value[0] = 'False'
                                    elif jTemp[0] == '.F' and jTemp[1] == 'False' and value[0] == 'False':
                                        value[0] = 'False'
                                    elif jTemp[0] == '.F' and jTemp[1] == 'True' and value[0] == 'False':
                                        value[0] = 'True'

                            #print(variables)
                            
                            if int(idTemp) <= int(factorTemp) + 1:
                                print(idTemp)
                                varTemp = int(idTemp) - 1
                                for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
                                    varTemp += 1
                                    #print('varTemp: ' + str(varTemp))    
                                if varTemp % 2 != 0:
                                    for key2, value2 in variables.items():
                                        if key2 == variableTemp:
                                            if jTemp[0] == '.Neg' and value2[0] == 'True':
                                                value2[0] = 'False'
                                            elif jTemp[0] == '.Neg' and value2[0] == 'False':
                                                value2[0] = 'True'
                                else:
                                    pass
                            else:
                                return ''

                        elif j.startswith('print'):
                            iTemp = j.replace('print', "")
                            try:
                                iTemp = iTemp.replace("--", "")
                            except:
                                pass
                            varTemp = []
                            kTemp = ''
                            yTemp = ''
                            for k in printList:
                                m = re.findall(r'\d+', k)
                                for x in parTemp:
                                    for y in m:
                                        if x[1] == y:
                                            kTemp = k.replace(y, x[0])
                                            yTemp = x[0]
                            #print('k: ' + str(kTemp) + ', iTemp: ' + str(iTemp))
                            if kTemp == iTemp:
                                printList.remove(k)

                            if int(idTemp) <= int(factorTemp) + 1:
                                #print('idTemp: ' + str(idTemp))
                                for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
                                    #print(x)
                                    iTemp2 = iTemp.replace(yTemp, str(x))
                                    #print(iTemp2)
                                    #print('iTemp2: ' + iTemp2)
                                    printList.append(iTemp2)
                                    blockTemp.append('print' + iTemp2)

                        elif j.startswith('move'):
                            jTemp = j.replace('move', '')
                            #print(j)
                            moves.reverse()
                            moves.remove(jTemp)
                            moves.reverse()

                            if int(idTemp) <= int(factorTemp) + 1:
                                for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
                                    moves.append(jTemp)
                                    blockTemp.append('move' + jTemp)
                            else:
                                return ''

            #print(moves)
    blockTempStr = ''
    for x in blockTemp:
        blockTempStr += x + ';'

    #print(blockTempStr)
    return blockTempStr

    #print(str(idTemp) + str(factorTemp))
    
    #if int(idTemp) <= int(factorTemp) + 1:
    #    for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
    #        print(x)
    #else:
    #    return ''
    
def enCasoVerifier(boolString, block, line):
    boolString = boolString.split(";")
    enCasoTemp = []

    print(boolString)

    block = block.replace(";", ",")
    block = block.split(",")

    #print('Block: ' + str(block))

    for i in block:
        if i == 'None':
            block.remove(i)
    try:
        block.remove('None')
    except:
        pass

    #print('Block: ' + str(block))

    if boolString.count("True") > 0:
        #print('--Entered if is false--')
        for i in block:
            if i.startswith('SET'):
                i = i.replace('SET', '')
                for key, value in variables.items():
                    if key == i:
                        variables.pop(i)
                        break

                #print(variables)

            elif i.startswith('bool'):
                i = i.replace('bool', '')
                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', i)
                #print('Variable: ' + str(variable))
                variableTemp = variable[0]
                i = i[len(variableTemp):len(i)]
                i = i.split('&')
                #print('variable: ' + str(variable) + ' i: ' + str(i))
                for key, value in variables.items():
                    if key == variableTemp:
                        if i[0] == '.Neg' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.Neg' and value[0] == 'False':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'True' and value[0] == 'True':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'False' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'False' and value[0] == 'False':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'True' and value[0] == 'False':
                            value[0] = 'True'
                #print('Variables after if is false: ' + str(variables))
            elif i.startswith('print'):
                i = i.replace('print', "")
                #print(i)
                for j in printList:
                    if j == i:
                        printList.remove(j)
                        break
                #print(printList)

            elif i.startswith('move'):
                i = i.replace('move', '')
                moves.reverse()
                moves.remove(i)
                moves.reverse()

            elif i.startswith('exec'):
                i = i.replace('exec', '')
                parametersTemp = i.split('&')
                id = parametersTemp[0]
                parametersTemp.pop(0)
                for x in parametersTemp:
                    if x == '':
                        parametersTemp.remove(x)
                #print('params: ' + str(parametersTemp) + ', id: ' + str(id))
                for key, value in defRutinasDict.items():
                    #print('key: ' + str(key) + ', value' + str(value[1]))
                    if id == key:
                        for j in value[1]:
                            for idx, k in enumerate(value[0]):
                                #print(k)
                                #print(j.find(k) != -1)
                                if j.find(k) != -1:
                                    #print(k, parametersTemp[idx])
                                    j = j.replace(k, parametersTemp[idx])
                            #print('j: ' + str(j))
                            if j.startswith('SET'):
                                jTemp = j.replace('SET', '')
                                jTemp = re.match(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                for key2, value2 in variables.items():
                                    if key2 == jTemp[0]:
                                        variables.pop(jTemp[0])
                                        break

                                #print(variables)

                            elif j.startswith('bool'):
                                jTemp = j.replace('bool', '')
                                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                #print('Variable: ' + str(variable))
                                variableTemp = variable[0]
                                jTemp = jTemp[len(variableTemp):len(i)]
                                jTemp = jTemp.split('&')
                                #print('variable: ' + str(variable) + ' i: ' + str(i))
                                for key2, value2 in variables.items():
                                    if key2 == variableTemp:
                                        if jTemp[0] == '.Neg' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.Neg' and value[0] == 'False':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'True' and value[0] == 'True':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'False' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'False' and value[0] == 'False':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'True' and value[0] == 'False':
                                            value[0] = 'True'
                                #print('Variables after if is false: ' + str(variables))
                            elif j.startswith('print'):
                                jTemp = j.replace('print', "")
                                
                                try:
                                    jTemp = jTemp.replace("--", "")
                                except:
                                    pass
                                #print(jTemp)
                                for k in printList:
                                    if k == jTemp:
                                        printList.remove(jTemp)
                                        break
                                #print(printList)

                            elif j.startswith('move'):
                                jTemp = j.replace('move', '')
                                #print(j)
                                moves.reverse()
                                moves.remove(jTemp)
                                moves.reverse()
        try: 
            for i in range(len(boolString)):
                boolString.remove("True")
        except ValueError:
            pass
        try: 
            for i in range(len(boolString)):
                boolString.remove("False")
        except ValueError:
            pass
        try: 
            for i in range(len(boolString)):
                boolString.remove("")
        except ValueError:
            pass
        enCasoStr = ''
        for i in boolString:
            enCasoStr += i + ';'

        print(enCasoStr)

        return enCasoStr


    elif boolString.count("True") == 0:
        enCasoStr = ''
        for i in block:
            enCasoStr += i + ';'

        print(enCasoStr)

        return enCasoStr

                        
    

def enCasoVerifier2(boolString, block, line):
    global cuandoEntonsList
    boolString = boolString.split(";")

    #print(boolString)
    #print(cuandoEntonsList)
    #print(block)

    block = block.replace(";", ",")
    block = block.split(",")

    for i in block:
        if i == 'None':
            block.remove(i)
    try:
        block.remove('None')
    except:
        pass

    #print('CuandoEntonsList: ' + str(cuandoEntonsList) + ' boolString: ' + str(boolString) + ' block: ' + str(block))

    if boolString.count("True") >= 1:
        #print('--Entered entons is true--')
        for i in block:
            if i.startswith('SET'):
                i = i.replace('SET', '')
                for key, value in variables.items():
                    if key == i:
                        variables.pop(i)
                        break

                #print(variables)

            elif i.startswith('bool'):
                i = i.replace('bool', '')
                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', i)
                #print('Variable: ' + str(variable))
                variableTemp = variable[0]
                i = i[len(variableTemp):len(i)]
                i = i.split('&')
                #print('variable: ' + str(variable) + ' i: ' + str(i))
                for key, value in variables.items():
                    if key == variableTemp:
                        if i[0] == '.Neg' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.Neg' and value[0] == 'False':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'True' and value[0] == 'True':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'False' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'False' and value[0] == 'False':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'True' and value[0] == 'False':
                            value[0] = 'True'
                #print('Variables after if is false: ' + str(variables))
            elif i.startswith('print'):
                i = i.replace('print', "")
                #print(i)
                for j in printList:
                    if j == i:
                        printList.remove(j)
                        break
                #print(printList)

            elif i.startswith('move'):
                i = i.replace('move', '')
                moves.reverse()
                moves.remove(i)
                moves.reverse()

            elif i.startswith('exec'):
                i = i.replace('exec', '')
                parametersTemp = i.split('&')
                id = parametersTemp[0]
                parametersTemp.pop(0)
                for x in parametersTemp:
                    if x == '':
                        parametersTemp.remove(x)
                #print('params: ' + str(parametersTemp) + ', id: ' + str(id))
                for key, value in defRutinasDict.items():
                    #print('key: ' + str(key) + ', value' + str(value[1]))
                    if id == key:
                        for j in value[1]:
                            for idx, k in enumerate(value[0]):
                                #print(k)
                                #print(j.find(k) != -1)
                                if j.find(k) != -1:
                                    #print(k, parametersTemp[idx])
                                    j = j.replace(k, parametersTemp[idx])
                            #print('j: ' + str(j))
                            if j.startswith('SET'):
                                jTemp = j.replace('SET', '')
                                jTemp = re.match(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                for key2, value2 in variables.items():
                                    if key2 == jTemp[0]:
                                        variables.pop(jTemp[0])
                                        break

                                #print(variables)

                            elif j.startswith('bool'):
                                jTemp = j.replace('bool', '')
                                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                #print('Variable: ' + str(variable))
                                variableTemp = variable[0]
                                jTemp = jTemp[len(variableTemp):len(i)]
                                jTemp = jTemp.split('&')
                                #print('variable: ' + str(variable) + ' i: ' + str(i))
                                for key2, value2 in variables.items():
                                    if key2 == variableTemp:
                                        if jTemp[0] == '.Neg' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.Neg' and value[0] == 'False':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'True' and value[0] == 'True':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'False' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'False' and value[0] == 'False':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'True' and value[0] == 'False':
                                            value[0] = 'True'
                                #print('Variables after if is false: ' + str(variables))
                            elif j.startswith('print'):
                                jTemp = j.replace('print', "")
                                
                                try:
                                    jTemp = jTemp.replace("--", "")
                                except:
                                    pass
                                #print(jTemp)
                                for k in printList:
                                    if k == jTemp:
                                        printList.remove(jTemp)
                                        break
                                #print(printList)

                            elif j.startswith('move'):
                                jTemp = j.replace('move', '')
                                #print(j)
                                moves.reverse()
                                moves.remove(jTemp)
                                moves.reverse()

                #print(moves)

                #print(moves)

    if boolString.count("True") >= 2:
        #print("--Entered entons is true 2--")
        check = True
        cuandoEntonsList.reverse()
        #print('CuandoEntonsList2: ' + str(cuandoEntonsList))
        for item in cuandoEntonsList:
            if item == '':
                cuandoEntonsList.remove(item)
        for index, item in enumerate(cuandoEntonsList):
            #print("CuandoEntonsList: " + str(cuandoEntonsList))
            #print("item: " + item)
            if cuandoEntonsList.count("END") >= 1:
                if item.startswith('SET'):
                    item = item.replace('SET', '')
                    for key, value in variables.items():
                        if key == item:
                            variables.pop(item)
                            break
                    cuandoEntonsList[index] = ''
                    #print(variables)

                elif item.startswith('bool'):
                    item = item.replace('bool', '')
                    variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', item)
                    #print('Variable: ' + str(variable))
                    variableTemp = variable[0]
                    item = item[len(variableTemp):len(item)]
                    item = item.split('&')
                    #print('variable: ' + str(variable) + ' i: ' + str(i))
                    for key, value in variables.items():
                        if key == variableTemp:
                            if item[0] == '.Neg' and value[0] == 'True':
                                value[0] = 'False'
                            elif item[0] == '.Neg' and value[0] == 'False':
                                value[0] = 'True'
                            elif item[0] == '.T' and item[1] == 'True' and value[0] == 'True':
                                value[0] = 'True'
                            elif item[0] == '.T' and item[1] == 'False' and value[0] == 'True':
                                value[0] = 'False'
                            elif item[0] == '.F' and item[1] == 'False' and value[0] == 'False':
                                value[0] = 'False'
                            elif item[0] == '.F' and item[1] == 'True' and value[0] == 'False':
                                value[0] = 'True'
                    #print('Variables after if is false: ' + str(variables))
                    cuandoEntonsList[index] = ''

                elif item.startswith('print'):
                    item = item.replace('print', "")
                    #print(i)
                    for j in printList:
                        if j == item:
                            printList.remove(j)
                            break
                    #print(printList)
                    cuandoEntonsList[index] = ''

                elif item.startswith('move'):
                    item = item.replace('move', '')
                    moves.reverse()
                    #print(moves)
                    moves.remove(item)
                    #print('after removed: ' + str(moves))
                    moves.reverse()
                    #print('after reverse: ' + str(moves))

                    #print(moves)
                    cuandoEntonsList[index] = ''

                elif item.startswith('exec'):
                    item = item.replace('exec', '')
                    parametersTemp = item.split('&')
                    id = parametersTemp[0]
                    parametersTemp.pop(0)
                    for x in parametersTemp:
                        if x == '':
                            parametersTemp.remove(x)
                    #print('params: ' + str(parametersTemp) + ', id: ' + str(id))
                    for key, value in defRutinasDict.items():
                        #print('key: ' + str(key) + ', value' + str(value[1]))
                        if id == key:
                            for j in value[1]:
                                for idx, k in enumerate(value[0]):
                                    #print(k)
                                    #print(j.find(k) != -1)
                                    if j.find(k) != -1:
                                        #print(k, parametersTemp[idx])
                                        j = j.replace(k, parametersTemp[idx])
                                #print('j: ' + str(j))
                                if j.startswith('SET'):
                                    jTemp = j.replace('SET', '')
                                    jTemp = re.match(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                    for key2, value2 in variables.items():
                                        if key2 == jTemp[0]:
                                            variables.pop(jTemp[0])
                                            break

                                    #print(variables)

                                elif j.startswith('bool'):
                                    jTemp = j.replace('bool', '')
                                    variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                    #print('Variable: ' + str(variable))
                                    variableTemp = variable[0]
                                    jTemp = jTemp[len(variableTemp):len(item)]
                                    jTemp = jTemp.split('&')
                                    #print('variable: ' + str(variable) + ' i: ' + str(i))
                                    for key2, value2 in variables.items():
                                        if key2 == variableTemp:
                                            if jTemp[0] == '.Neg' and value[0] == 'True':
                                                value[0] = 'False'
                                            elif jTemp[0] == '.Neg' and value[0] == 'False':
                                                value[0] = 'True'
                                            elif jTemp[0] == '.T' and jTemp[1] == 'True' and value[0] == 'True':
                                                value[0] = 'True'
                                            elif jTemp[0] == '.T' and jTemp[1] == 'False' and value[0] == 'True':
                                                value[0] = 'False'
                                            elif jTemp[0] == '.F' and jTemp[1] == 'False' and value[0] == 'False':
                                                value[0] = 'False'
                                            elif jTemp[0] == '.F' and jTemp[1] == 'True' and value[0] == 'False':
                                                value[0] = 'True'
                                    #print('Variables after if is false: ' + str(variables))
                                elif j.startswith('print'):
                                    jTemp = j.replace('print', "")
                                    
                                    try:
                                        jTemp = jTemp.replace("--", "")
                                    except:
                                        pass
                                    #print(jTemp)
                                    for k in printList:
                                        if k == jTemp:
                                            printList.remove(jTemp)
                                            break
                                    #print(printList)

                                elif j.startswith('move'):
                                    jTemp = j.replace('move', '')
                                    #print(j)
                                    moves.reverse()
                                    moves.remove(jTemp)
                                    moves.reverse()


                    cuandoEntonsList[index] = ''

                elif item.startswith('END'):
                    cuandoEntonsList[index] = ''

            elif cuandoEntonsList.count('END') == 0:
                break

            

        #cuandoEntonsList.reverse()

        try:
            while True:
                cuandoEntonsList.remove("")
        except ValueError:
            pass

        enCasoStr = ''
        for i in cuandoEntonsList:
            enCasoStr += i + ';'
        
        cuandoEntonsList.clear()
        return enCasoStr


    if boolString.count("True") == 0:
        enCasoStr = ''
        for i in block:
            enCasoStr += i + ';'

        cuandoEntonsList.clear()

        return enCasoStr
                        
    
def defRutinas(id, parameters, block, line):
    global defRutinasDict
    rutinasListTemp = []
    parametersTemp = []
    check = True

    #print(block)

    for x in defRutinasDict:
        if x == id:
            check = False
            break
        else:
            pass
    
    if check:
        try:
            parametersTemp = parameters.split(",")
        except:
            pass

        
        block = block.replace("None", "")
        block = block.replace(";", ",")
        block = block.split(",")

        for i in block:
            if i == 'None':
                block.remove(i)
        try:
            block.remove('None')
        except:
            pass

        try: 
            while True:
                block.remove("True")
        except ValueError:
            pass

        try: 
            while True:
                block.remove("False")
        except ValueError:
            pass

        try: 
            while True:
                block.remove("")
        except ValueError:
            pass

        #print(block)

        for i in block:
            if i.startswith('SET'):
                i = i.replace('SET', '')
                for key, value in variables.items():
                    if key == i:
                        #varsTemp.append("SET" + str(key) + "," + str(value[0]))
                        #print(str(key) + str(value[0]))
                        rutinasListTemp.append('SET' + i + ',' + str(value[0]))
                        variables.pop(i)
                        break

                #print(variables)

            elif i.startswith('bool'):
                rutinasListTemp.append(i)
                i = i.replace('bool', '')
                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', i)
                #print('Variable: ' + str(variable))
                variableTemp = variable[0]
                i = i[len(variableTemp):len(i)]
                i = i.split('&')
                #print('variable: ' + str(variable) + ' i: ' + str(i))
                for key, value in variables.items():
                    if key == variableTemp:
                        if i[0] == '.Neg' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.Neg' and value[0] == 'False':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'True' and value[0] == 'True':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'False' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'False' and value[0] == 'False':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'True' and value[0] == 'False':
                            value[0] = 'True'
                #print('Variables after if is false: ' + str(variables))
            elif i.startswith('print'):
                rutinasListTemp.append(i)
                i = i.replace('print', "")
                for j in printList:
                    if j == i:
                        printList.remove(j)
                        break

            elif i.startswith('move'):
                rutinasListTemp.append(i)
                i = i.replace('move', '')
                moves.reverse()
                moves.remove(i)
                moves.reverse()

                #print(moves)

            elif i.startswith('exec'):
                rutinasListTemp.append(i)
                print(i)
                print(rutinasListTemp)
                i = i.replace('exec', '')
                parametersTemp = i.split('&')
                id = parametersTemp[0]
                parametersTemp.pop(0)
                for x in parametersTemp:
                    if x == '':
                        parametersTemp.remove(x)
                #print('params: ' + str(parametersTemp) + ', id: ' + str(id))
                for key, value in defRutinasDict.items():
                    #print('key: ' + str(key) + ', value' + str(value[1]))
                    if id == key:
                        for j in value[1]:
                            for idx, k in enumerate(value[0]):
                                #print(k)
                                #print(j.find(k) != -1)
                                if j.find(k) != -1:
                                    #print(k, parametersTemp[idx])
                                    j = j.replace(k, parametersTemp[idx])
                            #print('j: ' + str(j))
                            if j.startswith('SET'):
                                jTemp = j.replace('SET', '')
                                jTemp = re.match(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                for key2, value2 in variables.items():
                                    if key2 == jTemp[0]:
                                        variables.pop(jTemp[0])
                                        break

                                #print(variables)

                            elif j.startswith('bool'):
                                jTemp = j.replace('bool', '')
                                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                #print('Variable: ' + str(variable))
                                variableTemp = variable[0]
                                jTemp = jTemp[len(variableTemp):len(i)]
                                jTemp = jTemp.split('&')
                                #print('variable: ' + str(variable) + ' i: ' + str(i))
                                for key2, value2 in variables.items():
                                    if key2 == variableTemp:
                                        if jTemp[0] == '.Neg' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.Neg' and value[0] == 'False':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'True' and value[0] == 'True':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'False' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'False' and value[0] == 'False':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'True' and value[0] == 'False':
                                            value[0] = 'True'
                                #print('Variables after if is false: ' + str(variables))
                            elif j.startswith('print'):
                                jTemp = j.replace('print', "")
                                
                                try:
                                    jTemp = jTemp.replace("--", "")
                                except:
                                    pass
                                #print(jTemp)
                                for k in printList:
                                    if k == jTemp:
                                        printList.remove(jTemp)
                                        break
                                #print(printList)

                            elif j.startswith('move'):
                                jTemp = j.replace('move', '')
                                #print(j)
                                moves.reverse()
                                moves.remove(jTemp)
                                moves.reverse()

        defRutinasDict[id] = [parametersTemp, rutinasListTemp]
        #print('defRutinasDict: ' + str(defRutinasDict))
        #print('id: ' + str(id) + ', parameters: ' + str(parametersTemp) + ', block: ' + str(block))

    else:
        errorList.append(["Error semantico, el nombre %s de la rutina utilizada ya existe" % id, line])

def defPrincipal(block, line):
    global contador

    if contador == 0:
        contador += 1
        pass
    elif contador != 0:

        errorList.append(["Error semantico, no se puede tener dos rutinas principales definidas", line])
        block = block.replace(";", ",")
        block = block.split(",")
        for i in block:
            if i == 'None':
                block.remove(i)
        try:
            block.remove('None')
        except:
            pass

        for i in block:
            if i.startswith('SET'):
                i = i.replace('SET', '')
                for key, value in variables.items():
                    if key == i:
                        variables.pop(i)
                        break

                #print(variables)

            elif i.startswith('bool'):
                i = i.replace('bool', '')
                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', i)
                #print('Variable: ' + str(variable))
                variableTemp = variable[0]
                i = i[len(variableTemp):len(i)]
                i = i.split('&')
                #print('variable: ' + str(variable) + ' i: ' + str(i))
                for key, value in variables.items():
                    if key == variableTemp:
                        if i[0] == '.Neg' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.Neg' and value[0] == 'False':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'True' and value[0] == 'True':
                            value[0] = 'True'
                        elif i[0] == '.T' and i[1] == 'False' and value[0] == 'True':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'False' and value[0] == 'False':
                            value[0] = 'False'
                        elif i[0] == '.F' and i[1] == 'True' and value[0] == 'False':
                            value[0] = 'True'
                #print('Variables after if is false: ' + str(variables))
            elif i.startswith('print'):
                i = i.replace('print', "")
                #print(i)
                for j in printList:
                    if j == i:
                        printList.remove(j)
                        break
                #print(printList)

            elif i.startswith('move'):
                i = i.replace('move', '')
                moves.reverse()
                moves.remove(i)
                moves.reverse()

                #print(moves)

            elif i.startswith('exec'):
                i = i.replace('exec', '')
                parametersTemp = i.split('&')
                id = parametersTemp[0]
                parametersTemp.pop(0)
                for x in parametersTemp:
                    if x == '':
                        parametersTemp.remove(x)
                #print('params: ' + str(parametersTemp) + ', id: ' + str(id))
                for key, value in defRutinasDict.items():
                    #print('key: ' + str(key) + ', value' + str(value[1]))
                    if id == key:
                        for j in value[1]:
                            for idx, k in enumerate(value[0]):
                                #print(k)
                                #print(j.find(k) != -1)
                                if j.find(k) != -1:
                                    #print(k, parametersTemp[idx])
                                    j = j.replace(k, parametersTemp[idx])
                            #print('j: ' + str(j))
                            if j.startswith('SET'):
                                jTemp = j.replace('SET', '')
                                jTemp = re.match(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                for key2, value2 in variables.items():
                                    if key2 == jTemp[0]:
                                        variables.pop(jTemp[0])
                                        break

                                #print(variables)

                            elif j.startswith('bool'):
                                jTemp = j.replace('bool', '')
                                variable = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}', jTemp)
                                #print('Variable: ' + str(variable))
                                variableTemp = variable[0]
                                jTemp = jTemp[len(variableTemp):len(i)]
                                jTemp = jTemp.split('&')
                                #print('variable: ' + str(variable) + ' i: ' + str(i))
                                for key2, value2 in variables.items():
                                    if key2 == variableTemp:
                                        if jTemp[0] == '.Neg' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.Neg' and value[0] == 'False':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'True' and value[0] == 'True':
                                            value[0] = 'True'
                                        elif jTemp[0] == '.T' and jTemp[1] == 'False' and value[0] == 'True':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'False' and value[0] == 'False':
                                            value[0] = 'False'
                                        elif jTemp[0] == '.F' and jTemp[1] == 'True' and value[0] == 'False':
                                            value[0] = 'True'
                                #print('Variables after if is false: ' + str(variables))
                            elif j.startswith('print'):
                                jTemp = j.replace('print', "")
                                
                                try:
                                    jTemp = jTemp.replace("--", "")
                                except:
                                    pass
                                #print(jTemp)
                                for k in printList:
                                    if k == jTemp:
                                        printList.remove(jTemp)
                                        break
                                #print(printList)

                            elif j.startswith('move'):
                                jTemp = j.replace('move', '')
                                #print(j)
                                moves.reverse()
                                moves.remove(jTemp)
                                moves.reverse()


def execRutinas(id, parameters, line):
    global defRutinasDict
    parametersTemp = []
    #check = True
    try:
        parametersTemp = parameters.split(",")
    except:
        pass

    #print("id: " + id + ", parameters: " + str(parameters))

    for key, value in variables.items():
            for idx, i in enumerate(parametersTemp):
                if key == i:
                    parametersTemp[idx] = value[0]

    #print(parameters)
    
    for key, value in defRutinasDict.items():
        #print("key: " + str(key) + ", value: " + str(value))
        print("id: " + id + ', parametersGiven: ' + str(len(parametersTemp)) + ', parametersNeeded: ' + str(len(value[0])))
        if key == id and len(parametersTemp) == len(value[0]):
            for i in value[1]:
                print('i: ' + i)
                for idx, j in enumerate(value[0]):
                    if i.find(j) != -1:
                        i = i.replace(j, parametersTemp[idx])
                    for idx2, k in enumerate(variablesTemp):
                        if k[1] == j:
                            tempVar = k[1].replace(j, parametersTemp[idx])
                            varDeclaration(k[0], tempVar, line)
                            #variablesTemp.pop(idx2)
                if i.startswith("SET"):
                    iTemp = i.replace("SET", "")
                    iTemp2 = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}',iTemp)
                    varDeclaration(iTemp2[0], iTemp[len(iTemp2[0]) + 1:len(iTemp)], line)
                if i.startswith("print"):
                    iTemp = i.replace("print", "")
                    try:
                        iTemp = iTemp.replace("--", "")
                    except:
                        pass
                    printList.append(iTemp)
                if i.startswith("move"):
                    iTemp = i.replace("move", "")
                    moves.append(iTemp)

                if i.startswith('exec'):
                    i = i.replace('exec', '')
                    print("hello")
                #    parametersTemp = i.split('&')
                #    id = parametersTemp[0]
                #    parametersTemp.pop(0)
                #    for x in parametersTemp:
                #        if x == '':
                #            parametersTemp.remove(x)
    
                #    for key, value in defRutinasDict.items():
                #    #print('key: ' + str(key) + ', value' + str(value[1]))
                #        if id == key:
                #            for j in value[1]:
                #                for idx, k in enumerate(value[0]):
                #                    #print(k)
                #                    #print(j.find(k) != -1)
                #                    if j.find(k) != -1:
                #                        #print(k, parametersTemp[idx])
                #                        j = j.replace(k, parametersTemp[idx])

                #                if i.startswith("SET"):
                #                    iTemp = i.replace("SET", "")
                #                    iTemp2 = re.findall(r'\@[a-zA-Z0-9\?\_]{2,9}',iTemp)
                #                    varDeclaration(iTemp2[0], iTemp[len(iTemp2[0]) + 1:len(iTemp)])
                #                if i.startswith("print"):
                #                    iTemp = i.replace("print", "")
                #                    try:
                #                        iTemp = iTemp.replace("--", "")
                #                    except:
                #                        pass
                #                    printList.append(iTemp)
                #                if i.startswith("move"):
                #                    iTemp = i.replace("move", "")
                #                    moves.append(iTemp)

        elif key == id and len(parametersTemp) > len(value[0]):
            errorList.append(["Error semantico, la rutina %s necesita menos parametros de los brindados" % id, line])
        elif key == id and len(parametersTemp) < len(value[0]):
            errorList.append(["Error semantico, la rutina necesita mas parametros de los brindados" % id, line])
        elif key != id:
            pass     
        else:
            errorList.append(["Error semantico, la rutina %s no existe" % id, line])

    for key, value in varsTemp.items():
        varDeclaration(key, value[0], line)

    varsTemp.clear()

    parametersTempTemp = ''
    for i in parametersTemp:
        parametersTempTemp += i + '&'

    

    #print('exec' + str(id) + '&' + str(parametersTempTemp))

    return 'exec' + str(id) + '&' + str(parametersTempTemp)