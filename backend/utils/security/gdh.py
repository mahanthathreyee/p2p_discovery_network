from Crypto.Random.random import randint
from Crypto.Util import number
import time
import matplotlib.pyplot as plt
from collections import deque

class gdh : 
    g = 2
    p = number.getPrime(2048)
    privateKeys = []
    publicKeys = []
    complementKeys = []
    ids = []
    secretKey = 0
    central_node = 0
    def insertNewUser(self):
        n_users = len(gdh.privateKeys)
        if(n_users>=1):
            exp_new = randint(1,int(gdh.p-1))
            gdh.privateKeys[0] = (gdh.privateKeys[0] * exp_new) % gdh.p
            gdh.publicKeys[0] = pow(gdh.publicKeys[0],exp_new,gdh.p)
            for i in range(0,n_users):
                if(i!=gdh.central_node):
                    gdh.complementKeys[i] = pow(gdh.complementKeys[i],exp_new,gdh.p)
            secretKey = pow(gdh.complementKeys[0],gdh.privateKeys[0],gdh.p)
            gdh.privateKeys.append(randint(1,int(gdh.p-1)))
            gdh.publicKeys.append(pow(gdh.g,gdh.privateKeys[n_users],gdh.p))
            gdh.complementKeys.append(secretKey)
            gdh.ids.append(id_queue[0])
            id_queue.append(id_queue[0]+1)
            id_queue.popleft()
            for i in range(0,n_users+1):
                if(i!=n_users):
                    gdh.complementKeys[i] = pow(gdh.complementKeys[i],gdh.privateKeys[n_users],gdh.p)
        else:
            gdh.privateKeys.append(randint(1,int(gdh.p-1)))
            gdh.publicKeys.append(pow(gdh.g,gdh.privateKeys[n_users],gdh.p))
            gdh.complementKeys.append(1)
            gdh.ids.append(id_queue[0])
            id_queue.append(id_queue[0]+1)
            id_queue.popleft()
            


NUM_NODES=1000
y = []
x = []
id_queue = deque()

id_queue.append(0)
group = gdh()
group.insertNewUser()
for i in range(NUM_NODES):
    start = time.time()
    group.insertNewUser()
    print("public keys: ", len(group.publicKeys), ", ", group.publicKeys)
    print("private keys: ", len(group.privateKeys), ", ", group.privateKeys)
    print("secret key: :", group.secretKey)
    end = time.time()
    if(i%5==0):
        print(i)
        y.append(end - start)
        x.append(i)
data = [x,y]

plt.plot(x,y)
plt.show()