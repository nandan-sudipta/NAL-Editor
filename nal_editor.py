import os
import sys
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.font import Font
from nal_compiler import NALCompiler

class NALEditor:
	# set up the root widget
	__root = Tk()
	__thisWidth = 500
	__thisHeight = 700
	__thisTextArea = Text(__root)
	__thisMenuBar = Menu(__root)
	__thisFileMenu = Menu(__thisMenuBar, tearoff = 0)
	__thisEditMenu = Menu(__thisMenuBar, tearoff = 0)
	__thisHelpMenu = Menu(__thisMenuBar, tearoff = 0)
	__thisCommandMenu = Menu(__thisMenuBar, tearoff = 0)
	
	# to add scroll bar
	__thisScrollBar = Scrollbar(__thisTextArea)
	__file = None
	
	compiler = None
	
	docu = None
	
	def __init__(self, **kwargs):
		
		if os.path.exists("./compiled"):
			pass
		else:
			os.mkdir("./compiled")
			
		if os.path.exists("./res/doc.enc"):
			d = open("./res/doc.enc", 'r')
			NALEditor.docu = d.read().strip()
			d.close()
		else:
			showinfo("Fatal Error", "File '%s' Is Missing From Installation Folder" % "doc.enc")
			exit()
			
		try:
			NALEditor.compiler = NALCompiler("./res/nal_opcodes.json")
		except:
			showinfo("Fatal Error", "File '%s' Is Missing From Installation Folder" % "nal_opcodes.json")
			exit()
			
		#icon
		try:
			self.__root.wm_iconbitmap("./res/nal.ico")
		except:
			pass
			
		# set window size as mentioned above
		try:
			self.__thisWidth = kwargs['width']
		except KeyError:
			pass
		try:
			self.__thisHeight = kwargs['height']
		except KeyError:
			pass
		
		# center the window
		screenWidth = self.__root.winfo_screenwidth()
		screenHeight = self.__root.winfo_screenheight()
		
		# for left-allign
		left = (screenWidth / 2) - (self.__thisWidth / 2)
		
		# for right-allign
		top = (screenHeight / 2) - (self.__thisHeight / 2)
		
		
		# for top and bottom
		self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))
		
		# to make the text area auto resizeable
		self.__root.grid_rowconfigure(0, weight = 1)
		self.__root.grid_columnconfigure(0, weight = 1)
		
		# add controls (widget)
		self.__thisTextArea.grid(sticky = N + E + S + W)
		
		# to open new file
		self.__thisFileMenu.add_command(label = "New", command = self.__newFile)
		
		# to open existing file
		self.__thisFileMenu.add_command(label = "Open", command = self.__openFile)
		
		# to save current file
		self.__thisFileMenu.add_command(label = "Save", command = self.__saveFile)
		
		# to create a line in the dialog
		self.__thisFileMenu.add_separator()
		
		# to exit the application
		self.__thisFileMenu.add_command(label = "Exit", command = self.__quitApplication)
		
		self.__thisMenuBar.add_cascade(label = "File", menu = self.__thisFileMenu)
		
		# to give feature of cut copy paste and editting
		self.__thisEditMenu.add_command(label = "Cut", command = self.__cut)
		self.__thisEditMenu.add_command(label = "Copy", command = self.__copy)
		self.__thisEditMenu.add_command(label = "Paste", command = self.__paste)
		self.__thisMenuBar.add_cascade(label = "Edit", menu = self.__thisEditMenu)
		
		# to create feature of description of NAL Editor and compiler
		self.__thisHelpMenu.add_command(label = "About NAL Editor", command = self.__showAbout)
		self.__thisCommandMenu.add_command(label = "Opcodes", command = self.__showOpcodes)
		self.__thisCommandMenu.add_command(label = "Compile", command = self.__runCompiler)
		self.__thisMenuBar.add_cascade(label = "Commands", menu = self.__thisCommandMenu)
		self.__thisMenuBar.add_cascade(label = "Help", menu = self.__thisHelpMenu)
		
		self.__root.config(menu = self.__thisMenuBar)
		
		self.__thisScrollBar.pack(side = RIGHT, fill = Y)
		
		# scrollbar will adjust automatically according to content
		self.__thisScrollBar.config(command = self.__thisTextArea.yview)
		self.__thisTextArea.config(yscrollcommand = self.__thisScrollBar.set)
		
		# if argument is passed open file otherwise open new file
		if len(sys.argv) == 2:
			self.__file = sys.argv[1]
			self.__root.title(os.path.basename(self.__file) + " - NAL Editor")
			f = open(self.__file, 'r')
			self.__thisTextArea.insert(1.0, f.read())
			f.close()
		else:
			self.__root.title("Untitled - Nano Editor")
		
	def __quitApplication(self):
		self.__root.destroy()
	
	def __showAbout(self):
		showinfo("About NAL Editor", "Text Editor For Nano Assembly Language")
		
	def __showOpcodes(self):
		
		top = Toplevel(self.__root)
		try:
			top.wm_iconbitmap("./res/nal.ico")
		except:
			pass
			
		top.title("Opcodes Documentation")
		top.geometry("600x850")
		font = Font(family = "Consolas", size = "8")
		txt = StringVar()
		msg = Message(top, textvariable = txt, font = font)
		txt.set(NALEditor.docu.strip())
		msg.pack()
		
	def __openFile(self):
		self.__file = askopenfilename(defaultextension = ".nal", filetypes = [("Nano Files", "*.nal*"), ("All Files", "*.*")])
		if self.__file == "":
			self.__file = None
		else:
			# try to open the file
			# set window title
			self.__root.title(os.path.basename(self.__file) + " - NAL Editor")
			self.__thisTextArea.delete(1.0, END)
			file = open(self.__file, 'r')
			self.__thisTextArea.insert(1.0, file.read())
			file.close()
			
	def __newFile(self):
		self.__root.title("Untitled NAL Editor")
		self.__file = None
		self.__thisTextArea.delete(1.0, END)
		
	def __saveFile(self):
		if self.__file == None:
			# save as new file
			self.__file = asksaveasfilename(initialfile = "Untitled.nal", defaultextension = ".nal", filetypes = [("Nano Files", "*.nal*"), ("All Files", "*.*")])
		if self.__file == "":
			self.__file = None
		else:
			# try to save the file
			file = open(self.__file, "w")
			file.write(self.__thisTextArea.get(1.0, END).strip())
			file.close()
			
			# change window title
			self.__root.title(os.path.basename(self.__file) + " - NAL Editor")
	
	def __cut(self):
		self.__thisTextArea.event_generate("<<Cut>>")
		
	def __copy(self):
		self.__thisTextArea.event_generate("<<Copy>>")
	
	def __paste(self):
		self.__thisTextArea.event_generate("<<Paste>>")
		
	def __runCompiler(self):
		if self.__file == None:
			# save as new file
			self.__file = asksaveasfilename(initialfile = "Untitled.nal", defaultextension = ".nan", filetypes = [("All Files", "*.*"), ("Nano Files", "*.nal*")])
		if self.__file == "":
			self.__file = None
			raise Exception("Error: File Not Saved")
		else:
			# try to save the file
			file = open(self.__file, "w")
			file.write(self.__thisTextArea.get(1.0, END))
			file.close()
			
			# change window title
			self.__root.title(os.path.basename(self.__file) + " - NAL Editor")
			
			# define the nac_file
			f = (os.path.basename(self.__file))
			nac_file = "./compiled/" + f[0 : f.rfind(".")] + ".nac"
			
		codes = None
			
		try:
			codes = NALEditor.compiler.read(self.__file)
		except:
			showinfo("Compiler Error", "Max No. Of Instructions Allowed Exceeded\nCan't Compile More Than 256 Instructions")
			raise Exception("Error: Compilation Failed")

		if codes == "":
			showinfo("Compiler Error", "No Instructions Found")
			raise Exception("Error: Compilation Failed")
			
		try:
			NALEditor.compiler.compile(codes, NALEditor.compiler.opcodes, nac_file)
		except:
			showinfo("Compiler Error", "Unrecognized Instruction -> %s" % NALEditor.compiler.error)
			raise Exception("Error: Compilation Failed")
		
	def run(self):
		
		# run main application
		self.__root.mainloop()

# run main application
notepad = NALEditor(width = 300, height = 400)
notepad.run()