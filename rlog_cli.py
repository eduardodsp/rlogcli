import sys
import argparse
import socket
import select
from pythonping import ping
from colorama import init, Fore, Back, Style

def main(argv):
   
    RLOG_BANNER = """ ______     __         ______     ______    
/\  == \   /\ \       /\  __ \   /\  ___\   
\ \  __<   \ \ \____  \ \ \/\ \  \ \ \__ \  
 \ \_\ \_\  \ \_____\  \ \_____\  \ \_____\ 
  \/_/ /_/   \/_____/   \/_____/   \/_____/ """

    # Initializes Colorama
    init(autoreset=True)

    parser = argparse.ArgumentParser(description='[RLOG] Remote Logger client. Receive, filter and save log messages from remote devices')

    parser.add_argument('-ip', type=str, default = "192.168.178.210", help='Server IP address')
    parser.add_argument('-p', dest = 'port', type=int, default = 8888, help='TCP PORT used by target server')
    parser.add_argument('-tag', type=str, help='Tag filter. User defined message tag')
    parser.add_argument('-type', type=int, help='Type filter. Available options: 1 = Info, 2 = Warnings, 3 = Errors')
    parser.add_argument('-o', dest = 'output', type=str, help='Output filename')

    args = parser.parse_args()
    
    HOST = args.ip
    PORT = args.port
    FILTER_TAG = args.tag
    FILTER_TYPE = args.type
    OUTPUT_FILE = args.output

    print(RLOG_BANNER)
    print("\n")
    
    MSG_HOST_PORT = HOST + ":" + str(PORT)
    MSG_WAITING_ON_SERVER = "Waiting for RLOG server on " + MSG_HOST_PORT
    MSG_CONNECTED_TO_SERVER = Fore.GREEN + "Connected to server on " + MSG_HOST_PORT + "!"
    MSG_DISCONNECTED_FROM_SERVER = Fore.RED + "Lost connection from server on " + MSG_HOST_PORT + "!"
    MSG_SERVER_UNREACHABLE = Fore.RED + "Server address is unreachable"
    MSG_FATAL_ERROR = Fore.RED + "Unexpected error!"

    exit = False
    attempts = 0

    print (MSG_WAITING_ON_SERVER)
    while (exit == False):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:        
                try:
                    s.settimeout(10)
                    s.connect((HOST, PORT))
                    print (MSG_CONNECTED_TO_SERVER)
                    s.setblocking(0)
                    socket_list = [s]
                    connected = True
                    attempts = 0
                    while(connected) : 

                        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [], 5)

                        if len(read_sockets) != 0:
                            raw = s.recv(1024)
                            lmsg = str(raw.decode('ascii'))
                            if (len(lmsg) > 0):
                                process_msg(lmsg, FILTER_TAG, FILTER_TYPE)      
                                save_to_file(lmsg, OUTPUT_FILE)                      
                        else:
                            rsp = ping(HOST, verbose=False)
                            if (rsp.success() == False):
                                print (MSG_DISCONNECTED_FROM_SERVER)
                                connected = False

                except socket.timeout:
                    # timeout trying to connect, lets try some more times            
                    print (MSG_WAITING_ON_SERVER)    

                    if (attempts >= 2):
                        print (MSG_SERVER_UNREACHABLE)
                        exit = True

                    attempts = attempts + 1        

                except KeyboardInterrupt:
                    exit = True

        except:
            print (MSG_FATAL_ERROR)
            exit = True

    print ("Terminating RLOG client!")


def process_msg(msg, ftag, ftype):

    # apply tag filter
    if (ftag is not None):
        if (msg.find(str("["+ ftag + "]")) == -1):
            return None

    # get message type
    msg_type = get_msg_type(msg)

    # apply type filter
    if (ftype is not None):
        if (msg_type != ftype):
            return None

    # print filtered message
    print_colored(msg, msg_type)


def get_msg_type(msg):
    
    if (msg.find("[i]") > 0):
        return 1
    
    if (msg.find("[!]") > 0):
        return 2

    if (msg.find("[#]") > 0):
        return 3

    else:
        return None


def print_colored(msg, itype):

    if (itype == 1):
        print (msg, end="")
    
    elif (itype == 2):
        print (Fore.YELLOW + msg, end="")

    elif (itype == 3):
        print (Fore.RED + msg, end="")


    
def save_to_file(msg, outputfile):

    if(outputfile is not None):
        with open(outputfile, 'a') as f:
            f.write(msg)

if __name__ == '__main__':
    try:
        main(sys.argv[1::])
    except KeyboardInterrupt as ex:
        exit(1)

