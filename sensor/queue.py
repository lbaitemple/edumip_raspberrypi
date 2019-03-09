class Queue:
    def __init__(self,  maxsize=0):
        self.maxsize = maxsize
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        if (self.size()>=self.maxsize):
            self.items.pop()
            self.enqueue(item)
        else:
            self.items.insert(0,item)

    def getValueAt(self, indx):
        if (indx<=self.size() and indx >=0):
            return(self.items[indx])
        else:
            return 0

    def dequeue(self):
        return self.items.pop()

    def printqueue(self):
        for a in range(0, self.size()):
            print self.items[a],
            print " ",

        print("\n")

    def size(self):
        return len(self.items)
 
