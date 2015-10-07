import string
import threading
import time

def print_test(msg,time_):
    time.sleep(time_)
    print(msg)
    

def main():

    a= threading.Thread(target=print_test,args=("THREAD 1",10,))
    a.start()
    
    b = threading.Thread(target=print_test,args=("THREAD 2",2,))
    b.start()
    
    print("THSRTNRNTRNN")
main()
