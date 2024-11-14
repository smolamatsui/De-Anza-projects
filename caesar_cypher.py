def uppercase(i):
    return 65 <= ord(i) <= 90

def encrypt(secret, shift):
    encrypt = ""
    for x in secret:
        if ord(x) != 32:
            base = ord('A') if uppercase(x) else ord('a')
            encrypt += chr((ord(x) - base + shift) % 26 + base)
        else:
            encrypt += x

    return encrypt

def largest_frequency(string):
    freq = {}
    for i in string:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1

    inverse = [(value, key) for key, value in freq.items()]
    return max(inverse)[1]

def decrypt(string):
    if uppercase(largest_frequency(string)):
        shift = ord(largest_frequency(string)) - ord('E')
    else:
        shift = ord(largest_frequency(string)) - ord('e')

    message = ""
    for x in string:
        if ord(x) != 32:
            base = ord('A') if uppercase(x) else ord('a')
            message += chr((ord(x) - base - shift) % 26 + base)
        else:
            message += x

    return message

message = "MEET ME AT ELEPHANT LAKE"
print("When you encrypt " + message + " with the Caesar Cipher by a shift of 3, it becomes: " +  encrypt(message, 3)) #change the 3 to any number you would like to shift your message by.

code = "PHHW PH DW HOHSKDQW ODNH" #insert anything you would like to decrypt, that has been encrypted through a caesar cipher.
print("When you decrypt " + code + ", it becomes this: " + decrypt(code))
