# NAL-Editor
An editor with built in compiler for a custom assembly language named "Nano Assembly Language" or in short NAL.
NAL is mainly based on a custom MPU which has been build using Logisim-Evolution.
The MPU Logisim circuit file "MPU.circ" along with ControlLogic is present in "NAL MPU Logisim" Folder.

# "installation" Folder
This folder contains "nal_editorv1.0.exe" file which can install NAL Editor in Windows machine.
The "nal_editorv1.0.iss" is an Inno Setup Script file used to create the installation package.

# "res" Folder
Contains 3 files:
1. "doc.enc" file - a simple text file containing the Documentation of the Opcodes of the MPU
2. "nal.ico" file - an icon file used for the project. 
3. "nal_opcodes.json" file - a JSON file which contains the hex Opcodes and corresponding Assembly Codes.
All the 3 files are required to start the app. Otherwise it'll crash.

# "nal_compiler.py" File
A Python file which contains important codes for compiling the Assembly Codes to the hex Opcodes.

# "nal_editor.py" File
A Python file which is the heart of the Editor.
Tkinter python module has been used for the GUI.

# Building the .exe File
Pyinstaller module has been used to convert the "nal_editor.py" to "nal_editor.exe" file.

# Tutorial
The best way to install the Editor is simply by the "nal_editorv1.0.exe" file.
Run the executable file and it will run the Editor.
The NAL Editor is a simple text editor where the assembly codes can be typed and saved.
The codes are saved as ".nal" file.
The Documentation can be viewed from "Commands>Opcodes"
Saved "<filename>.nal" file can be compiled using "Commands>Compile"
Max allowed instructions is 256.
Compiled files are saved as "<filename>.nac" files in compiled directory in app installation folder.
Install Logisim-Evolution, load the "MPU.circ" file from "Nano MPU Logisim" folder.
Load the ".nac" file in the ROM module inside MPU circuit and start the simulaton.
Turn On the PROG pin and DBG pin and wait for the program to load in MPU.
Turn Off the PROG pin and DBG pin, the computation will start.
