# miniasm
Tiny, slightly functional assembly-type language written in Python. It's like its own little computer written in Python! It has 8 data registers and 8 address registers (of adjustable word length), and uses its own language very similar to assembly. It supports immediate values, registers, line labels and comments. It even has its own little chunk of graphics memory! It's interpretive and reads from a text file, but one day, I may implement opcode-based programs for tiny files.

## "Instruction set"
An immediate value can be either decimal, binary or hex (for example, #200 for a decimal value, $1f for hex, %11001010 for binary)

### Registers/Values
- **mov r1/i1,r2/i2** - Moves a value from r1/i1 into r2/i2. The value remains in r1/i1.
- **add r1/i1,r2/i2** - Adds the value of r1/i1 to r2/i2.
- **sub r1/i1,r2/i2** - Subtracts the value of r1/i1 from r2/i2.
- **mul r1/i1,r2/i2** - Multiplies r2/i2 by r1/i1.
- **div r1/i1,r2/i2** - Divides r2/i2 by r1/i1.
- **shr i,r** - Shifts register r to the right by i bytes.
- **shl i,r** - Shifts register r to the left by i bytes.
- **or r1/i1,r2/i2** - Performs a bitwise "or" with r2/i2.
- **xor r1/i1,r2/i2** - Performs a bitwise "xor" with r2/i2.
- **and r1/i1,r2/i2** - Performs a bitwise "and" with r2/i2.
- **not r** - Performs a bitwise "not" on register r.
- **clr r** - Resets the value of register r.
- **cmp r1/i1,r2/i2** - Compares r1/i1 to r2/i2, and sets a bunch of flags for use with the jump instructions.
- **sto r1/i1,r2** - Stores a value into the memory offset of address register r2.
- **get r1,r2** - Gets a value from the memory offset of address register r1, and stores it in r2.

### Flow
- **jmp label** - Unconditionally jumps to a line label.
- **jg label** - Jumps to a label if r1/i1 is greater than r2/i2.
- **jl label** - Jumps to a label if r1/i1 is less than r2/i2.
- **jge label** - Jumps to a label if r1/i1 is greater than or equal to r2/i2.
- **jle label** - Jumps to a label if r1/i1 is less than or equal to r2/i2.
- **je label** - Jumps to a label if r1/i1 is equal to r2/i2.
- **jne label** - Jumps to a label if r1/i1 isn't equal to r2/i2.
- **je label** - Jumps to a label if r1/i1 is equal to r2/i2.
- **jne label** - Jumps to a label if r1/i1 isn't equal to r2/i2.