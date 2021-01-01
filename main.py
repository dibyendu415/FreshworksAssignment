import functions as f
import threading

while(True):
    print("Press 1 to create new key-value pair.")
    print("Press 2 to read a value.")
    print("Press 3 to Delete a key-value.")
    print("Enter any number(other than 1,2,3) to exit.")

    val = int(input())
    
    if(val==1):
        print("Enter key:")
        key = input()
        print("Enter value:")
        value = int(input())
        print("Enter Time-to-Live:")
        ttl = int(input())
        t1=threading.Thread(target=(f.create),args=(key,value,ttl))
        t1.start()
        t1.join()
    elif(val==2):
        print("Enter Key:")
        key = input()
        t2=threading.Thread(target=(f.read),args=(key,))
        t2.start()
        t2.join()
    elif(val==3):
        print("Enter Key:")
        key = input()
        t3=threading.Thread(target=(f.delete),args=(key,))
        t3.start()
        t3.join()
    else:
        print("Exit.")
        break
