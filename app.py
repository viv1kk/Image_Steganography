from modules.libs import Encode, Decode
from modules.AES import AESCipher

def encode():
    message = input("Enter the message : ")
    password = input("Enter the Password : ")

    aes = AESCipher()
    encryped_message = aes.encrypt(message, password)
    encoded = Encode("image/image2.jpg", encryped_message)
    encoded.debugInfo()
    # encoded.showImages()

def decode():
    password = input("Enter the Password : ")
    decoded = Decode("image/asd.png")
    decoded.debugInfo()
    if decoded.secret_encryped_message:
        aes = AESCipher()
        decrpted_message = aes.decrypt(decoded.secret_encryped_message, password)
        if decrpted_message:
            print(f"Hidden Message: {decrpted_message}")
        else:
            print("Error! Check Password or Image")
    else:
        print("Error, The Image is not Valid!")
encode()
decode()