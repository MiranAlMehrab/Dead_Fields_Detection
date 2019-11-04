import os
import time
import glob
import javalang
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


fileDirectory = None
declaredVariableList = []
usedVariableList = []

globalDeclaredVariableList = []
globalUsedVariableList = []

inFunctionDeclaredVariableList = []
inFunctionUsedVariableList = []

unusedGlobalVariableList = []
unusedLocalVariableList = []

allVariableListWithLineNumber = []

finalOutPutList = []

def clearLists():
    globalDeclaredVariableList.clear()
    globalUsedVariableList.clear()
    inFunctionDeclaredVariableList.clear()
    inFunctionUsedVariableList.clear()
    allVariableListWithLineNumber.clear()


def computeUnusedGlobalVariable():
    for variable in globalUsedVariableList:
        if(variable in globalDeclaredVariableList):
            globalDeclaredVariableList.remove(variable)

def computeUnusedLocalVariable():
    #print(inFunctionUsedVariableList)
    index = 0
    for variables in inFunctionUsedVariableList:
        for variable in variables:
            if(variable in inFunctionDeclaredVariableList[index]):
                inFunctionDeclaredVariableList[index].remove(variable)
            if(variable in globalDeclaredVariableList):
                globalDeclaredVariableList.remove(variable)


        index = index + 1


def printnewLine(limit):
    for iterator in range(0,limit):
        print(' ')


def printVariabeList(message,variabeList):
    print(message)
    for variable in variabeList:
        print(variable)



def readFileDirectory(fullPath):
    global fileDirectory
    fileDirectory = glob.iglob(fullPath,recursive=True)
    #fileDirectory = glob.iglob('C:/Users/Miran Al Mehrab/Desktop/javaLang/**/*.java', recursive=True)


def printMessage(message, variableName):
    print(message,' : ',variableName)


def writeVariableToFile(sourceCodeFileName):

    outputFileName = separateFileNameFromDirectoryName(sourceCodeFileName)
    outputFileName = outputFileName.replace('.txt','.csv')
  
    filePointer = open(outputFileName,'w')  

    filePointer.write('variable name,line number'+'\n')
    for variable in globalDeclaredVariableList:
        for line in allVariableListWithLineNumber:
            if(variable == line[0]):
                print('match found')
                print(variable,' line number:',line[1])
                filePointer.write(variable+','+str(line[1])+'\n')
                break

    for lines in inFunctionDeclaredVariableList:
        if(len(lines)>0):
            for variable in lines:
                for line in allVariableListWithLineNumber:
                    if(variable == line[0]):
                        filePointer.write(variable+','+str(line[1])+'\n')
                        break
    filePointer.close()

    # declaredVariableList.append(inFunctionDeclaredVariableList.copy())
    # declaredVariableList.append(globalDeclaredVariableList.copy())
    # writeToFile('Declared'+outputFileName,declaredVariableList)

    # usedVariableList.append(inFunctionUsedVariableList.copy())
    # usedVariableList.append(globalUsedVariableList.copy())
    # writeToFile('Used'+outputFileName,usedVariableList)





def separateFileNameFromDirectoryName(fileName):
    currentFile = str(fileName).split('/')
    currentFile = currentFile[len(currentFile)-1]
    currentFile = currentFile.split('\\')
    currentFile = currentFile[len(currentFile)-1]
    outputFile = currentFile.replace('.java','.txt')
    return outputFile


def writeToFile(outputFileName,fileElementList):
    filePointer = open(outputFileName,'w')
    for lineList in fileElementList:
        for line in lineList:
            str_line = ""
            for i in line:
                if( type(str_line) is None):
                    str_line = i
                else:
                    str_line = str_line + i + ','
            str_line = str_line+'\n'
            filePointer.write(str_line)

    filePointer.close()
    fileElementList.clear()



def addFromBodyListToVariableList(sourceBodyList):
    destinationVariableList = []
    for variableBody in sourceBodyList:
            if(variableBody.member not in destinationVariableList):
                destinationVariableList.append(variableBody.member)
    return destinationVariableList



def addFromVraibleListToUsedOrDeclaredList(sourceList,destinationList):
    for variable in sourceList:
        if(variable not in destinationList):
            destinationList.append(variable)



def handleBinaryOperation(treeNode,tempVariableList):

    leftVariableBodyList = []
    rightVariableBodyList = []

    if(type(treeNode) is javalang.tree.BinaryOperation):

        rightVariable_body = treeNode.operandr
        leftVariable_body = treeNode.operandl

        # check all the left variable for searching for binary useage
        while True:
            if(type(leftVariable_body) is javalang.tree.BinaryOperation):
                if(type(leftVariable_body.operandl) is javalang.tree.MemberReference):
                    leftVariableBodyList.append(leftVariable_body.operandl)
                if(type(leftVariable_body.operandr) is javalang.tree.MemberReference):
                    leftVariableBodyList.append(leftVariable_body.operandr)

                leftVariable_body = leftVariable_body.operandl

            elif(type(leftVariable_body) is javalang.tree.MemberReference):
                leftVariableBodyList.append(leftVariable_body)
                break
            elif(type(leftVariable_body) is javalang.tree.Literal):
                break
            elif(type(leftVariable_body) is javalang.tree.MethodInvocation):
                handleMethodInvocation(leftVariable_body,tempVariableList)
                break
            else:
                break

        # check all the right variable for searching for binary useage
        while True:
            if(type(rightVariable_body) is javalang.tree.BinaryOperation):
                if(type(rightVariable_body.operandl) is javalang.tree.MemberReference):
                    rightVariableBodyList.append(rightVariable_body.operandl)
                if(type(rightVariable_body.operandr) is javalang.tree.MemberReference):
                    rightVariableBodyList.append(rightVariable_body.operandr)

                rightVariable_body = rightVariable_body.operandr
            elif(type(rightVariable_body) is javalang.tree.MemberReference):
                rightVariableBodyList.append(rightVariable_body)
                break
            elif(type(rightVariable_body) is javalang.tree.Literal):
                break
            elif(type(rightVariable_body) is javalang.tree.MethodInvocation):
                handleMethodInvocation(rightVariable_body,tempVariableList)
                break
            else:
                break

            
        leftVariableList = addFromBodyListToVariableList(leftVariableBodyList)
        rightVariableList = addFromBodyListToVariableList(rightVariableBodyList)


        addFromVraibleListToUsedOrDeclaredList(leftVariableList,tempVariableList)
        addFromVraibleListToUsedOrDeclaredList(rightVariableList,tempVariableList)

        #for variable in usedVariableList:
            #print(variable)



def handleMemberReference(treeNode,tempVariableList):
    #print(treeNode.member)
    tempVariableList.append(treeNode.member)


def handleDeclaredVariable(treeNode,tempDeclarationVariableList,tempUsedVariableList):
    
    variableName = treeNode.declarators[0].name
    lineNumber = treeNode.position.line
    print(variableName)
    print(lineNumber)

    allVariableListWithLineNumber.append([variableName,lineNumber])
    
    #variableType = treeNode.type.name
    tempDeclarationVariableList.append(variableName)

    if(type(treeNode.declarators[0].initializer) is javalang.tree.MemberReference):
        usedVaraibleName = treeNode.declarators[0].initializer.member
        tempUsedVariableList.append(usedVaraibleName)

    elif(type(treeNode.declarators[0].initializer) is javalang.tree.BinaryOperation):
        handleBinaryOperation(treeNode.declarators[0].initializer,tempUsedVariableList)

    elif(type(treeNode.declarators[0].initializer) is javalang.tree.MethodInvocation):
        #print(type(treeNode.declarators[0].initializer.arguments))
        if(len(treeNode.declarators[0].initializer.arguments) > 0):
            if(type(treeNode.declarators[0].initializer.arguments[0]) is javalang.tree.MemberReference):
                handleMemberReference(treeNode.declarators[0].initializer.arguments[0],tempUsedVariableList)
            elif(type(treeNode.declarators[0].initializer.arguments[0]) is javalang.tree.BinaryOperation):
                handleBinaryOperation(treeNode.declarators[0].initializer.arguments[0],tempUsedVariableList)


def handleQualifier(treeNode,tempVariableList):
    #time.sleep(3)
    print(treeNode.qualifier)
    if(treeNode.qualifier not in tempVariableList):
        #time.sleep(3)
        print(treeNode.qualifier)

        tempVariableList.append(treeNode.qualifier)

def handleMethodInvocation(treeNode,tempVariableList):
    if(len(treeNode.arguments) > 0):
        #print(treeNode.arguments)
        for i in range(0,len(treeNode.arguments)):
            if(type(treeNode.arguments[i]) is javalang.tree.MemberReference):
                handleMemberReference(treeNode.arguments[i],tempVariableList)
            elif(type(treeNode.arguments[i]) is javalang.tree.BinaryOperation):
                handleBinaryOperation(treeNode.arguments[i],tempVariableList)

    if(len(treeNode.qualifier) > 0):
        handleQualifier(treeNode,tempVariableList)




def handleReturnStatement(treeNode,tempDeclaredVaraibleList,tempUsedVraiableList):
    #print(treeNode)
    if(type(treeNode.expression) is javalang.tree.MemberReference):
        usedVariableName = treeNode.expression.member
        #usedVariableNode = [usedVariable,',',variableType]
        tempUsedVraiableList.append(usedVariableName)
        #print(usedVariable)

    elif(type(treeNode.expression) is javalang.tree.BinaryOperation):
        handleBinaryOperation(treeNode.expression,tempUsedVraiableList)

    elif(type(treeNode.expression) is javalang.tree.MethodInvocation):
        #print('method invocation in return statememnt')
        #print(treeNode.expression)
        handleMethodInvocation(treeNode.expression,tempUsedVraiableList)

#def handleObject(treeNode,tempUsedVariableList):


def handleStatementInMetheod(body,tempDeclaredVaraibleList,tempUsedVraiableList):
    print(body)
    printnewLine(2)

    if(type(body.expression) is javalang.tree.MemberReference):
        usedVariable = body.expression.member
        handleMemberReference(usedVariable,tempUsedVraiableList)
        #print('Used variable', usedVariable)
    elif(type(body.expression) is javalang.tree.Assignment):
        #assignedVariableName = body.expression.expressionl.member
        #print('Assigned variable',assignedVariableName)
        #time.sleep(3)
        #print(body.expression.value)
        #time.sleep(4)
        handleBinaryOperation(body.expression.value,tempUsedVraiableList)
    elif(type(body.expression) is javalang.tree.MethodInvocation):
        print('here i come')
        #print(body.expression)
        handleMethodInvocation(body.expression,tempUsedVraiableList)


def handleCondition(treeNode,tempUsedVraiableList):
    #print(treeNode)
    if(type(treeNode.condition) is javalang.tree.BinaryOperation):
        handleBinaryOperation(treeNode.condition,tempUsedVraiableList)
    elif(type(treeNode.condition) is javalang.tree.MemberReference):
        handleMemberReference(treeNode.condition,tempUsedVraiableList)


def handleMethod(treeNode,tempDeclaredVaraibleList,tempUsedVraiableList):

    if(type(treeNode.body) != type(None)):

        for body in treeNode.body:
            #print(body)

            if(type(body) is javalang.tree.LocalVariableDeclaration):
                handleDeclaredVariable(body,tempDeclaredVaraibleList,tempUsedVraiableList)

            elif(type(body) is javalang.tree.ReturnStatement):
                variableType = treeNode.return_type.name
                #print(variableType)
                handleReturnStatement(body,tempDeclaredVaraibleList,tempUsedVraiableList)

            elif(type(body) is javalang.tree.StatementExpression):
                #print(treeNode.body[0])
                #print('statement found')
                handleStatementInMetheod(body,tempDeclaredVaraibleList,tempUsedVraiableList)
                #printMessage('Usage','statement expression')

            elif(type(body) is javalang.tree.IfStatement):
                #print('condition found')
                handleCondition(body,tempUsedVraiableList)
            #if(type(body) is javalang.tree.WhileStatement or type(body) is javalang.tree.DoStatement or type(body) is javalang.tree.ForStatement):
                #handleLoop(body)


    #print(treeNode.body[0].expression.operator)







def handleLoop(treeNode):
    printnewLine(2)

    if(type(treeNode) is javalang.tree.ForStatement):
        #print(treeNode)
        printnewLine(1)
        #print(treeNode.body.statements[0].expression)

        # usedVariableName = treeNode.body[0].statements
        # print(usedVariableName)
    elif(type(treeNode) is javalang.tree.WhileStatement):
        #print(treeNode)
        printnewLine(1)
        #print(treeNode.body.statements[0].expression.member)
        # usedVariableName = treeNode.body[0]#.#statements.expression#.member
        # print(usedVariableName)
    elif(type(treeNode) is javalang.tree.DoStatement):
        #print(treeNode)
        printnewLine(1)
        #print(treeNode.body.statements[0].expression.arguments.member)
        #usedVariableName = treeNode.body[0].statements.expression.arguments.member




def handleConstructor(treeNode,tempUsedVraiableList):
    print('Constructor : ',treeNode.name)
    for body in treeNode.body:
        if(type(body.expression.value) is javalang.tree.MemberReference):
            #assignedVariableName = body.expression.expressionl.selectors.member
            #declaredVariableList.append([assignedVariableName,',','int']) #int here is assumed
            print(body.expression.expressionl.selectors[0].member)

        elif(type(body.expression.value) is javalang.tree.BinaryOperation):
            print(body.expression.expressionl.selectors[0].member)
            #handleBinaryOperation(body.expression.value,tempUsedVraiableList) #int here is assumed



def removeEmptyList(variableList):
    for line in variableList:
        if(len(line) == 0):
            variableList.remove(line)


def trimList():
    removeEmptyList(globalDeclaredVariableList)
    removeEmptyList(globalUsedVariableList)
    removeEmptyList(inFunctionDeclaredVariableList)
    removeEmptyList(inFunctionUsedVariableList)



def checkAllFilesFromDirectory():

    for sourceCodeFileName in fileDirectory:

        try:
            #print(sourceCodeFileName)
            fileContent = open(sourceCodeFileName,'r')
            sourceTree = javalang.parse.parse(fileContent.read())
            sourceFileImports = sourceTree.imports


            for treeNode in sourceTree.types[0].body:

                if(type(treeNode) is javalang.tree.FieldDeclaration):
                    #print(treeNode)
                    handleDeclaredVariable(treeNode,globalDeclaredVariableList,globalUsedVariableList)

                elif(type(treeNode) is javalang.tree.MethodDeclaration):
                    #print(treeNode)
                    tempUsedVraiableList = []
                    tempDeclaredVaraibleList = []
                    #print(treeNode.annotations[0].name)
                    #if(treeNode.annotations[0].name is 'Test'):
                    handleMethod(treeNode,tempDeclaredVaraibleList,tempUsedVraiableList)

                    #print(tempDeclaredVaraibleList)
                    #print(tempUsedVraiableList)

                    #if(len(tempDeclaredVaraibleList)>0):
                    inFunctionDeclaredVariableList.append(tempDeclaredVaraibleList.copy())
                    #if(len(tempUsedVraiableList)):
                    inFunctionUsedVariableList.append(tempUsedVraiableList.copy())

                    tempDeclaredVaraibleList.clear()
                    tempUsedVraiableList.clear()

                #elif(type(treeNode) is javalang.tree.ConstructorDeclaration):
                    #handleConstructor(treeNode)


            

            outputFileName = separateFileNameFromDirectoryName(sourceCodeFileName)
            outputFileName = outputFileName.replace('.txt','.java')
            
            print('Source File Name: ',outputFileName)
            
            print(allVariableListWithLineNumber)
            #printVariabeList('All declared Varible List',globalDeclaredVariableList)
            #printVariabeList('All Used Varible List',globalUsedVariableList)
            printVariabeList('All declared Varible List in function',inFunctionDeclaredVariableList)
            printVariabeList('All Used Varible List in function',inFunctionUsedVariableList)

            computeUnusedGlobalVariable()
            computeUnusedLocalVariable()

            writeVariableToFile(sourceCodeFileName)


            #trimList()
            #print('passed trim')
            printVariabeList('Unused global variable',globalDeclaredVariableList)
            printVariabeList('Unused local variable',inFunctionDeclaredVariableList)
            addScrollBarToFrame(sourceCodeFileName)
            clearLists()
        except:
            print('Error in file parsing!')

    print('Finding all the dead field is finished!')

def main():
    checkAllFilesFromDirectory()



##################################################################
root = Tk()
root.geometry("800x500")
root.title("Dead Fields Test")

frame = Frame(root) #adding a frame
frame.pack()

bottomframe = Frame(root)
bottomframe.pack(side = TOP)

scrollbar = Scrollbar(bottomframe)
scrollBoxList = Listbox(bottomframe,height='25',width='66',font="Verdana 10 bold", yscrollcommand = scrollbar.set)

scrollbar.pack( side = RIGHT, fill = Y )
scrollBoxList.pack( side = TOP , fill = BOTH )
scrollbar.config( command = scrollBoxList.yview )



def addScrollBarToFrame(sourceFileName):

    # for line in deadFieldList:
    #     if(len(line) > 0):
    #         scrollBoxList.insert(END, str(line))
    # #scrollBoxList.insert(END,'\n')

    fileName = separateFileNameFromDirectoryName(sourceFileName)
    fileName = fileName.replace('.txt','.java')
    firstLine = 'File name : '+fileName

    scrollBoxList.insert(END,firstLine,'\n')
    scrollBoxList.insert(END,'variable name   line number')

    for variable in globalDeclaredVariableList:
        for line in allVariableListWithLineNumber:
            if(variable == line[0]):
                scrollBoxList.insert(END,variable+str(line[1]).rjust(30)+'\n')
                break

    for lines in inFunctionDeclaredVariableList:
        if(len(lines)>0):
            for variable in lines:
                for line in allVariableListWithLineNumber:
                    if(variable == line[0]):
                        scrollBoxList.insert(END,variable+str(line[1]).rjust(30)+'\n')
                        break
    
    scrollBoxList.insert(END,'\n')


    
    global space_left_for_scroll_bar
    space_left_for_scroll_bar = False



def clearCLI():
    os.system('cls' if os.name == 'nt' else 'clear')


def clearScrollBar():
    global space_left_for_scroll_bar
    space_left_for_scroll_bar = True
    scrollBoxList.delete(0,'end')
    #scrollBoxList.pack_forget()
    #scrollbar.pack_forget()




def findDeadField():
    if(fileDirectory is None):
        messagebox.showerror("Error", "File Directory is Empty!")
    else:
        main()


def addProject():
    file_directory = filedialog.askdirectory()+'/**/*Test.java'
    readFileDirectory(file_directory)
    clearScrollBar()

    #print(file_directory)

def exitProgram():
    print('Ha Ha Ha!')
    clearCLI()
    root.destroy()


addProjectButton = Button(frame,text='Add Project', height='1', width='12',font="Verdana 13 bold",fg = 'green',command = lambda: addProject())
testButton = Button(frame,text='Test Project', height='1', width='12',font="Verdana 13 bold",fg = 'green',command = lambda: findDeadField())
clearButton = Button(frame,text='Clear',height='1',width='12',font="Verdana 13 bold",fg = 'green',command = lambda:clearScrollBar())
exitButton = Button(frame,text='Exit',height='1',width='12',font="Verdana 13 bold",fg = 'green',command = lambda:exitProgram())


addProjectButton.pack(side=LEFT)
testButton.pack(side=LEFT)
clearButton.pack(side=LEFT)
exitButton.pack(side=LEFT)


space_left_for_scroll_bar = True


mainloop()


##################################################################
