import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict

# part 1
class Metric:
    def __init__(self):
        self.conversions = defaultdict(lambda: None, {
            'kg_to_lb': lambda x: x * 2.20462,
            'gram_to_oz': lambda x: x * 0.035274,
            'km_to_mi': lambda x: x * 0.621371,
            'meter_to_ft': lambda x: x * 3.28084,
            'cm_to_in': lambda x: x * 0.393701,
            'li_to_gal': lambda x: x * 0.264172,
            'mil_to_floz': lambda x: x * 0.033814,
        })

    def convert(self, value, unit):
        conversion = self.conversions.get(unit)
        if conversion is None:
            raise ValueError(f"Conversion for '{unit}' not found.")
        return conversion(value)

class Imperial:
    def __init__(self):
        self.conversions = defaultdict(lambda: None, {
            'lb_to_kg': lambda x: x * 0.453592,
            'oz_to_gram': lambda x: x * 28.3495,
            'mi_to_km': lambda x: x * 1.60934,
            'ft_to_meter': lambda x: x * 0.3048,
            'in_to_cm': lambda x: x * 2.54,
            'gal_to_li': lambda x: x * 3.78541,
            'floz_to_mil': lambda x: x * 29.5735,
        })

    def convert(self, value, unit):
        conversion = self.conversions.get(unit)
        if conversion is None:
            raise ValueError(f"Conversion for '{unit}' not found.")
        return conversion(value)

# part 2
class ConversionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        
        self.metric_converter = Metric()
        self.imperial_converter = Imperial()
        
        self.unit_system = tk.StringVar(value="Imperial")
        self.measurement_type = tk.StringVar(value="Weight")
        
        self.create_widgets()
    
    def create_widgets(self):

        style = ttk.Style()
        style.configure('Black.TRadiobutton', foreground='black')

        ttk.Label(self.root, text="Select Unit System:", foreground='black').grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(self.root, text="Imperial", variable=self.unit_system, value="Imperial", command=self.update_units, style='Black.TRadiobutton').grid(row=0, column=1)
        ttk.Radiobutton(self.root, text="Metric", variable=self.unit_system, value="Metric", command=self.update_units, style='Black.TRadiobutton').grid(row=0, column=2)
        ttk.Label(self.root, text="Select Measurement Type:", foreground='black').grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(self.root, text="Weight", variable=self.measurement_type, value="Weight", command=self.update_units, style='Black.TRadiobutton').grid(row=1, column=1)
        ttk.Radiobutton(self.root, text="Length", variable=self.measurement_type, value="Length", command=self.update_units, style='Black.TRadiobutton').grid(row=1, column=2)
        ttk.Radiobutton(self.root, text="Volume", variable=self.measurement_type, value="Volume", command=self.update_units, style='Black.TRadiobutton').grid(row=1, column=3)
        ttk.Label(self.root, text="Select Unit:", foreground='black').grid(row=2, column=0, sticky=tk.W)
        self.unit_listbox = tk.Listbox(self.root, height=4, exportselection=False)
        self.unit_listbox.grid(row=2, column=1, columnspan=3, sticky=tk.W+tk.E)
        self.update_units()
        ttk.Label(self.root, text="Value to Convert: ", foreground='black').grid(row=3, column=0, sticky=tk.W)
        self.input_value = ttk.Entry(self.root, foreground='black')
        self.input_value.grid(row=3, column=1, columnspan=3, sticky=tk.W+tk.E)
        ttk.Label(self.root, text="Converted Value: ", foreground='black').grid(row=4, column=0, sticky=tk.W)
        self.output_value = ttk.Entry(self.root, state='readonly', foreground='black')
        self.output_value.grid(row=4, column=1, columnspan=3, sticky=tk.W+tk.E)
        style = ttk.Style() # If i dont create a style again, the button turns into a radio type button
        style.configure('Custom.TButton', foreground='black') 
        convert_button = ttk.Button(root, text="Convert", command=self.convert, style='Custom.TButton')
        convert_button.grid(row=5, column=1, columnspan=3, sticky=tk.W+tk.E)
    
    def update_units(self):
        unit_system = self.unit_system.get()
        measurement_type = self.measurement_type.get()
        self.unit_listbox.delete(0, tk.END)

        if unit_system == 'Imperial':
            units = {
                'Weight': ['lb_to_kg', 'oz_to_gram'],
                'Length': ['mi_to_km', 'ft_to_meter', 'in_to_cm'],
                'Volume': ['gal_to_li', 'floz_to_mil']
            }.get(measurement_type, [])
        else:
            units = {
                'Weight': ['kg_to_lb', 'gram_to_oz'],
                'Length': ['km_to_mi', 'meter_to_ft', 'cm_to_in'],
                'Volume': ['li_to_gal', 'mil_to_floz']
            }.get(measurement_type, [])

        for unit in units:
            self.unit_listbox.insert(tk.END, unit)
        
    def convert(self):
        try:
            value = float(self.input_value.get())
            from_unit = self.unit_listbox.get(tk.ACTIVE)
            
            if not from_unit:
                raise ValueError("Select a unit to convert.")
            
            if self.unit_system.get() == "Imperial":
                converted_value = self.imperial_converter.convert(value, from_unit)
            else:
                converted_value = self.metric_converter.convert(value, from_unit)
            
            self.output_value.config(state='normal')
            self.output_value.delete(0, tk.END)
            self.output_value.insert(0, str(converted_value))
            self.output_value.config(state='readonly')
        except ValueError as e:
            messagebox.showerror("Conversion Error", str(e))
    
    def get_target_unit(self, from_unit):
        target_units = {
            'kg_to_lb': 'lb_to_kg', 'gram_to_oz': 'oz_to_gram',
            'km_to_mi': 'mi_to_km', 'meter_to_ft': 'ft_to_meter', 'cm_to_in': 'in_to_cm',
            'li_to_gal': 'gal_to_li', 'mil_to_floz': 'floz_to_mil'
        }
        return target_units.get(from_unit, None)


root = tk.Tk()
app = ConversionApp(root)
root.mainloop()
