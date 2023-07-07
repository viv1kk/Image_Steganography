from modules.libs import Encode, Decode
from modules.AES import AESCipher

def encode():
    print("\nENCODE\n\n")
    image_path = input("Enter the base image path : ")
    message = input("Enter the message : ")
    password = input("Enter the Password : ")

    aes = AESCipher()
    encryped_message = aes.encrypt(message, password)
    encoded = Encode(image_path, encryped_message)
    download_path = input("Download Path with name for stego image : ")
    encoded.debugInfo()
    encoded.download(download_path)
    # encoded.showImages()

def decode():
    print("\nDECODE\n\n")
    image_path = input("Enter the stego image path : ")
    password = input("Enter the Password : ")
    decoded = Decode(image_path)
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



mode = input("Encode = 0, Decode = 1 : ")
if mode == "0":
    encode()
else:
    decode()