class PNBT:
    base_map = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def __init__(self, value, base):
        self.base = base.upper()
        self.value = str(value) 
        self.base_value = PNBT.base_map.index(self.base)

    def __str__(self):
        return f"{self.base}x{self.value_in_base()}"
    
    def value_in_base(self):
        decimal_value = self.to_decimal()  
        digits = []

        if decimal_value == 0:
            return '0'       
        while decimal_value > 0:
            digits.append(PNBT.base_map[decimal_value % self.base_value])
            decimal_value //= self.base_value
        return ''.join(reversed(digits))  

    def to_decimal(self):
        decimal = 0
        for digit in self.value:
            digit_value = PNBT.base_map.index(digit)
            decimal = decimal * self.base_value + digit_value
        return decimal
    
    def from_decimal(self, decimal_value, base):
        base_value = PNBT.base_map.index(base)
        digits = []
        while decimal_value > 0:
            digits.append(PNBT.base_map[decimal_value % base_value])
            decimal_value //= base_value
        return ''.join(reversed(digits)) if digits else '0'


    def __add__(self, other):
        result_decimal = self.to_decimal() + other.to_decimal()
        highest_base = max(self.base_value, other.base_value)
        highest_base_char = PNBT.base_map[highest_base]
        result_value = self.from_decimal(result_decimal, highest_base_char)
        return PNBT(result_value, highest_base_char)

    def __sub__(self, other):
        result_decimal = self.to_decimal() - other.to_decimal()
        highest_base = max(self.base_value, other.base_value)
        highest_base_char = PNBT.base_map[highest_base]
        result_value = self.from_decimal(result_decimal, highest_base_char)
        return PNBT(result_value, highest_base_char)

    def __mul__(self, other):
        result_decimal = self.to_decimal() * other.to_decimal()
        highest_base = max(self.base_value, other.base_value)
        highest_base_char = PNBT.base_map[highest_base]
        result_value = self.from_decimal(result_decimal, highest_base_char)
        return PNBT(result_value, highest_base_char)

    def __truediv__(self, other):
        result_decimal = self.to_decimal() // other.to_decimal() 
        highest_base = max(self.base_value, other.base_value)
        highest_base_char = PNBT.base_map[highest_base]
        result_value = self.from_decimal(result_decimal, highest_base_char)
        return PNBT(result_value, highest_base_char)

    def __mod__(self, other):
        result_decimal = self.to_decimal() % other.to_decimal()
        highest_base = max(self.base_value, other.base_value)
        highest_base_char = PNBT.base_map[highest_base]
        result_value = self.from_decimal(result_decimal, highest_base_char)
        return PNBT(result_value, highest_base_char)
    
    
    def __lt__(self, other):
        return self.to_decimal() < other.to_decimal()

    def __eq__(self, other):
        return self.to_decimal() == other.to_decimal()

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return self.to_decimal() > other.to_decimal()

    def __ge__(self, other):
        return self > other or self == other

    def __ne__(self, other):
        return not self == other

#test sets from binarypdf

pn1 = PNBT("18G", 'S')
pn2 = PNBT("121", 'V') 

result = pn1 + pn2
print(result)

pn3 = PNBT("SJ", 'Z')
pn4 = PNBT("512", 'A') 

result = pn3 - pn4
print(result)

pn5 = PNBT("4344", '6')
pn6 = PNBT("101", '3') 

result = pn5 * pn6
print(result)

pn7 = PNBT("IO", 'K')
pn8 = PNBT("50", 'O') 

result = pn7 / pn8
print(result)

pn9 = PNBT("3F", 'W')
pn0 = PNBT("10", 'M') 

result = pn9 % pn0
print(result)

