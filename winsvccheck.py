import subprocess
import os

os.system("") #run this to initialize the use of ansi in windows
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

#---------------------------------------------------------------------
# print in color.  color is a value from the sytle clase. reset to 
# if reset is true.
def printc(color, text, reset):
    t = color + text
    if (reset):
        t += style.RESET
    print(t)

#---------------------------------------------------------------------
# determine if the path is writable by the current user
def dir_writable(path):
    try:
        p = path.rsplit('\\', 1)
        temp = p[0] + '\\foo.txt'
        temp = temp.replace("\\\\", "\\")
        if (temp.startswith('"')):
            temp += '"'
        open(temp, "x")
        os.remove(temp)
        return True
    except Exception as e:
        print(e)
        return False

#---------------------------------------------------------------------
# run "sc query" and extract the names of the services on the machine.
# tested with Windows 10 Pro
def serviceNames(show):
    names = []
    s = subprocess.Popen(['sc','query'], stdout=subprocess.PIPE)
    output = s.stdout.read()
    ar = str(output).split('SERVICE_NAME: ')
    for i in range(1, len(ar)):
        ar2 = ar[i].split('\\r\\n')
        names.append(ar2[0])
    print(str(len(names)) + " service names detected\r\n")
    if (show):
        temp = '\r\n'.join(names)
        print(temp)
    return names

#---------------------------------------------------------------------
# run "sc qq [name]" and extract the path to the service by service name.
# tested with Windows 10 Pro
def servicePaths(names, show):
    paths = []
    for name in names:
        s = subprocess.Popen(['sc', 'qc', name], stdout=subprocess.PIPE)
        output = s.stdout.read()
        ar = str(output).split('BINARY_PATH_NAME   : ')
        ar2 = ar[1].split('\\r\\n')
        ar3 = ar2[0].split('.exe')
        path = ar3[0] + '.exe'
        if (ar3[0].startswith('"')):
            path += '"'
        paths.append(path)
        if (show):
            print(name + " : " + path)            
    return paths

#-----------------------------------------------------------------------
# look for vulnerabilities in the service name/path
# currently implments: unquoted service path with a space
#                      writable service path by current user
def lookForVulns(names, paths):
    for i in range(0, len(paths)):
        name = names[i]
        path = paths[i]
        if (" " in path and "\"" not in path):
            printc(style.RED, f'Service {name} has a space with an unquoted path: {path}', True)
        if (dir_writable(path)):
            printc(style.GREEN, f'Service {name} path is writable by current user: {path}', True)

names = serviceNames(False)
paths = servicePaths(names, False)
lookForVulns(names, paths)

# loop service_names and call "sc qc [name]" and parse out the file path
# look for unquoted paths
# look for paths the current user has rights to

#print(output)