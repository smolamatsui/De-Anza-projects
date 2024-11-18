import tkinter as tk
import io
import unittest

# Class for converting strings to and from bits/bytes
class BitstringConverter:
    def __init__(self, input_string):
        if not isinstance(input_string, str):
            raise ValueError("Input must be a string.")
        self._input_string = input_string
        self._conversions = {
            "Bits": self._to_bits,
            "Bytes": self._to_bytes,
            "BitString": self._to_bitstring,
            "ByteArray": self._to_bytearray,
            "BytesIO": self._to_bytesio,
            "From Bits": self._from_bits,
            "From Bytes": self._from_bytes,
        }

    def _to_bits(self):
        return ' '.join(f'{ord(c):08b}' for c in self._input_string)

    def _to_bytes(self):
        return ' '.join(f'{b:02x}' for b in self._input_string.encode('utf-8'))

    def _to_bitstring(self):
        return f"0b{' '.join(format(ord(c), '08b') for c in self._input_string)}"

    def _to_bytearray(self):
        return ' '.join(f'{b:02x}' for b in bytearray(self._input_string, 'utf-8'))

    def _to_bytesio(self):
        bytes_io = io.BytesIO(self._input_string.encode('utf-8'))
        return ' '.join(f'{b:02x}' for b in bytes_io.getvalue())

    def _from_bits(self, bits):
        try:
            byte_array = bytearray(int(bits[i:i + 8], 2) for i in range(0, len(bits), 9))  
            return byte_array.decode('utf-8')
        except ValueError:
            return "Invalid Bit Stream"

    def _from_bytes(self, byte_data):
        try:
            return bytes.fromhex(byte_data.replace(" ", "")).decode('utf-8')
        except (ValueError, AttributeError):
            return "Invalid Byte Stream"

    def convert(self, conversion_type):
        func = self._conversions.get(conversion_type)
        if func:
            if conversion_type in ["From Bits", "From Bytes"]:
                return func(self._input_string)
            return func()
        return "Unknown Conversion Type"

    def __str__(self):
        return f"BitstringConverter(input_string='{self._input_string}')"

    def __repr__(self):
        return f"BitstringConverter('{self._input_string}')"

    def __iter__(self):
        return iter(self._input_string)

    def __len__(self):
        return len(self._input_string)

    def __getitem__(self, index):
        return self._input_string[index]

    def __contains__(self, item):
        return item in self._input_string

    def __eq__(self, other):
        if isinstance(other, BitstringConverter):
            return self._input_string == other._input_string
        return False


# Class for the Tkinter application
class BitstringConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bitstring Converter App")

        # Input label
        self.input_label = tk.Label(root, text="Input String or Stream:", fg="black")
        self.input_label.grid(row=0, column=0, padx=10, pady=10)

        # Input box
        self.input_entry = tk.Entry(root, width=40, fg="white")
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)

        # Conversion type selection menu
        self.conversion_type = tk.StringVar(root)
        self.conversion_type.set("Bits") 
        self.type_menu = tk.OptionMenu(root, self.conversion_type,
                                        "Bits", "Bytes", "BitString",
                                        "ByteArray", "BytesIO",
                                        "From Bits", "From Bytes")
        self.type_menu.config(fg="black")
        self.type_menu.grid(row=1, column=0, padx=10, pady=10)

        # Convert button
        self.convert_button = tk.Button(root, text="Convert", command=self.convert, fg="black")
        self.convert_button.grid(row=1, column=1, padx=10, pady=10)

        # Output label
        self.output_label = tk.Label(root, text="Converted Output:", fg="black")
        self.output_label.grid(row=2, column=0, padx=10, pady=10)

        # Output box
        self.output_entry = tk.Entry(root, width=40, fg="white")
        self.output_entry.grid(row=2, column=1, padx=10, pady=10)

    def convert(self):
        input_string = self.input_entry.get()
        try:
            converter = BitstringConverter(input_string)
        except ValueError as ve:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, str(ve))
            return

        conversion_type = self.conversion_type.get()
        result = converter.convert(conversion_type)

        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, result)


# Create the main Tkinter window
root = tk.Tk()
app = BitstringConverterApp(root)
root.mainloop()


# Unit test class
class TestBitstringConverter(unittest.TestCase):

    def setUp(self):
        self.converter = BitstringConverter("Hello")

    def test_to_bits(self):
        expected_bits = '01001000 01100101 01101100 01101100 01101111'
        self.assertEqual(self.converter._to_bits(), expected_bits)

    def test_to_bytes(self):
        expected_bytes = '48 65 6c 6c 6f'
        self.assertEqual(self.converter._to_bytes(), expected_bytes)

    def test_to_bitstring(self):
        expected_bitstring = "0b01001000 01100101 01101100 01101100 01101111"
        self.assertEqual(self.converter._to_bitstring(), expected_bitstring)

    def test_to_bytearray(self):
        expected_bytearray = '48 65 6c 6c 6f'
        self.assertEqual(self.converter._to_bytearray(), expected_bytearray)

    def test_to_bytesio(self):
        expected_bytesio = '48 65 6c 6c 6f'
        self.assertEqual(self.converter._to_bytesio(), expected_bytesio)

    def test_from_bits(self):
        bits = '01101000 01100101 01101100 01101100 01101111'
        expected_string = 'hello'
        self.assertEqual(self.converter._from_bits(bits), expected_string)

    def test_from_bytes(self):
        byte_data = '48 65 6c 6c 6f'
        expected_string = 'Hello'
        self.assertEqual(self.converter._from_bytes(byte_data), expected_string)

    def test_invalid_from_bits(self):
        invalid_bits = 'xyz'
        self.assertEqual(self.converter._from_bits(invalid_bits), "Invalid Bit Stream")

    def test_invalid_from_bytes(self):
        invalid_bytes = 'invalid'
        self.assertEqual(self.converter._from_bytes(invalid_bytes), "Invalid Byte Stream")

    def test_convert(self):
        self.assertEqual(self.converter.convert("Bits"), self.converter._to_bits())
        self.assertEqual(self.converter.convert("Unknown"), "Unknown Conversion Type")

if __name__ == '__main__':
    unittest.main()
