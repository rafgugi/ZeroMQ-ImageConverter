import os
from PIL import Image
import StringIO
import zmq

print("Start worker")

#fungsi untuk mengambil format gambar dari suatu file
#--format gambar dilihat dari ekstensinya (.png, .jpg, dan lain-lain)
def get_format(filename):
    img_format = filename[filename.rfind('.')+1:].upper()
    if (img_format == 'JPG'):
        img_format = 'JPEG'
    return img_format

context = zmq.Context()

# Socket to receive messages on
vent_socket = context.socket(zmq.PULL)
vent_socket.connect('tcp://localhost:5557')

# Socket to send messages to
sink_socket = context.socket(zmq.PUSH)
sink_socket.connect('tcp://localhost:5558')

# Process tasks forever
while True:
    img_dict = vent_socket.recv_pyobj();
    print("Receive file %s, starting the process" % img_dict['name'])
    try:
        # Get the image format
        img_format = get_format(img_dict['name'])

        # Get the image
        img = Image.open(img_dict['data'])

        # Convert to grayscale
        img = img.convert('L')

        # Save new image
        data = StringIO.StringIO()
        img.save(data, img_format)
        img_dict['data'] = data

        # Send converted image to sink
        print(" - Send converted image to sink.")
        sink_socket.send_pyobj(img_dict)
        print(" - Success sending %s" % img_dict['name'])
    except Exception as e:
        print("Error: %s" % e)