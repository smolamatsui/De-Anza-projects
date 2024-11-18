from io import BytesIO
import tkinter as tk
from tkinter import ttk
from tkinter import *

class BitString:
    def __init__(self,string='Hi'):
        self.__string = string
        self.__commandmap = {
            'bits': self._toBits,
            'bytes': self._toBytes,
            'bitstring': self._toBitString,
            'bytearray': self._toByteArray,
            'byteIO': self._toBytesIO
        }
        self.__conversions = {}

    def getString(self):
        #get the current string value
        return self.__string
    
    def setString(self,string):
        #set string before use to hide the data. Validate user input
        if not isinstance(string, str):
            raise ValueError("Input must be a string")
        self.__string = string

    def _toBits(self):
        #converting string to bits
        bit = [format(ord(char), '08b') for char in self.__string]
        return bit
    
    def _toBytes(self):
        #converting string to bytes
        byte = bytes(self.__string, 'utf-8')
        return repr(byte)
    
    def _toBitString(self):
        #converting string to bitstring
        bitString = ''.join(format(ord(char), '08b') for char in self.__string)
        return bitString
    
    def _toByteArray(self):
        #converting string to bytearray
        byteArray = bytearray(self.__string, 'utf-8')
        return byteArray
    
    def _toBytesIO(self):
        #converting string to byteIO
        binary_buffer = BytesIO()
        bytes_obj = self._toBytes()#use bytes function 
        binary_buffer.write(bytes_obj)
        result_bytes = binary_buffer.getvalue()
        return result_bytes
    
    def bitToString(self,bit):
        #convert bit back to string
        string = ''.join(chr(int(b, 2)) for b in bit)
        return string
    
    def byteToString(self,byte):
        #convert byte back to string
        string = byte.decode('utf-8')
        return string
    
    def __getitem__(self,command):
        #allow user to directly access dictionary
        if command in self.__commandmap:
            result = self.__commandmap[command]()
            self.__conversions[command] = result
            return result
        raise KeyError(f"Conversion '{command}' not supported.")

    def __iter__(self):
        #iterate through commands
        self.__current = iter(self.__commandmap.keys())
        return self
    
    def __next__(self):
        #getting the next element of the iteration
        return next(self.__current)
           
    def __str__(self):
        #return string representation of all the conversions done
        if not self.__conversions:
            return "No conversions done yet"
        output = "Conversions: \n"
        for key, value in self.__conversions.items():
            output += f"{key.capitalize()}: {value}\n"
        return output

#creating tkinter interface for string conversion
class StringApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("String Converter")
        self.geometry("650x400")
        self.BitString = BitString()
        self.create_widgets()
    
    def create_widgets(self):
        #create string label
        self.stringlabel = tk.Label(self, text="Enter in string:")
        self.stringlabel.grid(row=0, column =0, padx=10, pady=10, sticky='w')

        #create entry for string
        self.validateCommand = self.register(self.validateInput)
        self.textEntry = tk.Entry(self, width = 50, validate="key", validatecommand=(self.validateCommand, '%P'))
        self.textEntry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        #create label for conversion
        self.conversiontypelabel = tk.Label(self, text = "Conversion type")
        self.conversiontypelabel.grid(row=1, column =0, padx=10, pady=10, sticky='w')

        #create combobox for conversion options
        commands = list(self.BitString)
        self.comboBox = ttk.Combobox(self, values=commands,state="readonly")
        self.comboBox.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.comboBox.set(commands[0])

        #create conversion button
        self.convertbutton = tk.Button(self, text="Convert", width=6, command = self.convertString)
        self.convertbutton.grid(row=1, column=2, padx=10, pady=10, sticky='w')

        #output label
        self.outputlabel = tk.Label(self, text="Output")
        self.outputlabel.grid(row=2, column =0, padx=10, pady=10, sticky='w') 

        #output frame
        self.outputFrame = tk.Frame(self)
        self.outputFrame.grid(row=2, column =1, padx=10, pady=10, sticky='w')

        #output box
        self.box = tk.Text(self.outputFrame, height=5, width=50)
        self.box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.box.config(state=tk.DISABLED)

        #scrollbar for output box
        self.scrollbar = tk.Scrollbar(self.outputFrame, command=self.box.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.box.config(yscrollcommand=self.scrollbar.set)

    def convertString(self):
        #converting string to output
        inputString = self.textEntry.get()
        self.BitString.setString(inputString)

        conversionType = self.comboBox.get()
        try:
            result = self.BitString[conversionType]
        except KeyError as e:
            result = str(e)
        
        self.box.config(state=tk.NORMAL)
        self.box.delete(1.0, tk.END)
        self.box.insert(tk.END, result)
        self.box.config(state=tk.DISABLED)
    
    def validateInput(self,value):
     #handling error if user puts in an integer   
        if all(char.isalpha() or char.isspace() for char in value):
            return True
        else:
            self.show_error_message("Invalid input", "Please enter only string values (no numbers).")
            return False
        
    def show_error_message(self, title, message):
        #creating error window 
        error_window = tk.Toplevel(self)
        error_window.title(title)
        error_window.geometry("400x200")  
        
        # Create a text widget for the message
        text_box = tk.Text(error_window, wrap=tk.WORD, height=8, width=50)
        text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text_box.insert(tk.END, message)
        text_box.config(state=tk.DISABLED)
        

if __name__ == "__main__":
    app = StringApplication()
    app.mainloop()

