# RSACryptosystem

Encrypts a given plaintext file using the RSA cryptosystem and a random key of the given prime number bitlength

COMMAND LINE ARGS
- (1) plainTextFileName - Name of the plaintext file to be encrypted
- (2) cipherTextFile - Name of the file to be created containing the generated cipher
- (3) decryptedTextFile - Name of the file to be created containing the decryption
- (4) bitLength - Number of bits of primes p and q. Must be between 8 and 2048 inclusive

Generates two psuedo-random prime numbers, p and q, and multiplies them together to create n of approx. twice the bit length of the primes.
Calculates phi(n) given p and q. Chooses a random valid e and calculates d as the modular inverse of e mod phi(n) using the 
pulverizer algorithm (aka Extended Euclidean algorithm)

OUTPUT FILES:
- cipherTextFile - The encryption of each individual character (using it's Unicode point value). Each new line represents one character.
- decryptedTextFile - The decryption of the cipher text. Assuming normal execution, contents should be identical to plainTextFile
- keys.txt - Each key value used in the encryption/decryption process
