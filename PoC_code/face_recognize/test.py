from test_class import test
import time

t1 = test()
while True:
    time.sleep(0.5)
    print("caller ",t1.getCount())
