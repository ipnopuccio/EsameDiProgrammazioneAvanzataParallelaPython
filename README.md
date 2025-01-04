# Little Man Computer (LMC) Simulator

This project implements a simulator for the Little Man Computer (LMC), an educational computer model used to teach the basics of assembly programming and computer architecture.

## Overview

The implementation consists of two main classes:
- `LMC`: The main computer simulator that executes the machine code
- `Assembler`: A tool that converts assembly code into machine code for the LMC

## Features

- 100 memory locations (numbered 0-99)
- Basic instruction set including arithmetic, branching, and I/O operations
- Support for labels in assembly code
- Input and output queues for program I/O
- Error handling for illegal instructions and memory overflow

## Usage

### Basic Example

```python
from lmc import Assembler, LMC

# Write your assembly program
program = """
INP
STA 50    // Store first number in memory location 50
INP
ADD 50    // Add the number from memory location 50
OUT       // Output the result
HLT       // Stop the program
"""

# Create an assembler and convert the program to machine code
assembler = Assembler()
machine_code = assembler.assemble(program)

# Create an LMC instance and load the program
lmc = LMC()
lmc.load_program(machine_code)

# Set input values
lmc.set_input([5, 3])

# Run the program and get the output
result = lmc.run()
print("Output:", result)  # Will print: Output: [8]
```

## Instruction Set

### Machine Code Format
- Instructions are 3-digit numbers
- First digit is the operation code (opcode)
- Last two digits are the operand (memory address)

### Available Instructions

| Assembly | Machine Code | Description |
|----------|-------------|-------------|
| ADD xx   | 1xx        | Add value from memory location xx to accumulator |
| SUB xx   | 2xx        | Subtract value from memory location xx from accumulator |
| STA xx   | 3xx        | Store accumulator value to memory location xx |
| LDA xx   | 5xx        | Load value from memory location xx into accumulator |
| BRA xx   | 6xx        | Branch (jump) to memory location xx |
| BRZ xx   | 7xx        | Branch to xx if accumulator is zero |
| BRP xx   | 8xx        | Branch to xx if previous operation was positive |
| INP      | 901        | Input a value into the accumulator |
| OUT      | 902        | Output the accumulator value |
| HLT      | 000        | Halt the program |

## Program Limitations

- Memory is limited to 100 locations (0-99)
- Values must be between 0 and 999
- Input values must be non-negative integers
- Programs cannot exceed 100 instructions

## Error Handling

The simulator includes several error checks:
- Program size exceeding memory limit
- Invalid input values (must be 0-999)
- Illegal instructions (400-499)
- Empty input queue when INP instruction is executed
- Invalid assembly syntax

## Comments

Assembly code can include comments using the `//` syntax:
```python
INP       // Read first number
STA 50    // Store it in memory
```

## Example Programs

### Adding Two Numbers
```python
INP       // Get first number
STA 50    // Store in memory location 50
INP       // Get second number
ADD 50    // Add number from memory
OUT       // Display result
HLT       // Stop program
```

### Counting Down
```python
INP       // Get starting number
loop OUT  // Display current number
    SUB 1 // Subtract 1
    BRP loop // If result is positive, continue loop
HLT       // Stop when done
```
