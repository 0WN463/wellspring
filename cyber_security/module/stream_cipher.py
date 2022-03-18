from random import Random
from secrets import randbelow
""" For illustration purposes, we simply use the random package with a fixed seed to simulate a bitstream """
""" However, for secure implementation, one should use a cryptographically secure generator instead """
class StreamCipher:
    def __init__(self, seed):
        self.key = seed
        
    def __repr__(self):
        return f'StreamCipher(key={self.key})'
     
    def encrypt(self, message_bytes, iv=None):
        if iv is None:
            iv = randbelow(1000_000)
        
        keystream_generator = Random(self.key ^ iv)
        random_bytes = keystream_generator.randbytes(len(message_bytes))
        cipher_bytes = bytes(message_byte ^ random_byte for message_byte, random_byte in zip(message_bytes, random_bytes))
        return iv, cipher_bytes
        
    def decrypt(self, message):   
        iv, ciphertext = message
        
        return self.encrypt(ciphertext, iv)  
