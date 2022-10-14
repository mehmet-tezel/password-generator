#python 3.10.7
#https://github.com/mehmet-tezel

import getopt, sys, os
import string, secrets
import json
import pyperclip
from os.path import exists as file_exists

temp = string.ascii_letters + string.digits + string.punctuation
filename = "passlist.json"

def usage():
    print("\nUSAGE: python passgen.py\n\t-h, --help:\t prints usage menu.")
    print("\t-v, --version:\t prints script version.")
    print("\t-f, --find:\t gets password from id.")
    print("\t-i, --id:\t set id.")
    print("\t-l, --length:\t set password length.")
    print("\t-g, --generate:\t generates password with given arguments.")
    print("\t-d, --delete:\t deletes passlist.json")
    print("\texample usage:\t python passgen.py -i info@passwordgen.com -l 16 -g")
    print("\t- creates new data into passlist.json.")

def password_manager():
    print("***** PASSWORD GENERATOR *****")
    print("[1] List Passwords")
    print("[2] Generate Password")
    print("[3] Generate Password With Key")
    print("[4] Get Password From Key")

    userdata = {}

    if file_exists(filename):
        with open(filename) as f:
            userdata = json.load(f)

    choice = int(input(">> "))
    if choice == 1:
        print(userdata)
    elif choice == 2:
        length = int(input("Enter password length: "))
        password = "".join(secrets.choice(temp) for i in range(length))
    elif choice == 3:
        id = input("Enter id: ")
        length = int(input("Enter password length: "))
        password = "".join(secrets.choice(temp) for i in range(length))   
        userdata[id] = [{"Password": password, "Length": length}]
        with open(filename, "w") as f:
            json.dump(userdata, f, indent=4, separators=(",",": "))
    elif choice == 4:
        if file_exists(filename):
            with open(filename) as f:
                userdata = json.load(f)
                id = input("Enter id: ")
                print(eval("Password", userdata[id][0]))
        else:
            print("Please generate password first!")
    else:
        print("Wrong usage!")

    if choice == 2 or choice == 3:
        print("Generated password: " + password)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvi:f:l:gd", ["help", "version", "id=", "find=", "length=", "generate", "delete"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    userdata = {}
    password = None
    id = None
    length = None
   
    if file_exists(filename):
        with open(filename) as f:
            userdata = json.load(f)
            
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-v", "--version"):
            print("Password Generator Version 1.0.0")
        elif o in ("-f", "--find"):
            try:
                password = eval("Password", userdata[a][0])
                pyperclip.copy(password)
                print("Password: " + password + " copied to clipboard.")
            except:
                print("ID Not Found. Please check your id or username and run script again.")
        elif o in ("-i", "--id"):
            id = a
        elif o in ("-l", "--length"):
            length = int(a)
        elif o in ("-g", "--generate"):
            try:
                password = "".join(secrets.choice(temp) for i in range(length))   
                userdata[id] = [{"Password": password, "Length": length}]
                with open(filename, "w") as f:
                    json.dump(userdata, f, indent=4, separators=(",",": "))
                    print("Password: " + password + " generated and written to file.")
            except:
                print("Please use -h or --help for more information. Set all arguments and then generate password.")
        elif o in ("-d", "--delete"):
            if file_exists(filename):
                os.remove(filename)
                print("File succesfully removed.")
        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        password_manager()
