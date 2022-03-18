def demonstrate_cipher(cipher, plaintext):
    print(cipher)
    print()
    ciphertext = cipher.encrypt(plaintext)
    print("Plaintext:".ljust(35), plaintext)
    print("Ciphertext/Encrypted plaintext:".ljust(35), ciphertext)
    print(f'Decrypted "{ciphertext if len(ciphertext) <= 20 else "ciphertext"}":'.ljust(35), cipher.decrypt(ciphertext))
