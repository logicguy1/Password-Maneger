from time import sleep
import random

import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def getPass(password_provided):
    password = password_provided.encode()
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def getData():
    file = open("storage.txt", "r")
    read = file.read()
    file.close()
    if read == "":
        return False
    else:
        return read

if getData() != False:
    trys = 0

    while True:
        key = input("KEY: ")
        try:
            file = open("storage.txt", "r").readlines()
            dict = {}
            key = getPass(key)
            f = Fernet(key)
            for i in file:
                split1, split2 = i.split("^^^^")
                split1 = split1.strip()
                split2 = split2.strip()
                split1 = split1.encode()
                split2 = split2.encode()
                split1 = f.decrypt(split1)
                dict[split1.decode()] = split2
                decode = f.decrypt(split2)
        except:
            trys += 1
            if trys >= 3 and trys != 10:
                print(f"You failed {trys} times the system will lock for 5 minutes")
                sleep(300)
            elif trys == 10:
                file = open("storage.txt", "w")
                file.close()
                print("You faied 10 times and all the files has been eraced!")
                break
            pass
        else:
            trys = 0
            print("key is valid")
            inp = input("\nWelcome to the password Manager this is the place to store your passwords nice and safe\nType a number to get started\n1: Add a new password\n2: Sertch a site in the database\n3: Create a new password\nEnter here: ")

            if inp == "1":
                web = input("Type a website: ")
                passwd = input("Type the password: ")

                webe = f.encrypt(web.encode())
                passwde = f.encrypt(passwd.encode())

                file = open("storage.txt", "a")
                file.write(f"\n{webe.decode()}^^^^{passwde.decode()}")
                file.close()
            elif inp == "2":
                inp = input("Type a webside to seartch: ")
                try:
                    get = dict.get(inp)
                except:
                    print("Not Found")
                else:
                    if get is not None:
                        decode = f.decrypt(get)
                        print(decode.decode())
                    else:
                        print("Not Found")
            elif inp == "3":
                char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                while True:
                    inp = input("How long: ")
                    try:
                        inp = int(inp)
                    except:
                        print("NaN")
                    else:
                        break
                str = ""
                for i in range(inp):
                    temp = random.choice(char)
                    str += temp
                print(str)
                inp = input("Do you want to save this new password? (y/n)")
                if inp.lower() == "y":
                    web = input("Type a website: ")

                    webe = f.encrypt(web.encode())
                    passwde = f.encrypt(str.encode())

                    file = open("storage.txt", "a")
                    file.write(f"\n{webe.decode()}^^^^{passwde.decode()}")
                    file.close()
            else:
                print("Not a option")

else:
    print("Make a new key")
    key = input("KEY: ")
    key = getPass(key)
    inp = input("Do you want to save a new password? (y/n)")
    if inp.lower() == "y":
        web = input("Type a website: ")
        passwd = input("Type the password: ")

        f = Fernet(key)
        webe = f.encrypt(web.encode())
        passwde = f.encrypt(passwd.encode())

        file = open("storage.txt", "a")
        file.write(f"{webe.decode()}^^^^{passwde.decode()}")
        file.close()
