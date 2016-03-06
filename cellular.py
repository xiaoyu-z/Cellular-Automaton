__author__ = 'zhengxiaoyu'
import numpy as np
import sys
#first step : convert the input value to binary
def toBinary(num, bit):
    '''
    :param num: the inuput num
    :param bit: n-bit
    :return:the binary list in n-bit
    >>> toBinary(6,3)
    [1, 1, 0]
    >>> toBinary(8,2)
    bit too samll
    >>> toBinary(16, 8)
    [0, 0, 0, 1, 0, 0, 0, 0]
    '''
    if num > 255 or num <0 or pow(2,bit)<= num:
        print("bit too samll")
        return
    binaryList = []
    for i in range(bit):
        if(num%2==1):
            binaryList.append(1)
            num = int(num/2)
        else:
            binaryList.append(0)
            num = int(num/2)
    binaryList.reverse()
    #print(binaryList)
    return binaryList

#secodn step: determine the rule:
def setRule(binaryList):
    '''return a list containing eight rules
    input: the binary list

    >>> setRule([1,0,1,0,1,0,0,0])
    [([1, 1, 1], 1), ([1, 1, 0], 0), ([1, 0, 1], 1), ([1, 0, 0], 0), ([0, 1, 1], 1), ([0, 1, 0], 0), ([0, 0, 1], 0), ([0, 0, 0], 0)]
    '''
    ruleList = []
    for i in range(8):
        ruleList.append((toBinary(7-i,3),binaryList[i]))
    #print(ruleList)
    return ruleList

#third step: start from the first line
def start(columns):
    '''
    input: the columns input form the keyborad
    :return the first line of output
    >>> start(7)
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    '''
    startList = [0 for i in range(columns)] + [1] + [0 for i in range(columns)]
    return startList
def process(columns,ruleList):
    '''

    :return: the result
    input: columns and the rule list
    >>> process(4,[([1, 1, 1], 0), ([1, 1, 0], 0), ([1, 0, 1], 0), ([1, 0, 0], 1), ([0, 1, 1], 1), ([0, 1, 0], 1), ([0, 0, 1], 1), ([0, 0, 0], 0)])
    [[0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 1, 1, 0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 0, 0, 0, 1]]
    '''
    resultList =[]
    resultList.append(start(columns))
    for i in range(columns):
        newList = []
        startList = resultList[len(resultList)-1]
        for i in range(columns*2+1):
            newList.append(applyRule(ruleList,([0]+startList+[0])[i:i+3]))
        resultList.append(newList)
    return resultList
def processWolfram(columns,ruleList):
    '''
    input: columns and the rule list
    :return: the wolfram result
    >>> processWolfram(4,[([1, 1, 1], 0), ([1, 1, 0], 0), ([1, 0, 1], 0), ([1, 0, 0], 1), ([0, 1, 1], 1), ([0, 1, 0], 1), ([0, 0, 1], 1), ([0, 0, 0], 0)])
    [[0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 1], [0, 0, 1, 1, 0, 0, 1, 1, 1], [0, 1, 1, 0, 1, 1, 1, 0, 0], [1, 1, 0, 0, 1, 0, 0, 1, 1]]
    >>> processWolfram(4,setRule(toBinary(139, 8)))
    [[0, 0, 0, 0, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 1, 1, 1], [1, 1, 1, 0, 0, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1, 1, 1, 1], [1, 0, 0, 1, 1, 1, 1, 1, 1]]
    '''
    resultList =[]
    resultList.append(start(columns))
    for i in range(columns):
        newList = []
        startList = resultList[len(resultList)-1]
        for i in range(columns*2+1):
            newList.append(applyRule(ruleList,([0]+startList+[1])[i:i+3]))
        resultList.append(newList)
    return resultList
def applyRule(ruleList, input):
    '''
    apply the rule
    input: the rule list and the list with three elements
    >>> applyRule([([1, 1, 1], 0), ([1, 1, 0], 0), ([1, 0, 1], 0), ([1, 0, 0], 1), ([0, 1, 1], 1), ([0, 1, 0], 1), ([0, 0, 1], 1), ([0, 0, 0], 0)],[0,0,0])
    0
    '''
    for i in ruleList:
        if(i[0]==input):
            return i[1]

#show the output and write the output
def show(result,columns):
    '''
    print the result
    input: the result from process() or processWolfram(), columns
    >>> show(process(4,setRule(toBinary(30,8))),4)
    P1 9 5
    000010000
    000111000
    001100100
    011011110
    110010001
    '''
    formater = "%r"*(columns*2+1)
    print ("P1 "+str(columns*2+1) +" "+ str(columns+1))
    for i in result:
        i = tuple(i)
        print (formater%i)

def is_p(s):
    if len(s)==1:
        return True
    else:
        return s[0] == s[-1] and is_p(s[1:-1])
def double(x): return x*2
def mystery(arg):
    return lambda f:f(arg)

def writeFile(fileName, result, columns):
    '''
    generate the image file
    input: the image name, result, columns
    '''
    file = open(fileName, "w")
    file.write("P1 "+str(columns*2+1)+" "+str(columns+1))
    for line in result:
        file.writelines(str(i) for i in line)
        file.write('\n')
    file.close()
count =0
def interleaved_sum(n, odd_term, even_term):
        global count
        #count = n
       # count = 0
        if n > count:
            count = n
        def sum_together(n ,term_1, term_2):
            global count
            if n == count:
                count = 0
                return term_1(n)
            else:
                return term_1(n)+term_2(n+1)+sum_together(n+2, term_1, term_2)
        if n==0:
            return sum_together(0, even_term, odd_term) - even_term(0)
        elif n == 1:
            return sum_together(1, odd_term, even_term)
        else:
            return interleaved_sum(n-2,odd_term,even_term)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    if len(sys.argv) <3 :
        print("need more parameter")
        exit()
    if len(sys.argv)==3 or len(sys.argv) == 5:
        result = process(int(sys.argv[2]),setRule(toBinary(int(sys.argv[1]),8)))
    elif len(sys.argv) == 4 or len(sys.argv) == 6:
        if(sys.argv[3] == 'Wolfram'):
            result = processWolfram(int(sys.argv[2]),setRule(toBinary(int(sys.argv[1]),8)))
        else:
            print("do you mean Wolfram ?")
    show(result, int(sys.argv[2]))
    #len(sys.argv) == 6 or len(sys.argv) == 5:

    if len(sys.argv) > 4:
        if(sys.argv[len(sys.argv)-2] == '>'):
            writeFile(sys.argv[len(sys.argv)-1], result, int(sys.argv[2]))
