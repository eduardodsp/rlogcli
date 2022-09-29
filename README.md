# RLOG Client

Small client to receive, print and filter messages from remote devices running an [RLOG Server](https://github.com/eduardodsp/rlog)

## Requirements

- python (3.x.y)
- pip

## Installation
```bash
pip install -r requirements.txt
```

## How To Use
To use this client all you have to do is run the following command
```
python rlogcli.py -ip <rlog server ip address> -p <user defined tcp port>
```
The client will immediately start running and will try to connect to the server at the defined
ip address + port. If successful the client will begin to print all received messages in order.

### Example:
```
python rlogcli.py -ip 192.168.178.210 -p 8888
```
[![gif with examples][example-link]][example-link]

### Command Options
```
usage: rlogcli.py [-h] [-ip IP] [-p PORT] [-tag TAG] [-type TYPE] [-o OUTPUT]        

[RLOG] Remote Logger client. Receive, filter and save log messages from remote devices

options:
  -h, --help  show this help message and exit
  -ip IP      Server IP address
  -p PORT     TCP PORT used by target server
  -tag TAG    Tag filter. User defined message tag
  -type TYPE  Type filter. Available options: 1 = Info, 2 = Warnings, 3 = Errors      
  -o OUTPUT   Output filename
```
Arguments -tag and -type are display filters that allows the user to select which messages are to be printed on the terminal: 
- Tag: This is a user defined string that typically indicates the context of the message.
- Type: Indicates whether this is an Informational, Warning or Error message.

Argument -o allows the user to write all messages to a plain text file. By desgin all messages are saved to the file, even if display filters are being used. 

[example-link]:   https://github.com/eduardodsp/rlogcli/blob/main/example.gif