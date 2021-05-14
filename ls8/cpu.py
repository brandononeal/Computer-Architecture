"""CPU functionality."""

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.ram = [0] * 256
        self.reg = [0] * 8
        self.sp = 7
        self.pc = 0

    def ram_read(self, ram_address):
        return self.ram[ram_address]

    def ram_write(self, ram_address, ram_value):
        self.ram[ram_address] = ram_value

    def load(self, filename):
        """Load a program into memory."""

        with open(filename) as filedata:
            address = 0

            for line in filedata:
                data = line.split('#')[0].strip()

                if data == '':
                    continue

                num = int(data, 2)
                self.ram_write(address, num)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            # FL 00000LGE
            if self.reg[reg_a] == self.reg[reg_b]:
                # Set to 00000001
                pass
            elif self.reg[reg_a] > self.reg[reg_b]:
                # Set to 00000010
                pass
            elif self.reg[reg_a] < self.reg[reg_b]:
                # Set to 00000100
                pass
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.ADD = 0b10100000
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001

        self.CMP = 0b10100111

        self.JMP = 0b01010100
        self.JEQ = 0b01010101
        self.JNE = 0b01010110

        running = True

        while running:
            inst = self.ram[self.pc]

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if inst == self.HLT:
                running = False
            elif inst == self.LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif inst == self.PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif inst == self.ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3
            elif inst == self.MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            elif inst == self.PUSH:
                self.reg[self.sp] -= 1
                value = self.reg[operand_a]
                self.ram_write(self.reg[self.sp], value)
                self.pc += 2
            elif inst == self.POP:
                value = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1
                self.reg[operand_a] = value
                self.pc += 2
            elif inst == self.CALL:
                self.reg[self.sp] -= 1
                self.ram_write(self.reg[self.sp], self.pc + 2)
                self.pc = self.reg[operand_a]
            elif inst == self.RET:
                self.pc = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1
            elif inst == self.CMP:
                self.alu('CMP', operand_a, operand_b)
                self.pc += 3
            elif inst == self.JMP:
                pass
            elif inst == self.JEQ:
                pass
            elif inst == self.JNE:
                pass
