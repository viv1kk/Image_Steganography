import cv2
import numpy as np
import datetime

CHAR_SIZE = 8
RESERVED_BUFFER_FOR_MESSAGE_SIZE = 64 #total 64 bits

class Encode():
    def __init__(self, path, message):
        self.image_path = path
        self.img = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        self.height, self.width, self.channel = self.img.shape
        self.message = message
        self.bin_msg = self.asciiAsBinary(self.message)
        self.encoded_image = self.encode()
        # self.download()

    def download(self, path):
        cv2.imwrite(path, self.encoded_image)

    def asciiAsBinary(self, message):
        msg_ascii = []
        msg_bin_str = ""

        for i in range(len(message)):
            msg_ascii.append(ord(message[i]))
            msg_bin_str += format(msg_ascii[i],'08b')
            # print(type(format(msg_ascii[i],'08b')))
        return msg_bin_str
    
    def is_similar(image1, image2):
        return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())

    # check whether the image can accomodate the complete messages
    def canImageStore(size, message):
        width, height = size
        bits_img = width*height

        bits_msg = len(message)*8
        if bits_msg > bits_img:
            return True
        else:
            return False

    def encode(self):
        image = np.copy(self.img)
        image = image.astype('uint16')
        ind  = 0
        msg_len_str = format((len(self.bin_msg)//CHAR_SIZE),'064b')
        
        #now message contains the length of string and the message.
        self.bin_msg = msg_len_str+self.bin_msg
        # print(bin_msg)
        height, width, channel = image.shape

        for y in range(0, height):
            for x in range(0, width):
                if ind == len(self.bin_msg):
                    image = image.astype('uint8')
                    return image
                b = image[y,x,0]
                g = image[y,x,1]
                r = image[y,x,2]
                
                if int(self.bin_msg[ind]) == 0:
                    if (r+g+b)%2 == 0:
                        if r == 0:
                            image[y,x,2] += 1
                        else:
                            image[y,x,2] -= 1
                else:
                    if (r+g+b)%2 == 1:
                        if r == 255:
                            image[y,x,2] -= 1
                        else:
                            image[y,x,2] += 1
                ind += 1
        image = image.astype('uint8')
        self.encoded_image = image
        return image

    def debugInfo(self):
        height, width, channel = self.encoded_image.shape
        with open('./debug/encode_debug.txt', 'w') as f:
            # (8*2) beacuase the characters are unicode (UTF-16) characters and it takes 16 bits to represent it
            f.write(f"{datetime.datetime.now()}\n")
            f.write(f"Total number of Pixels : {height*width}\n")
            f.write(f"Max number of characters can be accomodated : {(height*width)//(8*2)} characters\n")
            f.write(f"Number of Bits occupied by the Message : {len(self.bin_msg)-RESERVED_BUFFER_FOR_MESSAGE_SIZE} bits\n")
            f.write(f"Number of Bits occupied by Message Length : {RESERVED_BUFFER_FOR_MESSAGE_SIZE} bits\n")
            f.write(f"Total Number of Bits occupied by Message: {len(self.bin_msg)} bits\n")
            f.write(f"Total number of characters + meta accomodated : {len(self.bin_msg)//(8*2)} characters\n")
            f.write(f"Avaliable space : {((height*width)//8)-(len(self.bin_msg)//(8*2))} characters\n")
            f.write(f"Total space Left unused : {(height*width)-(len(self.bin_msg)+RESERVED_BUFFER_FOR_MESSAGE_SIZE)} bits\n\n")
            f.write(f"\n")
            f.write(f"Encrypted String (AES_CBC) :\n{self.message}")
        

    def showImages(self):
        cv2.namedWindow('Image 1', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Image 2', cv2.WINDOW_NORMAL)

        # Display the images in their respective windows
        cv2.imshow('Image 1', self.img)
        cv2.imshow('Image 2', self.encoded_image)
        cv2.waitKey(0)


class Decode():
    def __init__(self, path):
        self.path = path
        self.img = self.loadImage()
        self.secret_encryped_message = self.decode()

    def debugInfo(self):
        height, width, channel = self.img.shape
        with open('./debug/decode_debug.txt', 'w') as f:
            f.write(f"{datetime.datetime.now()}\n")
            f.write(f"Total number of Pixels : {height*width}\n")
            f.write(f"Size of message in bits : {len(self.secret_encryped_message)*8} bits\n\n")
            f.write(f"Encrypted String (AES_CBC) :\n{self.secret_encryped_message}\n")

    def loadImage(self):
        return cv2.imread(self.path)
    
    def extractMessage(self, bin):
        message = ""
        message_string_length = int(bin[:RESERVED_BUFFER_FOR_MESSAGE_SIZE], 2)
        message_len_in_bin = message_string_length*CHAR_SIZE
        if message_len_in_bin+RESERVED_BUFFER_FOR_MESSAGE_SIZE > self.img.shape[0]*self.img.shape[1]:
            return 0
        for x in range(RESERVED_BUFFER_FOR_MESSAGE_SIZE, RESERVED_BUFFER_FOR_MESSAGE_SIZE+message_len_in_bin, CHAR_SIZE):
            character = chr(int(bin[x:x+CHAR_SIZE], 2))
            message += character
        return message

    def decode(self):
        image = np.copy(self.img)
        image = image.astype('uint16')
        height, width, channel = image.shape

        raw_bin = ""
        for y in range(0, height):
            for x in range(0, width):
                b = image[y,x,0]
                g = image[y,x,1]
                r = image[y,x,2]

                if (r+g+b)%2 == 0:
                    raw_bin += '1'
                else:
                    raw_bin += '0'
        message = self.extractMessage(raw_bin)
        # message = raw_bin
        return message