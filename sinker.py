import StringIO
import os
import zmq

print("Start sinker")

# Set active directory containing images
os.chdir('D:\Pictures\dst')

context = zmq.Context()

# Socket to receive messages on
worker_socket = context.socket(zmq.PULL)
worker_socket.bind("tcp://*:5558")

# Socket to send successful messages
vent_socket = context.socket(zmq.PUSH)
vent_socket.bind("tcp://*:5559")

# Forever loop
while True:
    # Receive object from worker
    img_dict = worker_socket.recv_pyobj()

    # Save received file
    f = open(img_dict['name'], 'wb')
    f.write(img_dict['data'].getvalue())
    f.close()

    # Send successful message
    print("Finished converting %s" % img_dict['name'])
    vent_socket.send_string("Finished converting %s" % img_dict['name'])