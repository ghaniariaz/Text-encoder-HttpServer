import socket
from PIL import Image

def create_rgbarray(img,len):
    counter = 0
    width,height = img.size
    L=[]
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            L.append(r)
            L.append(g)
            L.append(b)
            counter+=1
            if counter==len:
                break
        if counter==len:
            break
    return L

def create_bitarray(message):
    L = []
    for ch in message:
        Y = get_bit(ch)
        for obj in Y:
            L.append(obj)
    return L

def get_bit(ch):
    L = []
    asc  = ord(ch)
    for i in range(8):
        L.append(asc & pow(2,i) != 0)
    return L

def createLengthArray(length):
    L = []
   # asc  = ord(ch)
    for i in range(8):
        L.append(length & pow(2,i) != 0)
    return L

def setbit(oldbyte,newbit):
    if newbit:
        return oldbyte | newbit
    else:
        return oldbyte & 0b11111110

def set_bit(v, index, x):
  mask = 1 << index
  v &= ~mask
  if x:
    v |= mask
  return v

def decode_image(img):
   
    width, height = img.size
    msg = ""
    index = 0
    length =0
    rgbarray = create_rgbarray(img,8)
    for j in range(8):
        bit = rgbarray[j] & 1
        length = set_bit(length,j,bit)
    rgbarray = create_rgbarray(img,length*8)
    msg=""
    ch = 0
    for i in range(length*8):
        bit = rgbarray[i+8] & 1
        if (i%8==0) & (i!=0):
            msg += chr(ch)
            ch = 0
        ch = set_bit(ch,i%8,bit)
    msg+=chr(ch)
    return msg
# Set up a TCP/IP socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Connect as client to a selected server
# on a specified port
print("Enter filename")
filename = input()
s.connect(("localhost",5555))
prevresp = ""
resp = ""
data = ""
request = "GET /"+filename+" HTTP/1.0\n\n"
# Protocol exchange - sends and receives
s.send(request.encode('utf-8'))
f = open("a.png", "wb")
while True:
        prevresp = resp
        resp = s.recv(1024)
        if "404".encode('utf-8') in resp:
            print("File not found")
            exit()
        if resp == prevresp: 
            break
        else:
            f.write(resp)
f.close()

img2 = Image.open("a.png")
hidden_text = decode_image(img2)
print("Hidden text:\n{}".format(hidden_text))

# Close the connection when completed
s.close()
print ("\ndone")
