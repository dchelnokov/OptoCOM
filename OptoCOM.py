import os
import sys
import time

try:
    os.chdir(r'C:\Users\DXC\AppData\Roaming\Python\Python39\Scripts')
except:
    pass
import serial

def tx_cmd(handler, cmd):
    feedback = ''
    try:
        msg_to_send = cmd + '\r'
        print(f'>sending {msg_to_send}')
        handler.write(msg_to_send.encode())
        b = handler.read()
        while b:
            feedback += b.decode()
            b = handler.read()
    except:
        print(f"Couldn't send the command {cmd}.")
    return feedback

arg_len = len(sys.argv)
delay = 3
port=''
commands = []

if arg_len > 2:
    port = sys.argv[1]
    commands = sys.argv[2:]
else:
    print(f' Not enough arguments: expected 2 or more, received {arg_len}',
          '\n\n Tip: The first argument is the port name (e.g. "COM5"), than one or more commands that must be sent\n',
          r' Example: C:\OptoCOM.exe "COM5" "~0000 1" "~00150 1"',
          "\n - each command will automatically receive the trailing *new line* character.\n",
          f"\n  Each next command in the line will be sent with {delay} second{'s' if delay > 1 else ''} delay.",
          "\n  After sending each command the response from host will be shown.",
          "\n *Please send bug reports to 2chelnokov@gmail.com with the keyword 'bug_report' in subject",
          "\n (c) Dmitry Chelnokov 2022")
    sys.exit()


try:
    print(f'>Opening connection to {port}...')
    ser = serial.Serial(port=port,
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        bytesize=8,
                        timeout=3,
                        xonxoff=False,
                        stopbits=serial.STOPBITS_ONE
                        )
except:
    print(f"Error: can't open the serial port '{port}':", )
    sys.exit()

for cmd in commands:
    r = tx_cmd(ser, cmd)
    print(f"> Response for {cmd} was:\n{r if len(r) else 'No response'}")
    
    if arg_len > 3:
        print(f"> wait {delay} second{'s' if delay > 1 else ''}")
        time.sleep(delay)

ser.close()
print('<< END.')



