import sys
import os
import time

def is_valid_register(string):
	valid=False
	if string[0]=="d" or string[0]=="a":
		register=string[1]
		if register.isdigit():
			register=int(register)
			if register>=0 and register<=9:
				valid=True
	return valid

def get_register_value(string):
	global data_registers
	global address_registers
	value=0
	if is_valid_register(string):
		if string[0]=="d":
			value=data_registers[int(string[1])]
		else:
			value=address_registers[int(string[1])]
	return value

def set_register_value(string,value):
	global data_registers
	global address_registers
	global bits
	if is_valid_register(string):
		if string[0]=="d":
			data_registers[int(string[1])]=value & bits
		else:
			address_registers[int(string[1])]=value & bits

def get_arg_value(string,register):
	value=0
	if string[0]=="#":
		if string[1:].isdigit():
			value=int(string[1:])
	elif string[0]=="$":
		try:
			value=int(string[1:],16)
		except:
			pass
	elif string[0]=="%":
		try:
			value=int(string[1:],2)
		except:
			pass
	elif is_valid_register(string) and register:
		value=get_register_value(string)
	return value

if len(sys.argv)>1:
	file_name=sys.argv[1]
	if os.path.exists(file_name):
		num_registers=8
		data_registers=[0]*num_registers
		address_registers=[0]*num_registers
		jump_line=0
		jump_loops=0
		jump_loops_max=2000
		line_number=0

		labels={}

		video_memory_address=1000
		video_width=40
		video_height=20
		video_memory_size=video_width*video_height
		memory=[0]*(video_memory_address+video_memory_size)

		bits=16
		bits=(2**bits)-1

		with open(file_name,"r") as file:
			program=file.readlines()
		for a in range(0,len(program)):
			program[a]=program[a].strip("\t")
			program[a]=program[a].strip("\n")
			program[a]=program[a].replace("video_width",str(video_width))
			program[a]=program[a].replace("video_height",str(video_height))
			program[a]=program[a].replace("video_offset",str(video_memory_address))
			if ";" in program[a]:
				program[a]=program[a][:program[a].index(";")]
		program=list(filter(None,program))

		print("Memory size: " + str(len(memory)) + " bytes")
		print()

		cmp_equal=False
		cmp_greater=False
		cmp_lower=False

		for counter,line in enumerate(program):
			if line[-1]==":":
				labels.update({line[:-1]:counter})

		start_time=time.perf_counter()

		while line_number<len(program) and line_number>=0:
			line=program[line_number]
			command=line.split(" ")[0].lower()
			if len(line.split(" "))>1:
				args=line.split(" ")[1].lower().split(",")
				value=0
				if len(args)==2:
					if command=="mov":
						set_register_value(args[1],get_arg_value(args[0],True))
					elif command=="add":
						set_register_value(args[1],get_arg_value(args[1],True)+get_arg_value(args[0],True))
					elif command=="sub":
						set_register_value(args[1],get_arg_value(args[1],True)-get_arg_value(args[0],True))
					elif command=="mul":
						set_register_value(args[1],get_arg_value(args[1],True)*get_arg_value(args[0],True))
					elif command=="div":
						set_register_value(args[1],get_arg_value(args[1],True)//get_arg_value(args[0],True))
					elif command=="shr":
						set_register_value(args[1],get_arg_value(args[1],True)>>get_arg_value(args[0],False))
					elif command=="shl":
						set_register_value(args[1],get_arg_value(args[1],True)<<get_arg_value(args[0],False))
					elif command=="or":
						set_register_value(args[1],get_arg_value(args[1],True) | get_arg_value(args[0],True))
					elif command=="xor":
						set_register_value(args[1],get_arg_value(args[1],True) ^ get_arg_value(args[0],True))
					elif command=="and":
						set_register_value(args[1],get_arg_value(args[1],True) & get_arg_value(args[0],True))
					elif command=="cmp":
						if get_arg_value(args[0],True)>get_arg_value(args[1],True):
							cmp_greater=True
						elif get_arg_value(args[0],True)<get_arg_value(args[1],True):
							cmp_lower=True
						elif get_arg_value(args[0],True)>=get_arg_value(args[1],True):
							cmp_greater=True
							cmp_equal=True
						elif get_arg_value(args[0],True)>=get_arg_value(args[1],True):
							cmp_lower=True
							cmp_equal=True
					elif command=="sto":
						if args[1][0]=="a":
							if get_register_value(args[1])<len(memory):
								memory[get_register_value(args[1])]=get_arg_value(args[0],False)
							else:
								print("Memory address out of range!")
								line_number=-1
					elif command=="get":
						if args[0][0]=="a":
							if get_register_value(args[1])<len(memory):
								set_register_value(args[1],memory[get_register_value(args[0])])
							else:
								print("Memory address out of range!")
								line_number=-1
					else:
						print("Invalid instruction on line " + str(line_number+1) + ": " + command)
				elif len(args)==1:
					if command=="not":
						set_register_value(args[0],~get_arg_value(args[0],True))
					elif command=="clr":
						set_register_value(args[0],0)
					elif command=="jmp" or command=="jle" or command=="jge" or command=="jl" or command=="jg" or command=="je" or command=="jne":
						if args[0] in labels:
							condition=True
							if command=="jle":
								condition=cmp_lower or cmp_equal
							elif command=="jge":
								condition=cmp_greater or cmp_equal
							elif command=="jl":
								condition=cmp_lower
							elif command=="jg":
								condition=cmp_greater
							elif command=="je":
								condition=cmp_equal
							elif command=="jne":
								condition=not cmp_equal
							if condition:
								line_number=labels[args[0]]
								if jump_line==line_number:
									jump_loops+=1
								else:
									jump_loops=0
								jump_line=line_number

							cmp_equal=False
							cmp_greater=False
							cmp_lower=False
						else:
							print("Error: Label \"" + args[0] + "\" doesn't exist")
					else:
						print("Error: Invalid instruction \"" + command + "\" on line " + str(line_number+1))
				else:
					print("Error: Invalid instruction \"" + command + "\" on line " + str(line_number+1))
			else:
				if line[-1]!=":":
					print("Error: Invalid instruction \"" + command + "\" on line " + str(line_number+1))
			line_number+=1
			if jump_loops>jump_loops_max:
				line_number=-1
				print("HALTED! Infinite loop")

		print("Contents of registers:")
		for a in range(0,num_registers):
			print("d" + str(a) + ": " + str(data_registers[a]).ljust(5) + "\ta" + str(a) + ": " + str(address_registers[a]))

		print()
		print("Video memory:")
		for a in range(0,video_memory_size):
			if memory[video_memory_address+a]:
				print(chr(9608),end="")
			else:
				print(" ",end="")
			if a%video_width==video_width-1:
				print()

		end_time=time.perf_counter()

		print()
		print("Executed in " + str(end_time-start_time) + " seconds")
	else:
		print("Invalid path!")
else:
	print("No file specified!")