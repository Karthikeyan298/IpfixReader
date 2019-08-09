import socket
from ipfix import reader, template, ie
from struct import unpack

UDP_IP = "127.0.0.1"
UDP_PORT = 5000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
mbuf = reader.message.MessageBuffer()

ie.use_iana_default()
# myie = ie.for_spec("myNewInformationElement(41916/4322)<int>")
# ie._register_ie(myie)

def print_msg(msg):
    print("=======================TEMPLATES=========================")
    print(msg.templates)
    print("=========================================================")
    for rec in msg.namedict_iterator():
        print("RECORD: {}".format(rec))
        for key in rec:
            if key == "_ipfix_41916_4322":
                print("============================")
                print(len(rec[key]))
                print(unpack(">I", rec[key])[0])
                print("============================")
            if key == "_ipfix_41916_4321":
                print("============================")
                print(unpack(">Q", rec[key])[0])
                print("============================")




while True:
    data, addr = sock.recvfrom(4096) # buffer size is 1024 bytes
    mbuf.from_bytes(data)

    print(mbuf.get_export_time())
    try:
        print_msg(mbuf)
    except Exception as e:
        print("ERROR: {}".format(e))
