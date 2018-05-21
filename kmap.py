import argparse
from truthtable import truthtable
import sys

class kmap(object):
    def __init__(self,minvalues,*kwargs):
        '''takes a minvales as a list or space seperated string'''
        if isinstance(minvalues,str):
            self.minvalues=[int(i) for i in minvalues.split()]
            self.lenghtOftable=max(self.minvalues)
        else:
            self.minvalues=minvalues
            self.lenghtOftable=max(self.minvalues)
        self.table=truthtable(self.lenghtOftable,self.minvalues)
        self.column=None
        self.row=None
        self.dictColumn=None
        self.dictRow=None
        self.kmapTable=None
        self.createKmap()

    def createKmap(self):
        self.calculateRowAndColumnForMap()
        self.kmapTable=[[0 for i in range(len(self.column))] for i in range(len(self.row))]
        #sets the ones
        for row in range(self.table.lenghtoftable):
            if self.table.table[row][self.table.numberofvariables]==1:
                therow=self.getRow(row)
                self.setMap(therow)
        print()
        for i in range(len(self.kmapTable)):
            print(self.kmapTable[i])
        
        print()
        self.getLargestsOnes()

    def calculateRowAndColumnForMap(self):
        variables=self.table.numberofvariables
        
        if variables-2==0:
            self.column=['0','1']
            self.dictColumn={self.column[i]:i for i in range(len(self.column))}
            self.row=['0','1']
            self.dictRow={self.row[i]:i for i in range(len(self.row))}
        elif variables-2>0:
            self.column=['00','01','11','10']
            if variables-2==2:
                self.row=['00','01','11','10']
            elif variables-2==1:
                self.row=['0','1']
            else:
                raise ValueError("invalid number of variable")
            self.dictColumn={self.column[i]:i for i in range(len(self.column))}
            self.dictRow={self.row[i]:i for i in range(len(self.row))}
       
          
    def getRow(self,row):
        if self.table is None:
            return
        return "".join([str(i)  for i in self.table.table[row]][:-1])

    def setMap(self,row):
        if len(row)==2:
            r=row[0]
            c=row[1]
            self.kmapTable[self.dictRow[r]][self.dictColumn[c]]=1
        elif len(row)==3:
            r=row[0]
            c=row[1:]
            self.kmapTable[self.dictRow[r]][self.dictColumn[c]]=1
        elif len(row)==4:
            r=row[:2]
            c=row[2:]
            self.kmapTable[self.dictRow[r]][self.dictColumn[c]]=1
        else:
            raise ValueError("unsupported operation")

    def getLargestsOnes(self):
        ones=[]
        for row in range(len(self.kmapTable)):
            for column in range(len(self.kmapTable[0])):
                if self.kmapTable[row][column]==1:
                    thisone=[]
                    #check for single columns or rows
                    thisone+=self.checkSingleRowORColumn(row,column,2)
                    thisone+=self.checkSingleRowORColumn(row,column,4)
                    #checks for  square boxes
                    thisone+=self.checkSquaredRowORColumn(row,column,2,2)
                    thisone+=self.checkSquaredRowORColumn(row,column,2,4)
                    thisone+=self.checkSquaredRowORColumn(row,column,4,2)
                    thisone+=self.checkSquaredRowORColumn(row,column,4,4)
                    thisone=sorted(thisone,key=lambda x:(abs(x[0]-x[1])+abs(x[2]-x[3]))*abs(x[2]-x[3]))
                    
                    if thisone:
                        r1,r2,c1,c2=thisone[-1]
                        self.fillTaken(r1,r2,c1,c2)
                        ones.append(thisone[-1])
                    else:
                        self.kmapTable[row][column]="d"
                        ones.append((row,row,column,column))

        print()
        print(self.solve(ones))
        

    def checkSingleRowORColumn(self,row,column,size):
        squaredCoordinates=[]
        if size<=len(self.column):
            t=True
            for c in range(column,column+size):
                t=self.kmapTable[row][c%len(self.column)]!=0 and t
            if t:
                squaredCoordinates.append((row,row,column,column+size-1))
        if size<=len(self.row):
            t=True
            for r in range(row,row+size):
                t=self.kmapTable[r%len(self.row)][column]!=0 and t
            if t:
                squaredCoordinates.append((row,row+size-1,column,column))
        return squaredCoordinates

    def checkSquaredRowORColumn(self,row,column,rowSize,columnSize):
        squaredCoordinates=[]
        
        if rowSize <=len(self.kmapTable) and  columnSize<=len(self.kmapTable[0]):
            t=True
            for r in range(row,row+rowSize):
                for c in range(column,column+columnSize):
                    t=self.kmapTable[r%len(self.row)][c%len(self.column)]!=0 and t
            if t:
                squaredCoordinates.append((row,row+rowSize-1,column,column+columnSize-1))
        return squaredCoordinates

    def fillTaken(self,r1,r2,c1,c2):
        for r in range(r1,r2+1):
            for c in range(c1,c2+1):
                self.kmapTable[r%len(self.row)][c%len(self.column)]="d"

    def solve(self,ones):
        ans=""
        for data in ones:
            r1,r2,c1,c2=data
            row=self.row[r1:min(len(self.row),r2+1)]+self.row[0:r2+1-len(self.row)]
            column=self.column[c1:min(len(self.column),c2+1)]+self.column[0:c2+1-len(self.column)]
            
            a,b,x,y=None,None,None,None

            if len(self.row[0])==2:
                a,b=row[0]
                x,y=True,True
                for r in row:
                    x=a==r[0] and x
                    y=b==r[1] and y
            else:
                a=row[0]
                x=True
                for r in row:
                    x=a==r and x
            ans+="a" if x and a=="1" else ""
            ans+="a'" if x and a=="0" else ""
            ans+="b" if y  and b=="1" else ""
            ans+="b'" if y  and b=="0" else ""

        
            if len(self.column[0])==2:
                a,b=column[0]
                x,y=True,True
                for c in column:
                    x=a==c[0] and x
                    y=b==c[1] and y
            else:
                a=column[0]
                x=True
                for c in column:
                    x=a==r and x

            ans+="c" if x and a=="1" else ""
            ans+="c'" if x and a=="0" else ""
            ans+="d" if y  and b=="1" else ""
            ans+="d'" if y  and b=="0" else ""
            ans+="+"

        ans=ans[:len(ans)-1]
        return ans
                    
k=kmap([1,2,3])
    