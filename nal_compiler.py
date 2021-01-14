import json
import os

class NALCompiler:
	
	opcodes = None
	error = "FDF"

	def __init__(self, opcodes_file):
		self.opcodes_file = opcodes_file
		
		if os.path.exists(opcodes_file):
			file = open(opcodes_file, 'r')
			opcodes_json = file.read()
			file.close()
		else:
			raise Exception()	

		NALCompiler.opcodes = json.loads(opcodes_json)
		
			
	def read(self, nal_file):
		
		nalFile = open(nal_file, 'r')
		str = nalFile.read()
		nalFile.close()
		
		raw_code = str.strip()
		
		if len(raw_code.split()) > 256:
			raise Exception()
			
		return raw_code
			
	def compile(self, codes_str, opcodes_dict, nac_file):
		
		instructions = codes_str.split("\n")
				
		output_str = "v2.0 raw\n"
		col = 0
		
		for i in instructions:
			ins = i.split(" ")
			comm = ins[0]
			
			if comm in opcodes_dict:
				output_str += opcodes_dict[comm]
				col += 1
				if col == 8:
					output_str += "\n"
					col = 0
				else:
					output_str += " "
			else:
				NALCompiler.error = comm
				raise Exception()
		
			if len(ins) == 2:
				arg = ins[1]
				output_str += arg
				col += 1
				if col == 8:
					output_str += "\n"
					col = 0
				else:
					output_str += " "

		f = open(nac_file, 'w')
		f.write(output_str)
		f.close()