# RSA.py
# 
# Encrypts a given plaintext input file using the RSA cryptosystem and a random key of the given bitlength
# 
# COMMAND LINE ARGS
# (1) plainTextFileName - Name of the plaintext file to be encrypted
# (2) cipherTextFile - Name of the file to be created containing the generated cipher
# (3) decryptedTextFile - Name of the file to be created containing the decryption
# (4) bitLength - Number of bits of n. Must be between 8 and 1024 inclusive
#
# Generates two prime numbers, p and q, and multiplies them together to create an n of the given bit length.
# Calculates phi(n) given p and q. Chooses a random valid e and calculates it's modular inverse using the pulverizer
# algorithm. 
#
# OUTPUT FILES:
# cipherTextFile - The encryption of each individual character (using it's Unicode point value). Each new line represents on character.
# decryptedTextFile - The decryption of the cipher text. Assuming normal execution, contents should be identical to plainTextFile
# keys.txt - Each key value used in the encryption/decryption process
# 
# @author Nicholas Dombroski
# @email dombronm202@potsdam.edu
# @course CIS 475 Intro to Cryptography
# @assignment RSA programming assignment

import sys
import math
from math import sqrt
import random

def main():
    # Parse command line arguments
    try:
        sys.argv[1]
    except IndexError:
        raise Exception("Please supply a plain text file name")
    plainTextFileName = sys.argv[1]

    try:
        open(plainTextFileName,'r')
    except FileNotFoundError:
        raise Exception("File does not exist")
    plainTextFile = open(plainTextFileName,'r')

    try:
        sys.argv[2]
    except IndexError:
        raise Exception("Please supply a name for the file to  output the cipher text")
    cipherTextFile = sys.argv[2]

    try:
        sys.argv[3]
    except IndexError:
        raise Exception("Please supply a name for the file to  output the decrypted text")
    decryptedTextFile = sys.argv[3]

    try:
        sys.argv[4]
    except IndexError:
        raise Exception("Please supply a bitlength for n")
    bitLength = int(sys.argv[4])
    if bitLength < 8 or bitLength > 1024:
        raise Exception("Bit length must be between 8 and 1024 inclusive")
    
    # Generate p and q
    p = getRandomPrime(bitLength/2)
    q = getRandomPrime(bitLength/2)

    # Calculate n and phi(n)
    n = p*q
    phi = (p-1) * (q-1)

    # Generate an e and find d: inverse of e mod phi(n)
    e = getE(phi)
    d, throwaway = modInverse(e, phi)

    # Create encryption and decryption files
    unicodeVals = getUnicode(plainTextFile)
    encrypt(cipherTextFile, unicodeVals, e, n)
    decrypt(cipherTextFile, decryptedTextFile, d, n)

    # Write the key values to the file keys.txt
    keys = open("keys.txt",'w')
    keys.write("Bitlength used: " + str(bitLength) + "\n")
    keyString = "n: " + str(n) + "\np: " + str(p) + "\nq: " + str(q) + "\nphi(n): " + str(phi) + "\ne: " + str(e) + "\nd (secret exponent): " + str(d)
    keys.write(keyString)

    
# Returns a random prime number of the given bit length
# @param bitLength - number of bits the random prime number should be
# @return - a random prime int of the given bit length
def getRandomPrime(bitLength):
    while(True):
        p = random.randint(pow(2,bitLength-1)+1,pow(2,bitLength)-1)
        if isPrime(p):
            return p

# Returns True if input is a likely prime number, using Fermat's primality test
# @param n - The number to be checked if prime
# @return - True if n is a likely prime, False otherwise
def isPrime(n):
    if n == 1 or n % 2 == 0:
        return False
    for _ in range(0,1000):
        a = random.randint(2,n-2)
        if a % n == 0:
            continue
        if not pow(a,n-1,n) == 1:
            return False
    return True

# Returns a random integer e such that gcd(e,phi(n))=1
# @param phi - the value of phi(n)
# @return - a valid e value
def getE(phi):
    while(True):
        e = random.randint(1,int(sqrt(phi)))
        if math.gcd(e,phi) == 1:
            return e

# Implementation of the pulvarizer algorithm
# @param x - the number to find the inverse of
# @param modulus - the modulus value for which the inverse of x should be found on
# @return The inverse of x % modulus
def modInverse(x, modulus):
    A = modulus
    B = x
    Q = (A//B)
    R = A % B
    x1, y1, x2, y2 = 1, 0, 0, 1
    while(not R == 0):
        new_x2 = x1 - (Q*x2)
        new_y2 = y1 - (Q*y2)
        A = B 
        B = R 
        Q = int(A/B)
        R = A % B
        x1, y1 = x2, y2
        x2, y2 = new_x2, new_y2
    return y2 % modulus, x2 % modulus

# Parses a text file and returns a list of it's unicode values
# @param plainText - The plaintext file, opened in read mode
# @return A list of unicode values that make up the file's text
def getUnicode(plainTextFile):
    plainText = plainTextFile.read()
    unicodeVals = []
    for i in range(0,len(plainText)):
        unicodeVals.append(ord(plainText[i]))
    return unicodeVals

# Encrypts each value in unicodeVals using e and n and prints each resulting value onto a new line in the specified file
# @param cipherTextFile - the name of the file to output the cipher to
# @param unicodeVals - A list of unicode values representing the input plain text
# @param e - The public exponent
# @param n - the modulus value
def encrypt(cipherTextFile, unicodeVals, e, n):
    output = open(cipherTextFile,'w')
    for m in range(0,len(unicodeVals)):
        output.write(str(pow(unicodeVals[m],e,n)))
        output.write("\n")

# Parses the values of cipherTextFile, applies the decryption formula to each value and prints the result to decryptedTextFile
# @param cipherTextFile - The name of the file containing the generated cipher
# @param decryptedTextFile - The name of the file to ouput the decryption to
# @param d - the secret exponent
# @param n - the modulus value
def decrypt(cipherTextFile, decryptedTextFile, d, n):
    ciphers = open(cipherTextFile, 'r')
    output = open(decryptedTextFile, 'w')
    while(True):
        c = ciphers.readline()
        if not c:
            break
        m = pow(int(c),d,n)
        output.write(chr(m))
        
if __name__=="__main__":
    main()