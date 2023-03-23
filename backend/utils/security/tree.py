from Node import Node
import time
from collections import deque
import matplotlib.pyplot as plt

class Tree(object):
    def __init__(self,maxSize = 30000):
        
        self.root = Node(0,self)
        
        self.array = [self.root] + list([None]*(2*maxSize+10))
        
        self.nodeCount = 1
        self.queue = deque()
        self.queue.append(self.root)

    def left(self,node):
        x =  self.array[2*node.id + 1]
        return x
    def right(self,node):
        x =  self.array[2*node.id + 2]
        return x
    def parent(self,node):
        if(node.id==0):
            x =  node
        else:
            x =  self.array[((node.id)-1)//2]
        return x 
    def setLeft(self,x,target):
        self.array[2*x.id + 1] = target
    def setRight(self,x,target):
        self.array[2*x.id + 2] = target
    def setParent(self,x,target):
        if(x.id==0):
            return 
        self.array[(x.id-1)//2] = target
    def setLeaf(self,x):
        
        self.setLeft(x,None)
        self.setRight(x,None)

        x.isLeaf=True
    def findSponsor(self):
        front = self.queue[0]
        # if(front.left() is None and front.right() is None):
        self.queue.popleft()
        return front
        # else:
        #     print("Node deformed")
        #     return None
    def createNode(self):
        newNode = Node(self.nodeCount,self)
        self.nodeCount+=1
        return newNode
    def insertNewUser(self):
        sponsor = self.findSponsor()
        leftNewNode = self.createNode()
        self.queue.append(leftNewNode)
        rightNewNode = self.createNode()
        self.queue.append(rightNewNode)
        self.setParent(leftNewNode,sponsor)
        self.setParent(rightNewNode,sponsor)
        
        leftNewNode.copyDataFrom(sponsor)
        sponsor.isLeaf = False
        self.setLeft(sponsor,leftNewNode)
        self.setRight(sponsor,rightNewNode)
        
        sponsor.recalculateKeyPath()
    def deleteUser(self,deleteId=-1):
        toDelete = self.queue[-1]
    
        if(deleteId != -1):
            for i in self.queue:
                if i.id == deleteId:
                    toDelete = i

        
        if(toDelete.parent().left().id==toDelete.id):
            toDelete.parent().copyDataFrom(toDelete.parent().right())
        
        else:
            toDelete.parent().copyDataFrom(toDelete.parent().left())
        self.setLeaf(toDelete.parent())
        toDelete.parent().recalculateKeyPath()
        
        self.queue.pop()
        self.queue.pop()
        self.queue.appendleft(toDelete.parent())
    def swapNodes(self,node1,node2):
        node1.id,node2.id = node2.id,node1.id
        node1.key,node2.key = node2.key,node1.key
        node1.bKey,node2.bKey = node2.bKey,node1.bKey
        node1.isLeaf,node2.isLeaf = node2.isLeaf,node1.isLeaf
        node1.recalculateKeyPath()
        node2.recalculateKeyPath()
    def swapUsers(self,id1=-1,id2=-1):
        if(id1==-1 and id2==-1):
            node1 = len(self.queue) -2
            node2 = len(self.queue) -1
        else : 
            node1=node2=0
            for i in range(len(self.queue)):
                if(self.queue[i].id==id1):
                    node1 = i
                if(self.queue[i].id==id2):
                    node2 = i
        self.swapNodes(self.queue[node1],self.queue[node2])
        if(id1 == -1 and id2 == -1):
            x = self.queue.pop()
            y = self.queue.pop()
            self.queue.append(y)
            self.queue.append(x)
        else:
            self.queue[node1],self.queue[node2] = self.queue[node2],self.queue[node1]

    def removeUser(self,id):
        pass

    def verifyTreeIntegrity(self):
        return self.root.verifyIntegrity()
    def __str__(self):
        output =""
        lines, *_ = self.root.recursivePrint()
        for line in lines:
            output+=line
            output+='\n'
        return output

def insert_delete():
    NUM_NODES=100
    tree = Tree()
    y = []
    x = []
    for i in range(NUM_NODES):
        start = time.time()
        tree.insertNewUser()
        end = time.time()
        if(i%5==0):
            print(i)
            y.append(end - start)
            x.append(i)
    print(tree.verifyTreeIntegrity())
    # data=[x,y]
    #
    # plt.plot(x,y,"o-")
    # plt.xlabel("Number of users")
    # plt.ylabel("Time for insertion(sec)")
    # plt.savefig("./insertion_time_plot.png")
    # plt.clf()
    # x=[]
    # y=[]
    for i in range(NUM_NODES):
        start = time.time()
        tree.deleteUser()
        end = time.time()
        if(i%5==0):
            print(i)
            y.append(end - start)
            x.append(NUM_NODES-(i+1))
        
    print("After Delete",tree.verifyTreeIntegrity())
    # data=[x,y]
    # plt.plot(x,y,"o-")
    # plt.xlabel("Number of users")
    # plt.ylabel("Time for deletion(sec)")
    # plt.savefig("./deletion_time_plot.png")
    # plt.show()


# NUM_NODES=10
# tree = Tree()
# for i in range(NUM_NODES):
#     tree.insertNewUser()
# print(tree.verifyTreeIntegrity())
# print(tree)
# tree.swapUsers()
# print(tree.verifyTreeIntegrity())
# print(tree)

insert_delete()