class Rotor:
    def __init__(self):
        self.uppercase_base = ord('A')
        self.lowercase_base = ord('a')
        self.alphabet_length = 26

    def is_uppercase(self, char):
        return 'A' <= char <= 'Z'

    def is_lowercase(self, char):
        return 'a' <= char <= 'z'

    def getChar(self, current_char, shift):
        if self.is_uppercase(current_char):
            base = self.uppercase_base
        elif self.is_lowercase(current_char):
            base = self.lowercase_base
        else:
            return current_char  

        shifted_char = chr((ord(current_char) - base + shift) % self.alphabet_length + base)
        return shifted_char

rotor = Rotor()
encrypted_char = rotor.getChar('A', 3)
print(encrypted_char)