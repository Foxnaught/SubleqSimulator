

dataPointer = 0
memPointer = 0
def parseSource(RAM):
	global dataPointer
	global memPointer
	f = open("hello_world.asm", "r")
	#Where values are stored
	memPointer = 1000
	#Address in memory that instructions begin
	startPointer = 0
	#Current point in memory (RAM)
	dataPointer = 0
	#The virtual pointer points to a line in assembly
	#We will map these values to dataPointer values after interpreting them
	virtualPointer = 0
	virtualMemory = [-1]
	dataStore = {"buffer": len(RAM)-1, "buffer2": len(RAM)-2}
	labels = {}

	for line in f:
		if line.replace(" ", "").replace("\t", "").replace("\n", "") == "":
			continue

		print(line)
		virtualMemory.append(dataPointer)
		vals = line.replace("\n", "").split(" ")
		if len(vals) > 1 and vals[1] == "=":
			#Define where the variable values are in memory
			#We will replace variable names with these address values here after
			dataStore[vals[0]] = memPointer
			try:
				RAM[memPointer] = int(vals[2])
				memPointer += 1
			except:
				for i in vals[2]:
					RAM[memPointer] = ord(i)
					memPointer += 1

				RAM[memPointer] = ord("\0")
				memPointer += 1

		elif vals[0] == "LABEL":
			labels[vals[1]] = dataPointer
		elif vals[0] == "ADD":
			a1 = 0
			a2 = 0
			if vals[1] in list(dataStore.keys()):
				a1 = dataStore[vals[1]]
			else:
				#Unassigned reference
				exit()
				pass

			if vals[2] in list(dataStore.keys()):
				a2 = dataStore[vals[2]]
			else:
				#Unassigned reference
				exit()
				pass

			#Clear the buffer
			RAM[dataPointer] = dataStore["buffer"]
			RAM[dataPointer+1] = dataStore["buffer"]
			RAM[dataPointer+2] = dataPointer+3

			#BUFFER = -B
			RAM[dataPointer+3] = a2
			RAM[dataPointer+4] = dataStore["buffer"]
			RAM[dataPointer+5] = dataPointer+6

			#BUFFER = -B-A
			RAM[dataPointer+6] = a1
			RAM[dataPointer+7] = dataStore["buffer"]
			RAM[dataPointer+8] = dataPointer+9

			#B = 0
			RAM[dataPointer+9] = a2
			RAM[dataPointer+10] = a2
			RAM[dataPointer+11] = dataPointer+12

			#B = -BUFFER = B+A
			RAM[dataPointer+12] = dataStore["buffer"]
			RAM[dataPointer+13] = a2
			RAM[dataPointer+14] = -1

			dataPointer += 15

		elif vals[0] == "SUB":
			a1 = dataStore[vals[1]]
			a2 = dataStore[vals[2]]

			RAM[dataPointer] = a1
			RAM[dataPointer+1] = a2
			RAM[dataPointer+2] = dataPointer + 3
			dataPointer += 3

		elif vals[0] == "JMP":
			RAM[dataPointer] = dataStore["buffer"]
			RAM[dataPointer+1] = dataStore["buffer"]
			RAM[dataPointer+2] = vals[1]

			dataPointer += 3

		#JUMP IF LESS THAN OR EQUAL (JUMP A B C | A <= B -> C)
		elif vals[0] == "JLE":
			a1 = dataStore[vals[1]]
			a2 = dataStore[vals[2]]
			#Logical line address (line address in assembly)
			#We must convert this to a dataPointer value
			jmpAddr = vals[3]

			RAM[dataPointer] = dataStore["buffer"]
			RAM[dataPointer+1] = dataStore["buffer"]
			RAM[dataPointer+2] = dataPointer + 3

			RAM[dataPointer+3] = dataStore["buffer2"]
			RAM[dataPointer+4] = dataStore["buffer2"]
			RAM[dataPointer+5] = dataPointer + 6

			#BUFFER = -a1
			RAM[dataPointer+6] = a1
			RAM[dataPointer+7] = dataStore["buffer"]
			RAM[dataPointer+8] = dataPointer + 9

			#BUFFER2 = -a2
			RAM[dataPointer+9] = a2
			RAM[dataPointer+10] = dataStore["buffer2"]
			RAM[dataPointer+11] = dataPointer + 12

			#BUFFER2 = a1 - a2
			RAM[dataPointer+12] = dataStore["buffer"]
			RAM[dataPointer+13] = dataStore["buffer2"]
			#Virtual Addressing, jmpAddr is a string that points to a label which is mapped to a dataPointer value (physical address)
			RAM[dataPointer+14] = jmpAddr

			dataPointer += 15

		elif vals[0] == "PRINT":
			RAM[dataPointer] = dataStore["buffer"]
			RAM[dataPointer+1] = dataStore["buffer"]
			RAM[dataPointer+2] = dataPointer+3

			RAM[dataPointer+3] = dataStore[vals[1]]
			RAM[dataPointer+4] = dataStore["buffer"]
			RAM[dataPointer+5] = -3

			dataPointer += 6

		elif vals[0] == "PRINTC":
			RAM[dataPointer] = dataStore["buffer"]
			RAM[dataPointer+1] = dataStore["buffer"]
			RAM[dataPointer+2] = dataPointer+3

			RAM[dataPointer+3] = dataStore[vals[1]]
			RAM[dataPointer+4] = dataStore["buffer"]
			RAM[dataPointer+5] = -4

			dataPointer += 6

		elif vals[0] == "EXIT":
			RAM[dataPointer] = dataStore["buffer"]
			RAM[dataPointer+1] = dataStore["buffer"]
			RAM[dataPointer+2] = -1

			dataPointer += 3

	f.close()

	#Turn logical addresses into physical addresses
	for i in range(len(RAM)):
		if isinstance(RAM[i], str):
			RAM[i] = labels[RAM[i]]


def SubleqCompy():
	running = True
	ADDR = 0
	SUBO = 0
	VAL = 0
	IP = 0
	IPP1 = 1
	A = 0
	B = 0
	DIR = 0
	RWE = 0
	RRE = 0
	INC = 0
	HOLD = 0
	IPSEL = 0
	DIRSEL = 0
	JMP = 0
	HOLD = 0
	_ADDR = 0
	_SUBO = 0
	_VAL = 0
	_IP = 0
	_IPP1 = 1
	_A = 0
	_B = 0
	_DIR = 0
	_RWE = 0
	_RRE = 0
	_INC = 0
	_HOLD = 0
	_IPSEL = 0
	_DIRSEL = 0
	_JMP = 0
	_HOLD = 0

	#Our memory
	RAM = [0]*10000

	#Read the assembly and turn it into subleq code, put definitions (variable values) and instructions into memory
	parseSource(RAM)

	I = 0
	CC = 0
	#We do special functions by designating IP to be a negative value
	#We hold the starting addr of the current subleq instruction so when we encounter this special function
	#	we simply move ontot he next subleq instruction afterward
	currAddr = 0
	print("  CC,   IP, ADDR,  VAL,    A,    B,  SUBO")
	print("-----------------------------------------")
	while running:
		#print("%4.d, %4.d, %4.d, %4.d, %4.d, %4.d, %4.d" % (CC, IP, ADDR, VAL, A, B, SUBO))
		if CC == 0:
			currAddr = _IP

		IPSEL = 0
		DIRSEL = 0
		RWE = 0
		HOLD = 0
		INC = 0
		if CC == 0:
			RWE = 0
			INC = 1
			HOLD = 0
			IPSEL = 0
			DIRSEL = 0
		elif CC == 1:
			RWE = 0
			INC = 1
			HOLD = 0
			IPSEL = 0
			DIRSEL = 0
		elif CC == 2:
			RWE = 0
			INC = 0
			HOLD = 1
			IPSEL = 1
			DIRSEL = 0
		elif CC == 3:
			RWE = 0
			INC = 0
			HOLD = 1
			IPSEL = 1
			DIRSEL = 0
		elif CC == 4:
			RWE = 0
			INC = 0
			HOLD = 1
			IPSEL = 0
			DIRSEL = 0
		elif CC == 5:
			RWE = 0
			INC = 0
			HOLD = 1
			IPSEL = 1
			DIRSEL = 1
		elif CC == 6:
			RWE = 1
			INC = 0
			HOLD = 0
			IPSEL = 0
			DIRSEL = 0
		
		if DIRSEL:
			DIR = B
		else:
			DIR = VAL

		A = _VAL
		B = _A

		if IPSEL:
			ADDR = DIR
		else:
			ADDR = _IP

		if HOLD:
			IP = _IP
		else:
			if INC:
				IP = _IPP1
			else:
				if _JMP:
					IP = _VAL
				else:
					IP = _IPP1

		#IPP1 is unclocked so update immediately
		IPP1 = IP + 1

		if RWE == 1:
			RAM[_ADDR] = _SUBO

		VAL = RAM[_ADDR]

		SUBO = _VAL - _A
		if SUBO <= 0:
			JMP = 1
		else:
			JMP = 0

		#END OF INSTRUCTION
		if IP == -3 or IP == -4:
			if IP == -3:
				print(-_SUBO)
			else:
				print(chr(-_SUBO), end="")

			IP = currAddr + 3
			IPP1 = IP + 1
		if IP == -1:
			print("EXITING")
			running = False

		_ADDR = ADDR
		_SUBO = SUBO
		_VAL = VAL
		_IP = IP
		_IPP1 = IPP1
		_A = A
		_B = B
		_DIR = DIR
		_RWE = RWE
		_RRE = RRE
		_INC = INC
		_HOLD = HOLD
		_IPSEL = IPSEL
		_DIRSEL = DIRSEL
		_JMP = JMP
		_HOLD = HOLD

		CC += 1
		CC = CC % 7
		if CC == 0:
			I += 1

		

	print("Instructions: " + str(I))
	print(memPointer+dataPointer-1000)



SubleqCompy()