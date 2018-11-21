import socket

# Echo server program
import socket
import re
import threading
from Queue import Queue
#C:\Python27\python.exe -u C:\Users\chris\Documents\GitHub\Pydev\plugins\org.python.pydev.core\pysrc\pydevd.py --multiprocess --print-in-debugger-startup --vm_type python --client 127.0.0.1 --port 64974 --file C:\Users\chris\runtime-EclipseApplication\test\src\cats.py
class SocketReader(threading.Thread):

    def __init__(self, s, q):
        threading.Thread.__init__(self)
        self.buf = ""
        self.message_queue = list()
        self.sock = s

        self.setDaemon(True)
        self.q = q
        self._kill = False

    def get_message(self):
        return self.q.get(block=True)

    def run(self):
        while not self._kill:
            # Grab 1024 bytes
            # Append to any buffered data from prev calls.
            self.buf += self.sock.recv(1024)
            self.buf = self.buf.replace('\r', '')
            # Now, we might have a string that contains multiple lines.
            # Split whatever we get on \n.
            data_split = self.buf.split("\n")

            # If any items are actually split, then we have some complete
            # line commands we can use. If not, then we loop and get another
            # 1024 bytes until we have a newline.
            if len(data_split) > 1:

                # Queue everything but the last element. They will all be
                # complete commands.
                message_queue = data_split[:-1]
                for message in message_queue:
                    if message != "":
                        self.q.put(message)

                # The last element is going to be a partial (or empty) line, so
                # buffer it. Note that we *replace* the buffer here rather
                # than append to it.
                self.buf = data_split[-1]


    def do_kill(self):
        self._kill = True


def input_handler(s):
    print "INPUT_RECIEVED(%s)" % (re.escape(s))



import sys



HOST = ''                 # Symbolic name meaning the local host
PORT = 64974              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

q = Queue()
sr = SocketReader(conn,q)
sr.start()

conn.send(u"503\t1\thttp\n")
conn.send(u"501\t3\t1.1\tWINDOWS\tID\n")
#Set a breakpoint on cats.py
conn.send(u"111\t5\t0\tpython-line\tC:\\Users\\chris\\runtime-EclipseApplication\\test\\src\\cats.py\t11\t\tNone\tNone\n")
conn.send(u"131\t9\tfalse;false;false;true;true;\n")
conn.send(u"133\t11\t\n")
conn.send(u"140\t13\tREPLACE:\n")
conn.send(u"126\t15\tDjangoExceptionBreak\n")
conn.send(u"141\t17\ttrue\n")
conn.send(u"146\t19\tCMD_SHOW_RETURN_VALUES\t1\n")
conn.send(u"101\t21\t\n")
while 1:
    if not q.empty():
        print "RECIEVED: [%s]" % (q.get(False))

conn.close()
