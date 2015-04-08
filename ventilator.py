import os #operating system
from PIL import Image
import StringIO
import time
import zmq

try:
    raw_input
except NameError:
    # Python 3
    raw_input = input

print("Start ventilator")

# Set active directory containing images
os.chdir('D:\Pictures\src')

context = zmq.Context()

# Socket to send messages on
worker_socket = context.socket(zmq.PUSH)
worker_socket.bind("tcp://*:5557")

# Socket to receive successful messages 
sink_socket = context.socket(zmq.PULL)
sink_socket.connect("tcp://localhost:5559")

# Get file listing
files = os.listdir('.')

print("Press Enter when the workers are ready: ")
raw_input()
print("Sending tasks to workers")
tstart = time.time()

# Send files to workers
counter = 0
for file in files:
    print("Send %s to worker." % file)
    data = StringIO.StringIO(open(file, 'rb').read())
    img_dict = {'name': file, 'data': data}
    worker_socket.send_pyobj(img_dict)
    counter += 1

# Waiting all files to be processed
for _ in range(counter):
    print(sink_socket.recv_string())

# Count the elapsed time
tend = time.time()
print("Total elapsed time: %d sec" % (tend-tstart))
