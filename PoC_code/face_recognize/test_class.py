import time, threading
from collections import deque 

class test:
    def __init__(self):
        self.count = 0
        self.q = deque()
        t =  threading.Thread(target=self.increment)
        t.daemon = True
        t.start()


    def increment(self):
        time.sleep(4)
        while True:
            self.count += 6
            # print("class itself ",self.getCount())
            
            if len(self.q) < 5:
                self.q.append(self.count)
            else:
                # self.q.clear()
                self.q.popleft()
                self.q.append(self.count)
            # print(len(self.q))
        
            # time.sleep(0.3)
            
            # self.q.popleft()
            # print("sdfasd")
        # print(self.q.get())
    
    def getCount(self):
        print("leng:", len(self.q))
        if len(self.q) > 0:
            return self.q.pop()
        else:
            return -1
        