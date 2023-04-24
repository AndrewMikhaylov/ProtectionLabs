import shelve
import os
fs = shelve.open('filesystem', writeback=True)
current_dir = []
username = ""
isAdmin = False

def install(fs):
    global username
    global isAdmin
    print(list(fs.keys()))

    username = input('What is your username? ')
    if str(username) == "Admin":
        isAdmin = True
        return
    if username in list(fs.keys()):
        fs[username] = fs.get(username)
    else:
        password = input('Enter new password: ')
        fs[username] = {"System": {}, "Users": list(fs.keys())}


def current_dictionary():
    global username
    if username == "Admin":
        if len(current_dir) == 0:
            return dict(fs.items())
        else:
            username = current_dir[0]
    d = fs.get(username)
    for key in current_dir:
        d = d[key]
    return d


def ls(args):
    if username =="Admin" and len(current_dir) == 0:
        print('Available users systems: ')
    else:
        print('Contents of directory', "/" + "/".join(current_dir) + ':')
    for i in current_dictionary():
        print(i)

def cat(args):
    if len(args) != 1:
        print("Usage: cd <directory>")
        return

    if args[0] in current_dictionary() and type(current_dictionary()[args[0]]) == str:
        print(current_dictionary()[args[0]])
    else:
        print("Can't read given file")

def vi(args):
    if username == "Admin":
        print("Can't create text file in user spaces")
        return
    text_input=input("Print your text here: ")

    current_dictionary()[args[0]] = text_input
    fs.sync()


def cd(args):
    if len(args) != 1:
        print("Usage: cd <directory>")
        return

    elif args[0] == "..":
        if len(current_dir) == 0:
            print("Cannot go above root")
        elif isAdmin is True:
            current_dir.pop()
        else:
            current_dir.pop()
    elif type(current_dictionary()[args[0]]) == str:
        print("Can't enter text file")
        return
    elif args[0] not in current_dictionary():
        print("Directory" + args[0] + "not found")
    else:
        current_dir.append(args[0])


def mkdir(args):
    if len(args) != 1:
        print ("Usage: mkdir <directory>")
        return
    elif username =="Admin":
        print("Can't create directory in user spaces")
        return
    # create an empty directory there and sync back to shelve dictionary!
    current_dictionary()[args[0]] = {}
    fs.sync()

def clear(args):
    os.system('clear')
def ls_l(args):
    os.system('ls -l')

COMMANDS = {'ls' : ls, 'cd': cd, 'mkdir': mkdir, 'clear' : clear, 'ls -l' : ls_l, 'cat' : cat, 'vi' : vi}

install(fs)

while True:
    raw = input('> ')
    cmd = raw.split()[0]
    if cmd in COMMANDS:
        COMMANDS[cmd](raw.split()[1:])

    if cmd=='end':
        fs.close()
        break

    if cmd == 'exit':
        install(fs)


