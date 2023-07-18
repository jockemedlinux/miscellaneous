def get_opcode(instruction):
    opcode = ""
    parts = instruction.split()
    mnemonic = parts[0]

    if mnemonic == "jmp" and len(parts) == 2:
        operand = parts[1]

        if operand == "esp":
            opcode = "0xFF 0xE4"

    return opcode

instruction = input("Enter an instruction: ")
opcode = get_opcode(instruction)
print("Opcode:", opcode)