# SubleqSimulator
A software implementation of a subleq CPU

Running SubleqCompy.py will cause the pseudo-code in hello_world.asm to be interpreted and run into the subleq simulator.
The subleq simulator implementation has special hardware interrupts when certain addresses are targetted. Currently special addresses (interrupts) are negative.

LEGEND:
A = the address to a value which points to another address in memory
(A) = the value where the pointer address points to.

COMMANDS:

LABEL A   | creates a virtual address named A which can be used in jump destinations

A = B     | address A has the same pointing value as address B

ADD A B   | (A) is added to (B) and the value is stored at address B

SUB A B   | (A) is substracted from (B) and the value is stored at address B

JMP A     | Jump to the instruction below LABEL A

JLE A B C | Jump to address C if (A) is less than or equal to (B)

PRINT A   | Prints the integer at address A. (Doesn't currently work for negative numbers) Uses interrupt -3

PRINTC A  | Prints the char at address A. Interprets address A as an ascii character. Uses interrupt -4

EXIT      | Exits the program. Uses interrupt -1.
