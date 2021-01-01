import json
import os
import portalocker
import time

def create(key, value, ttl=0):

    #creating new file if the file is not present in specified location
    if not os.path.exists('D:/Freshworks/generatedFile.txt'):

        #lock to prevent more than one client process from using same file as a data store at any given time 
        try:
            with open("generatedFile.txt", "w") as write_file:
                portalocker.lock(write_file, portalocker.LOCK_EX)
                if(ttl==0):
                    li = [value,ttl]
                    json.dump({key:li}, write_file)
                else:
                    li = [value, time.time()+ttl]
                    json.dump({key:li}, write_file)

                portalocker.unlock(write_file)
        except IOError:
            time.sleep(0.05)

        print("Success: Key-value pair added successfully.")

    #if the specified path exists, add in that location
    else:
        with open('D:/Freshworks/generatedFile.txt') as f:
            data = json.load(f)
    
        if key in data:
            print("\nKey Exist Error: could not add, data already present.")
        elif(len(data)>(1024*1024*1024)):
            print("\nFile-Bound exhausted Error: Could not add any more data.")
        elif(value>(16*1024)):
            print("\nValue-out-of-bounds Error: Preferred Size of value exceeded.")
        elif(len(key)>32):
            print("Key-length exceeded Error: Must be capped at 32chars.")
        elif(key.isalpha()==False):
            print("Key-type error: Must contain only Alphabets.")
        else:
            if(ttl==0):
                ListValue = [value,ttl]
            else:
                ListValue = [value, time.time()+ttl]

                data[key] = ListValue
                print("\nSuccess: Key-value pair added successfully.")

            try:
                with open('D:/Freshworks/generatedFile.txt', 'w') as fi:
                    portalocker.lock(fi, portalocker.LOCK_EX)
                    json.dump(data, fi)
                    portalocker.unlock(fi)
            except IOError:
                time.sleep(0.05)


def read(key):
    try:
        with open('D:/Freshworks/generatedFile.txt') as file:
            data = json.load(file)
        if key not in data:
            print("\nCease-to-exist error: The specified key is absent.")
        else:
            ttlV = data[key]
            if(ttlV[1]==0):
                print(str(key)+":"+str(ttlV[0]))
            else:
                if(time.time() < ttlV[1]):
                    print(str(key)+":"+str(ttlV[0]))
                else:
                    print("\nKey-expire condition: Time-to-live of ",key,"has expired.")
    except:
        print("No-data-Error: Data store might not consist/ might not be initialised with any data.")

def delete(key):
    try:
        with open('D:/Freshworks/generatedFile.txt') as file:
            data = json.load(file)
        if key not in data:
            print("\nCease-to-exist error: The specified key does not exist.")
        else:
            ttlV=data[key]
            if ttlV[1]==0:
                del data[key]
                print("\nSuccess: Key-value pair deleted successfully.")
            else:
                if time.time()<ttlV[1]:
                    del data[key]
                    print("\nSuccess: Key-value pair deleted successfully.")
                else:
                    print("\nKey-expire condition: Time-to-live of",key,"has expired.")
            try:
                with open('D:/Freshworks/generatedFile.txt', 'w') as fi:
                    portalocker.lock(fi, portalocker.LOCK_EX)
                    json.dump(data, fi)
                    portalocker.unlock(fi)
            except IOError:
                time.sleep(0.05)

    except:
        print("No-data-Error: Data store might not consist/ might not be initialised with any data.")
