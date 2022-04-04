#!/usr/bin/env python3

import threading
import time
from printer import Printer

from cmd import Cmd
 
class MyPrompt(Cmd):
    def precmd(self, line):
        print(line)
        return line

    def do_exit(self, inp):
        print("Bye")
        return True

    def do_add(self, inp):
        print("Adding '{}'".format(inp))

    def do_G0(self, inp):
        print(inp)
        time.sleep(5)

    # absolute mode
    def do_go(self, inp):
        print(inp)
        #printer.send("G0")

    def do_move(self, inp):
        pass

def read_from_port(ser):
    while True:
        reading = ser.readline().decode()
        print(reading)
        #handle_data(reading)

printer = Printer()
printer.open('/dev/ttyUSB0')

MyPrompt().cmdloop()

printer.close()


#thread = threading.Thread(target=read_from_port, args=(ser,))
#thread.start()
