import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad

class AESCipher():
    def __init__(self):
        self.block_size = AES.block_size
    
    def encrypt(self, plain_text, key):
        # plain_text = self.__pad(plain_tCext)
        plain_text = pad(plain_text.encode('utf-8'), self.block_size, style='pkcs7')
        key = hashlib.sha256(key.encode()).digest()
        iv = Random.new().read(self.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text)
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text, key):
        encrypted_text = b64decode(encrypted_text)
        key = hashlib.sha256(key.encode()).digest()
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        try:
            plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
            # return self.__unpad(plain_text)
            return unpad(plain_text.encode("utf-8"), self.block_size, style="pkcs7").decode("utf-8")
        except ValueError:
            # print("Wrong password")
            return 0

    # def __pad(self, plain_text):
    #     number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
    #     ascii_string = chr(number_of_bytes_to_pad)
    #     padding_str = number_of_bytes_to_pad * ascii_string
    #     padded_plain_text = plain_text + padding_str
    #     return padded_plain_text

    # @staticmethod
    # def __unpad(plain_text):
    #     last_character = plain_text[len(plain_text) - 1:]
    #     return plain_text[:-ord(last_character)]
    
# aes = AESCipher()
# enc = aes.encrypt("HELLO this is VIVEK","sdfsdfs")
# print(enc)

# dec = aes.decrypt(enc, "sdfsdfs")
# print(dec)