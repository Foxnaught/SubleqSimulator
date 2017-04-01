



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

	RAM = [0]*10000
	RAM[1000] = 1111111
	RAM[1001] = 9876543
	RAM[1002] = 1
	RAM[1003] = 0
	RAM[1004] = 0
	
	RAM[0] = 1003
	RAM[1] = 1000
	RAM[2] = 12

	RAM[3] = 1002
	RAM[4] = 1000
	RAM[5] = 9

	RAM[6] = 1001
	RAM[7] = 1004
	RAM[8] = 3

	RAM[9] = 1001
	RAM[10] = 1004
	RAM[11] = 12

	RAM[12] = 1001
	RAM[13] = 1003
	RAM[14] = -1

	I = 0
	CC = 0
	print("  CC,   IP, ADDR,  VAL,    A,    B")
	while running:
		#print("%4s, %4s, %4s, %4s, %4s, %4s" % (CC, IP, ADDR, VAL, A, B))

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

		if IP == -1:
			running = False

	print("Instructions: " + str(I))
	print("RAM: " + str(RAM[1004]))

SubleqCompy()