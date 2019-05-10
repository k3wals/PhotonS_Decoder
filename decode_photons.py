'''*******************************************************************
* Project           : AnyCubic Photon S Print File Decoder
* Program name      : decode_photons.py
* Author            : Slawek Wojtysiak
* Date created      : May 8, 2019
* Purpose           : Show paramaters and images embedded in the print file
********************************************************************'''

import os
from pathlib import Path
import struct
import sys
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog

# Setup GUI
root = tk.Tk()
root.title("Photon S Print Parameters")
# root.geometry("500x500")
tk.Label(root, text="Print File Parameters", height=2, font="bold").grid(
    row=1, column=1)
tk.Button(root, text="Quit", command=root.destroy).grid(row=1, column=2)


# Check or get file to parse
if len(sys.argv) > 1:
    try:
        file_path = Path(sys.argv[1])
    except:
        print("Improper or no file provided as argument, opening file select dialog")
        exit()
else:
    try:
        file_path_name = tk.filedialog.askopenfilename(
            initialdir="/", title="Select *.photons file", filetypes=(("photons files", "*.photons"), ("all files", "*.*")))
        file_path = Path(file_path_name)
    except:
        print("Improper file chosen in dialog")
        file_path = Path.cwd().joinpath("testfile.photons")  # for testing purposes
        exit()

if file_path.exists() and file_path.is_file():
    data = Path(file_path).read_bytes()
else:
    print("File doesn't exist.")
    exit()

# File Print Parameters


class Print_Param:
    def __init__(self, paramater_name, byte_index, length, data_type, decoded_value):
        self.paramater_name = paramater_name
        self.byte_index = byte_index
        self.length = length
        self.data_type = data_type
        self.decoded_value = decoded_value


Print_Params = []  # list
Print_Params.append(Print_Param("Pixel Size", 6, 8, ">d", 0.0))
Print_Params.append(Print_Param("Layer Height", 14, 8, ">d", 0.0))
Print_Params.append(Print_Param("Exposure Time", 22, 8, ">d", 0.0))
Print_Params.append(Print_Param("Light Off Time", 30, 8, ">d", 0.0))
Print_Params.append(Print_Param("Bottom Exposure Time", 38, 8, ">d", 0.0))
Print_Params.append(Print_Param("Bottom Layers", 46, 4, ">i", 0))
Print_Params.append(Print_Param("Unknown Float 1", 50, 8, ">d", 0.0))
Print_Params.append(Print_Param("Unknown Float 2", 58, 8, ">d", 0.0))
Print_Params.append(Print_Param("Unknown Float 3", 66, 8, ">d", 0.0))
Print_Params.append(Print_Param("Unknown Float 4", 74, 8, ">d", 0.0))
Print_Params.append(Print_Param("Unknown Int 1", 82, 4, ">i", 0))
Print_Params.append(Print_Param("Unknown Int 2", 86, 4, ">i", 0))
Print_Params.append(Print_Param("Unknown Int 3", 90, 4, ">i", 0))
Print_Params.append(Print_Param("Unknown Int 4", 94, 4, ">i", 0))

try:
    print('File Length :\t', len(data))
    for param in Print_Params:
        param.decoded_value = struct.unpack(
            param.data_type, data[param.byte_index:param.byte_index+param.length])[0]
        print(param.paramater_name, "\t", param.decoded_value)
except:
    print("Something failed while parsing file")
    exit()

b = tk.Label(root, text="File Name", width=25,
             anchor="e", borderwidth=2, relief="groove")
b.grid(row=2, column=1)
b = tk.Label(root, text=file_path.name, width=25,
             anchor="w", borderwidth=2, relief="groove")
b.grid(row=2, column=2)

for i in range(len(Print_Params)):  # Column 1
    b = tk.Label(
        root, text=Print_Params[i].paramater_name, width=25, anchor="e", borderwidth=2, relief="groove")
    b.grid(row=i+3, column=1)
for i in range(len(Print_Params)):  # Column 1
    b = tk.Label(
        root, text=Print_Params[i].decoded_value, width=25, anchor="w", borderwidth=2, relief="groove")
    b.grid(row=i+3, column=2)


root.mainloop()
