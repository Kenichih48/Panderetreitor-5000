import re
variables = {}
moves = []
metronomoOn = True
printParameters = ''
printList = []
cuandoEntonsList = []
defRutinas = []

def returnVariables():
    return variables

def returnMoves():
    return moves

def returnPrintList():
    return printList
        
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

    def returnVariable(self):
        return 'SET' + self.name

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
            print("Error semantico, no se pueden hacer operaciones booleanas con numeros")
    print(variables)

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
        

    print(moves)

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

    print(moves)

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
    print(printParameters)

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

def ifVerifier(condition, block, block2):
    #print(str(conditionVerifier(condition)))
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
        print('--Entered if is false--')
        for i in block:
            if i.startswith('SET'):
                i = i.replace('SET', '')
                for key, value in variables.items():
                    if key == i:
                        variables.pop(i)
                        break

                print(variables)

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
                print('Variables after if is false: ' + str(variables))
            elif i.startswith('print'):
                i = i.replace('print', "")
                #print(i)
                for j in printList:
                    if j == i:
                        printList.remove(j)
                        break
                print(printList)

            elif i.startswith('move'):
                i = i.replace('move', '')
                moves.reverse()
                moves.remove(i)
                moves.reverse()

                print(moves)

    elif conditionVerifier(condition):
        print('--Entered if is true--')
        for i in block2:
            if i.startswith('SET'):
                i = i.replace('SET', '')
                for key, value in variables.items():
                    if key == i:
                        variables.pop(i)
                        break

                print(variables)

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
                print('Variables after if is false: ' + str(variables))
            elif i.startswith('print'):
                i = i.replace('print', "")
                print(i)
                for j in printList:
                    if j == i:
                        printList.remove(j)
                        break
                print(printList)

            elif i.startswith('move'):
                i = i.replace('move', '')
                moves.reverse()
                moves.remove(i)
                moves.reverse()

                print(moves)
                        
    return str(conditionVerifier(condition))

def ifVerifier2(condition, block):
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
        print('--Entered if is false--')
        for i in block:
            if i.startswith('SET'):
                i = i.replace('SET', '')
                for key, value in variables.items():
                    if key == i:
                        variables.pop(i)
                        break

                print(variables)

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
                print('Variables after if is false: ' + str(variables))
            elif i.startswith('print'):
                i = i.replace('print', "")
                #print(i)
                for j in printList:
                    if j == i:
                        printList.remove(j)
                        break
                print(printList)

            elif i.startswith('move'):
                i = i.replace('move', '')
                moves.reverse()
                moves.remove(i)
                moves.reverse()

                print(moves)

    elif conditionVerifier(condition):
        for i in block:
            cuandoEntonsList.append(i)

        cuandoEntonsList.append('END')
        
                        
    return str(conditionVerifier(condition))

def forVerifier(id, factor, num, block):
    idTemp = id
    factorTemp = factor

    #print(str(id) + ',' + str(factor) + ',' + str(num))

    for key, value in variables.items():
        if key == idTemp and value[1] == 'num':
            idTemp = value[0]
        elif key == idTemp and value[1] == 'bool':
            print("Error semantico, no se pueden usar booleanos en ciclos For 1")
            return 'Error'
        elif key != idTemp:
            pass
        
    for key, value in variables.items():
        if key == factorTemp and value[1] == 'num':
            factorTemp = value[0]
        elif key == factorTemp and value[1] == 'bool':
            print("Error semantico, no se pueden usar booleanos en ciclos For 2")
            return 'Error'
        elif key != factorTemp:
            pass
    
    #print(factorTemp)

    if idTemp.find('@') != -1:
        idTemp = 1
    if factorTemp.find('@') != -1:
        print("Error semantico, no se pueden usar booleanos en ciclos For o variable maxima no definida")
        return 'Error'

    block = block.replace(";", ",")
    block = block.split(",")
    blockTemp = block

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
            
            if int(idTemp) <= int(factorTemp) + 1:
                for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
                    idTemp = x
                varDeclaration(i, idTemp)
            else:
                return ''

            print(variables)

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

            print('Variables after for: ' + str(variables))

        elif i.startswith('print'):
            i = i.replace('print', "")
            for j in printList:
                if j == i:
                    printList.remove(j)
                    break
            #iTemp = re.split(r'd+', i)
            if int(idTemp) <= int(factorTemp) + 1:
                for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
                        if j == value[0]:
                            iTemp2 = i.replace(j, x)
                            printList.append(iTemp2)

            print(printList)

        elif i.startswith('move'):
            i = i.replace('move', '')
            moves.reverse()
            moves.remove(i)
            moves.reverse()

            if int(idTemp) <= int(factorTemp) + 1:
                for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
                    moves.append(i)
            else:
                return ''

            print(moves)

    #print(str(idTemp) + str(factorTemp))
    
    if int(idTemp) <= int(factorTemp) + 1:
        for x in range(int(idTemp), int(factorTemp) + 1, int(num)):
            print(x)
    else:
        return ''
    
def enCasoVerifier(boolString, block):
    boolString = boolString.split(";")

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
        print('--Entered if is false--')
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

                print(moves)
                        
    return 'En caso'

def enCasoVerifier2(boolString, block):
    global cuandoEntonsList
    boolString = boolString.split(";")

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
        print('--Entered entons is true--')
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

                print(moves)

    if boolString.count("True") >= 2:
        print("--Entered entons is true 2--")
        check = True
        cuandoEntonsList.reverse()
        #print('CuandoEntonsList2: ' + str(cuandoEntonsList))
        for i in cuandoEntonsList:
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

                print(moves)

            if i.startswith("END"):
                if check:
                    check = False
                    pass
                elif not(check):
                    break
                        
    cuandoEntonsList.clear()
    return 'En caso2'