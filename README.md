# SubleqSimulator
A software implementation of a subleq CPU

Running SubleqCompy.py will cause the pseudo-code in hello_world.asm to be interpreted and run into the subleq simulator.
The subleq simulator implementation has special hardware interrupts when certain addresses are targetted. Currently special addresses (interrupts) are negative.

COMMANDS:
LABEL A   | creates a virtual address named A which can be used in jump destinations
A = B     | A becomes the address where the value B is stored
ADD A B   | A is subtracted from B and the value is stored in B
SUB A B   | A is the substracted from B and the value is stored in B
JMP A     | Jump the to the instruction below LABEL A
JLE A B C | Jump to address C if A is less than or equal to B
PRINT A   | Prints the integer at address A. Uses interrupt -3
PRINTC A  | Prints the char at address A. Interprets address A as an ascii character. Uses interrupt -4
EXIT      | Exits the program. Uses interrupt -1.
