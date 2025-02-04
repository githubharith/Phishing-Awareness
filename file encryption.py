from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    return kdf.derive(password)

def encrypt_file(file_path, key, iv):
    with open(file_path, 'rb') as file:
        plaintext = file.read()
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(iv + ciphertext)

def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, 'rb') as encrypted_file:
        data = encrypted_file.read()
        iv = data[:16]
        ciphertext = data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    decrypted_file_path = encrypted_file_path[:-4]  # Remove the '.enc' extension
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

def main():
    action = input("Enter 'e' for encryption or 'd' for decryption: ").strip().lower()
    file_path = input("Enter the file path: ")
    password = input("Enter the password: ").encode('utf-8')
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)
    
    if action == 'e':
        encrypt_file(file_path, key, iv)
        print("File encrypted successfully.")
    elif action == 'd':
        decrypt_file(file_path, key)
        print("File decrypted successfully.")
    else:
        print("Invalid action. Please enter 'e' or 'd'.")

if __name__ == "__main__":
    main()
