from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file(input_file, output_file, key):
    backend = default_backend()
    iv = os.urandom(16)  # Generate a random IV for each encryption

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()

    with open(input_file, "rb") as f:
        plaintext = f.read()

    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    with open(output_file, "wb") as f:
        f.write(iv + ciphertext)

def decrypt_file(input_file, output_file, key):
    backend = default_backend()

    with open(input_file, "rb") as f:
        data = f.read()

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_plaintext = unpadder.update(decrypted_padded) + unpadder.finalize()

    with open(output_file, "wb") as f:
        f.write(decrypted_plaintext)

if __name__ == "__main__":
    key = b"CES6IGcVY7ABGsHr4WRx6YLClzyWFuKz7aInK72cpa4wKr8Bm2CdEWVS0OA8ZYymVN+ywM6pI776YcymGqOvMnLCGsSyIisjHiVms80TTN24Ct3vHyEUSwCMU3tZET5kxXZ2Yb4RYR3rMu2eyVzWzxVMAymmZtXe7xb991kK53liW1pvG+8Y7y1W2s+X9csN"
    input_image = 'D:/Userdata/Pictures/id/IMG-20230519-WA0001.jpg'
    encrypted_image = "encrypted_image.enc"
    decrypted_image = "decrypted_image.jpg"

    encrypt_file(input_image, encrypted_image, key)
    print("Image encrypted.")

    decrypt_file(encrypted_image, decrypted_image, key)
    print("Image decrypted.")
