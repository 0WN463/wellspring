from string import ascii_lowercase
from .optional import Optional
from itertools import cycle, islice

class SubstitutionCipher:
    def __init__(self, key):
        self.domain = ascii_lowercase + ' '
        assert len(key) == len(self.domain)
        self.key = key
        self.table = {a:b for a,b in zip(self.domain, key)}
        self.rtable = {b:a for a,b in zip(self.domain, key)}
    
    def __repr__(self):
        return f'Substitution Table:\n{self.domain}\n{self.key}'
    
    def encrypt(self, message):
        return ''.join(map(lambda x: self.table[x], message))
        
    def decrypt(self, message):
        return ''.join(map(lambda x: self.rtable[x], message))

class ShiftCipher:
    def __init__(self, key):
        self.domain = ascii_lowercase
        self.key = key
        
    def __repr__(self):
        return f'ShiftCipher(shift={self.key})'
    
    def encrypt(self, message):
        indices = map(lambda x: Optional.from_func(lambda: self.domain.index(x)), message)
        shift = lambda opt: (opt + self.key) % len(self.domain)
        shifted_indices = Optional.map_over(shift, indices)
        encrypted = Optional.map_over(lambda opt: self.domain[opt], shifted_indices)
        return ''.join(map(lambda elem: 
                           elem[1].value
                           if not elem[1].isEmpty
                           else elem[0], 
                           zip(message, encrypted)))
        
    def decrypt(self, message):
        indices = map(lambda x: Optional.from_func(lambda: self.domain.index(x)), message)
        shift = lambda opt: (opt + len(self.domain) - self.key) % len(self.domain)
        shifted_indices = Optional.map_over(shift, indices)
        decrypted = Optional.map_over(lambda opt: self.domain[opt], shifted_indices)
        return ''.join(map(lambda elem: 
                           elem[1].value
                           if not elem[1].isEmpty
                           else elem[0], 
                           zip(message, decrypted))) 

class VigenereCipher:
    def __init__(self, keyword):
        self.domain = ascii_lowercase
        self.key = keyword
        
    def __repr__(self):
        return f'ViginereCipher(keyword={self.key})'
    
    def encrypt(self, message):
        indices = map(lambda x: Optional.from_func(lambda: self.domain.index(x)), message)
        shift_amounts = islice(cycle(map(lambda x: self.domain.index(x), self.key)), len(message))
        shifts = map(lambda amt: lambda opt: (opt + amt) % len(self.domain), shift_amounts)
        shifted_indices = Optional.zip_with(shifts, indices)
        encrypted = Optional.map_over(lambda opt: self.domain[opt], shifted_indices)
        return ''.join(map(lambda elem: 
                           elem[1].value
                           if not elem[1].isEmpty
                           else elem[0], 
                           zip(message, encrypted)))
        
    def decrypt(self, message):
        indices = map(lambda x: Optional.from_func(lambda: self.domain.index(x)), message)
        shift_amounts = islice(cycle(map(lambda x: self.domain.index(x), self.key)), len(message))
        shifts = map(lambda amt: lambda opt: (opt + len(self.domain) - amt) % len(self.domain), shift_amounts)
        shifted_indices = Optional.zip_with(shifts, indices)
        decrypted = Optional.map_over(lambda opt: self.domain[opt], shifted_indices)
        return ''.join(map(lambda elem: 
                           elem[1].value
                           if not elem[1].isEmpty
                           else elem[0], 
                           zip(message, decrypted)))

class PermutationCipher:
    def __init__(self, permutation, padding='|'):
        self.key = permutation
        self.padding = padding
        
    def __repr__(self):
        return f'PermutationCipher(permutation={self.key})'
 
    def _pad(self, message):
        padding_size = len(self.key) - len(message) % len(self.key)
        return message + padding_size * self.padding
    
    def _unpad(self, message):
        return message.strip(self.padding)
    
    def encrypt(self, message):
        padded_message = self._pad(message)
        
        blocks = [padded_message[i:i+len(self.key)] for i in range(0, len(message), len(self.key))]
        shuffled_blocks = [[block[self.key.index(i)] for i in range(len(self.key))] for block in blocks]
        
        return ''.join([''.join(block) for block in shuffled_blocks])
        
    def decrypt(self, message):        
        blocks = [message[i:i+len(self.key)] for i in range(0, len(message), len(self.key))]
        shuffled_blocks = [[block[idx] for idx in self.key] for block in blocks]
        padded_plaintext = ''.join([''.join(block) for block in shuffled_blocks])
        return self._unpad(padded_plaintext)
        
class OneTimePad:
    def __init__(self, bitstream):
        self.bitstream = bitstream
        
    def __repr__(self):
        return f'OneTimePad(bitstream={self.bitstream})'
     
    def encrypt(self, message_bytes):
        assert len(message_bytes) <= len(self.bitstream)
        random_bytes = self.bitstream[:len(message_bytes)]
        cipher_bytes = bytes(message_byte ^ random_byte for message_byte, random_byte in zip(message_bytes, random_bytes))
        
        self.bitstream = self.bitstream[len(message_bytes):]
        return cipher_bytes
        
    def decrypt(self, message):        
        return self.encrypt(message) 
