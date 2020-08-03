#BitHash and BitVector taken from code distributed in class
from BitHash import BitHash 
from BitVector import BitVector
import pytest


class CountingBloomFilter(object):
    
    def __init__(self, numHashes,numCellsNeeded, counter):
        #numHashes
        self.__numHashes=numHashes
        #keys inserted
        self.__nItems=0
        # calculate bits per cell needed
        i=0
        num=0
        while num<counter:
            num+=2**i
            i+=1
        self.__bitsPerCell=max(i,4) 
        #size
        self.__size = numCellsNeeded*self.__bitsPerCell
        #bitVector
        self.__Vector=BitVector(size=self.__size)   
    
      
  
        
    # insert the specified key into the Bloom Filter.
    def insert(self, key):
        ans=0
        for i in range(self.__numHashes):
            self.__nItems+=1
            #set ans to be the BitHash value 
            ans=BitHash(key,ans)*self.__bitsPerCell
            final=ans%self.__size
           
            #create a mini bit vector of the cell being added too and get the int value
            new1=int(self.__Vector[final:final+self.__bitsPerCell])
            #add 1 to the int value
            new1+=1
            #create a new bit vector with the new value 
            new=BitVector(size=self.__bitsPerCell, intVal=new1)

            
            #add the number back into the bit vector 
            for i in range(self.__bitsPerCell):
                self.__Vector[final+i]=int(new[i])
       
        
                
    #remove a specified key from the Counting Bloom Filter           
    def remove(self,key):
        ans=0 
        prev=0
        for i in range(self.__numHashes):
            #set ans to be the BitHash value 
            ans=BitHash(key,ans)*self.__bitsPerCell
            final=ans%self.__size
            
            
            #create a BitVector with the correct number of bits per cell that equals 0 
            zeroVector=BitVector(size=self.__bitsPerCell,intVal=0,)
            #if the key is not in the CBM - it cant be removed so return False
            if self.__Vector[final:final+self.__bitsPerCell]==zeroVector:
                return False
            #subtract the size set by 1 
            self.__nItems-=1
            #create a mini bit Vector with the bits of the cell being subtracted
            new1=int(self.__Vector[final:final+self.__bitsPerCell])
            #subtract the int value by 1
            new1-=1
            #create a new bit vector with the new number 
            new=BitVector(size=self.__bitsPerCell, intVal=new1)            
                  
            #add the number back into the bit vector 
            for i in range(self.__bitsPerCell):
                self.__Vector[final+i]=int(new[i])
                        
        #if the key was succesfully deleted return True
        return True
        
    # Returns True if key MAY have been inserted into the Counting Bloom filter.
    # n or more times
    # Returns False if key definitely hasn't been inserted into the CBF.   
    def find(self, key,n):
        ans=0
        count=[0]*self.__numHashes
        for i in range(self.__numHashes):
            
            ans=BitHash(key,ans)*self.__bitsPerCell
            final=ans%self.__size
          
            #create a BitVector with the correct number of bits per cell that equals 0 
            zeroVector=BitVector(size=self.__bitsPerCell,intVal=0,)          
            #if zero is found in the BitHash(final) loaction in Vector,then the key 
            #has not been inserted 
            if self.__Vector[final:final+self.__bitsPerCell]==zeroVector:
                return False
            #create a temp that equal the bits of the cell 
            temp=str(self.__Vector[final:final+self.__bitsPerCell])
            #reverse the temp inorder to add correctly
            temp=temp[::-1]
       
            #calculate how many times the key was inserted 
            for j in range(len(temp)):
                if temp[j]==str(1):
                    count[i]+=2**j
                    
        #if the min of the count is greater then n , then it is in CBM n or more times
        if min(count)>=n:
            return True 
         
        return False
        
        
       

    # Returns the current number of keys inserted in this Counting Bloom Filter
    def numSet(self):
        return self.__nItems
        


       

    


#pytests
#___________________________test insert________________________________________
#test insert of 1 
def test_insert1():
    numHashes = 4
    #max inserts per cell
    counter=1
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded, counter)
    
    Bloom.insert("Hadas")
    
    assert Bloom.find("Hadas",1)
#test the insert or 2 differnt keys   
def test_insert2diff():
    numHashes = 4
    #max inserts per cell
    counter=1
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded,counter)
    
    Bloom.insert("Hadas")
    Bloom.insert("Zev")
    #make sure Hadas was inserted 
    assert Bloom.find("Hadas",1) 
    
#test the insert of 2 different keys part 2
def test_insert2diffPart2():
    numHashes = 4
    #max inserts per cell
    counter=1
    numCellsNeeded=10
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded,counter)
    
    Bloom.insert("Hadas")
    Bloom.insert("Zev")
    
    #make sure zev was inserted
    assert Bloom.find("Zev",1)

    
#insert the same key 2 times
def test_insertSame2():
    numHashes = 4
    #max inserts per cell
    counter=2
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter(numHashes,numCellsNeeded, counter)
    
    Bloom.insert("Hadas")
    Bloom.insert("Hadas")
    
    assert Bloom.find("Hadas",2)    
    
#insert many of the same
def test_manyinsertsofSame():  
    numHashes = 4
    #max inserts per cell
    counter=35
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter(numHashes, numCellsNeeded,counter)
    for i in range(35):
        Bloom.insert("Hadas")

    
    assert Bloom.find("Hadas",35)
    
#insert many of different keys 
def test_manyInsertOfDiff():
    numHashes = 4
    #max inserts per cell
    counter=35
    numCellsNeeded=12
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded, counter)
    for i in range(20):
        Bloom.insert("Hadas")
        Bloom.insert("Mom")
        Bloom.insert("Dad")
        
    #asserts that Hadas was inserted 10 or more times
    assert Bloom.find("Hadas",10)   
    
#insert many of different keys  part 2
def test_insertManyDiffPart2():
    numHashes = 4
    #max inserts per cell
    counter=35
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded,counter)
    for i in range(20):
        Bloom.insert("Hadas")
        Bloom.insert("Mom")
        Bloom.insert("Dad")
    #make sure Mom was inserted more then 15 times 
    assert Bloom.find("Mom", 15)  
    
#insert many of different keys    part 3
def test_insertManyDiffPart3():
    numHashes = 4
    #max inserts per cell
    counter=35
    numCellsNeeded=100

    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded, counter)
    for i in range(30):
        Bloom.insert("Hadas")
        Bloom.insert("Mom")
        Bloom.insert("Dad")
    #make sure Dad was inserted 20 or more times
    assert Bloom.find("Dad", 30)  
    
    
    
#test the size after the insert is +1
def test_sizeAfterInsert():
    numHashes = 1
    #max inserts per cell
    counter=1
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded, counter)
    
    Bloom.insert("Hadas")
    size1=Bloom.numSet()
    Bloom.insert("Zev")
    size2=Bloom.numSet()
    assert (size2-size1)==1
    
      
    
#_________________________________test find____________________________________
#test the find doesnt find keys that were not inserted 
def test_find():
    numHashes = 4
    #max inserts per cell
    counter=35
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded,counter)
    for i in range(35):
        Bloom.insert("Hadas")
    
    assert Bloom.find("Aryeh",5)==False
    
#test the find key only finds the key the right number of times 
def test_findtimes():
    numHashes = 4
    #max inserts per cell
    counter=35
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded,counter)
    for i in range(35):
        Bloom.insert("Hadas")
    assert Bloom.find("Hadas",40)==False
    
#test the find key only finds the key the right number of times
    numHashes = 4
    #max inserts per cell
    counter=35
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded, counter)
    for i in range(35):
        Bloom.insert("Hadas")
    assert Bloom.find("Hadas",35)

#___________________________________test remove_________________________________   
#test removing 1    
def test_remove():
    numHashes = 4 
    #max inserts per cell
    counter=1
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded,counter)
    
    Bloom.insert("Hadas")
   
    
    assert Bloom.remove("Hadas")

#test removing many 
def test_removeMany():
    numHashes = 4
    #max inserts per cell
    counter=35
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded, counter)
    for i in range(35):
        Bloom.insert("Hadas")
    for i in range(35):
        Bloom.remove("Hadas")
    assert Bloom.find("Hadas",35)==False 

#test removing keys 
def test_removeDifferent():
    numHashes = 4
    #max inserts per cell
    counter=35
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter(numHashes,numCellsNeeded, counter)
    for i in range(20):
        Bloom.insert("Hadas")
        Bloom.insert("Mom")
    for i in range(20):
        Bloom.remove("Mom")
    #make sure Mom was removed and not in the CBM anymore
    assert Bloom.find("Mom",20 )  == False 

    
#make sure the size is 1 less after a key is removed  
def test_sizeAfterRemove():
    numHashes = 1
    #max inserts per cell
    counter=1
    numCellsNeeded=100
    
    Bloom=CountingBloomFilter(numHashes,numCellsNeeded, counter)
    
    Bloom.insert("Hadas")
    size1=Bloom.numSet()
    Bloom.remove("Hadas")
    size2=Bloom.numSet()
    
    assert (size1-size2)==1
def test_removeFromEmpty():
    numHashes = 4
    #max inserts per cell
    counter=35
    numCellsNeeded=100
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded, counter)
    
    #assert the key  Hadas cannot be removed because it is not in the CBM
    assert Bloom.remove("Hadas")==False    
#_____________________________________test empty_______________________________    
#test to make sure an empty one is empty
def test_empty():
    numHashes = 4
    #max inserts per cell
    counter=35
    numCellsNeeded=1
    
    Bloom=CountingBloomFilter( numHashes,numCellsNeeded, counter)
    
    #assert the key  Hadas is found zero times 
    assert Bloom.find("Hadas",1)==False

    
    
pytest.main(["-v","-s","CountingBloomFilter.py"])