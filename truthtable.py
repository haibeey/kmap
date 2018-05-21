from math import log,ceil
class truthtable:
    def __init__(self,lenghtoftable,ones):
        '''takes the lenght of the table and sets it to the a power of two
            ones are the result which are one or true'''
        if self.isPowerOfTwo(lenghtoftable):
            self.lenghtoftable=lenghtoftable
        else:
            self.lenghtoftable=self.nearestPowerOfTwo(lenghtoftable)
        print(self.lenghtoftable)
        self.numberofvariables=ceil(log(lenghtoftable)/log(2))
        assert self.numberofvariables<=4,"number of varibles exceed the needed limit"
        self.ones=ones
        self.table=None
        self.buildTable()

    @staticmethod
    def isPowerOfTwo(number):
        return number&(number-1)==0
    @staticmethod
    def nearestPowerOfTwo(number):
        l=ceil(log(number)/log(2))-1
        return 2<<l
    def buildTable(self):
        self.table=[[0 for i in range(self.numberofvariables+1)] for i in range(self.lenghtoftable)]
        numberofset=self.lenghtoftable>>1
        ceil=True
        counter=1
        for column in range(self.numberofvariables):
            for row in range(self.lenghtoftable):
                self.table[row][column]= 1 if ceil else 0
                if counter==numberofset:
                    ceil=not ceil
                    counter=0
                counter+=1
            numberofset=numberofset>>1
       
        for row in range(self.lenghtoftable):
            if row+1 in self.ones:
                self.table[row][self.numberofvariables]=1
        for i in range(len(self.table)):
            print(self.table[i])
        
    
