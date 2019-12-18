"""CPU functionality."""

import sys
import os


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0x00] * 8
        self.sp = 0xf4
        self.pc = 0x00
        self.fl = 0x00
        self.heap_height = 0
        self.arg_1 = 0xf7
        self.arg_2 = 0xf6

        self.op_map = {1: {0: {0b0000: self.ADD,
                               0b1000: self.AND,
                               0b0111: self.CMP,
                               0b0110: self.DEC,
                               0b0011: self.DIV,
                               0b0101: self.INC,
                               0b0100: self.MOD,
                               0b0010: self.MUL,
                               0b1001: self.NOT,
                               0b1010: self.OR,
                               0b1100: self.SHL,
                               0b1101: self.SHR,
                               0b0001: self.SUB,
                               0b1011: self.XOR,
                               }},
                       0: {1: {0b0000: self.CALL,
                               0b0010: self.INT,
                               0b0011: self.IRET,
                               0b0101: self.JEQ,
                               0b1010: self.JGE,
                               0b0111: self.JGT,
                               0b1001: self.JLE,
                               0b1000: self.JLT,
                               0b0100: self.JMP,
                               0b0110: self.JNE,
                               0b0001: self.RET,
                               },
                           0: {0b0001: self.HLT,
                               0b0011: self.LD,
                               0b0010: self.LDI,
                               0b0000: self.NOP,
                               0b0110: self.POP,
                               0b1000: self.PRA,
                               0b0111: self.PRN,
                               0b0101: self.PUSH,
                               0b0100: self.ST,
                               }
                           }
                       }

    def exit(self):
        sys.exit()

    def load(self):
        """Load a program into memory."""
        args = sys.argv[1:]
        if args:
            file = os.path.join(args[0])
            with open(file, 'r') as f:
                for line in f:
                    line = line.split('#')[0].strip()
                    # print('l', line)
                    if line == '':
                        continue
                    self.ram[self.heap_height] = f'{int(line, 2):08b}'
                    self.heap_height += 1
        else:
            raise ValueError('No program file provided.')

    def first(self):
        return self.ram_read(self.arg_1)

    def second(self):
        return self.ram_read(self.arg_2)

    def PRN(self):
        print(int(self.reg[int(self.first(), 2)], 2), end='\n')

    def PRA(self):
        address = int(self.reg[int(self.first(), 2)], 2)
        letter = self.ram[address]
        print(chr(int(letter, 2)), end='')

    def LDI(self):
        self.reg[int(self.first(), 2)] = self.second()

    def HLT(self):
        self.exit()

    def LD(self):
        self.reg[int(self.first(), 2)] = self.reg[int(self.second(), 2)]

    def PUSH(self):
        self.sp -= 1
        if self.sp <= self.heap_height:
            raise IndexError('Stack Overflow')
        self.ram[self.sp] = self.reg[int(self.first(), 2)]

    def POP(self):
        self.reg[int(self.first(), 2)] = self.ram[self.sp]
        self.sp += 1

    def CALL(self):
        self.sp -= 1
        self.ram[self.sp] = self.pc + 1
        self.pc = int(self.reg[int(self.first(), 2)], 2)

    def RET(self):
        self.pc = self.ram[self.sp]
        self.sp += 1

    def ST(self):
        self.reg[self.first()] = self.second()

    def INT(self):
        pass

    def IRET(self):
        pass

    def NOP(self):
        pass

    def JMP(self):
        self.pc = int(self.reg[int(self.first(), 2)], 2)

    def JEQ(self):
        if self.fl & 1:
            self.pc = int(self.reg[int(self.first(), 2)], 2)
        else:
            self.pc += 1

    def JNE(self):
        if not self.fl & 1:
            self.pc = int(self.reg[int(self.first(), 2)], 2)
        else:
            self.pc += 1

    def JGT(self):
        if self.fl & (1 << 1):
            self.pc = int(self.reg[int(self.first(), 2)], 2)
        else:
            self.pc += 1

    def JGE(self):
        if self.fl & 1 or self.fl & (1 << 1):
            self.pc = int(self.reg[int(self.first(), 2)], 2)
        else:
            self.pc += 1

    def JLT(self):
        if self.fl & (1 << 2):
            self.pc = int(self.reg[int(self.first(), 2)], 2)
        else:
            self.pc += 1

    def JLE(self):
        if self.fl & 1 or self.fl & (1 << 2):
            self.pc = int(self.reg[int(self.first(), 2)], 2)
        else:
            self.pc += 1

    def DEC(self):
        deced = (int(self.reg[int(self.first(), 2)], 2) - 1) & 0xff
        self.reg[int(self.first(), 2)] = f'{deced:08b}'

    def INC(self):
        inced = (int(self.reg[int(self.first(), 2)], 2) + 1) & 0xff
        self.reg[int(self.first(), 2)] = f'{inced:08b}'

    def ADD(self):
        added = (int(self.reg[int(self.first(), 2)], 2) + int(self.reg[int(self.second(), 2)], 2)) & 0xff
        self.reg[int(self.first(), 2)] = f'{added:08b}'

    def SUB(self):
        subbed = (int(self.reg[int(self.first(), 2)], 2) - int(self.reg[int(self.second(), 2)], 2)) * 0xff
        self.reg[int(self.first(), 2)] = f'{subbed:08b}'

    def MUL(self):
        mulled = (int(self.reg[int(self.first(), 2)], 2) * int(self.reg[int(self.second(), 2)], 2)) & 0xff
        self.reg[int(self.first(), 2)] = f'{mulled:08b}'

    def DIV(self):
        dived = (int(self.reg[int(self.first(), 2)], 2) >> int(self.reg[int(self.second(), 2)], 2)) & 0xff
        self.reg[int(self.first(), 2)] = f'{dived:08b}'

    def MOD(self):
        modded = (int(self.reg[int(self.first(), 2)], 2) % int(self.reg[int(self.second(), 2)], 2)) & 0xff
        self.reg[int(self.first(), 2)] = f'{modded:08b}'

    def CMP(self):
        comp_a, comp_b = int(self.reg[int(self.first(), 2)], 2), int(self.reg[int(self.second(), 2)], 2)
        if comp_a == comp_b:
            self.fl = self.fl & 0b00000001
            self.fl = self.fl | 0b00000001
        if comp_a > comp_b:
            self.fl = self.fl & 0b00000010
            self.fl = self.fl | 0b00000010
        if comp_a < comp_b:
            self.fl = self.fl & 0b00000100
            self.fl = self.fl | 0b00000100

    def AND(self):
        anded = (int(self.reg[int(self.first(), 2)], 2) & int(self.reg[int(self.second(), 2)], 2)) & 0xff
        self.reg[int(self.first(), 2)] = f'{anded:08b}'

    def OR(self):
        ored = (int(self.reg[int(self.first(), 2)], 2) | int(self.reg[int(self.second(), 2)], 2)) & 0xff
        self.reg[int(self.first(), 2)] = f'{ored:08b}'

    def XOR(self):
        xored = (int(self.reg[int(self.first(), 2)], 2) ^ int(self.reg[int(self.second(), 2)], 2)) & 0xff
        self.reg[int(self.first(), 2)] = f'{xored:08b}'

    def NOT(self):
        noted = int(~int(self.reg[int(self.first(), 2)], 2), 2) & 0xff
        self.reg[int(self.first(), 2)] = f'{noted:08b}'

    def SHL(self):
        shled = (int(self.reg[int(self.first(), 2)], 2) << int(self.reg[int(self.second(), 2)], 2)) & 0xff
        self.reg[int(self.first(), 2)] = f'{shled:08b}'

    def SHR(self):
        shred = (int(self.reg[int(self.first(), 2)], 2) << int(self.reg[int(self.second(), 2)], 2)) & 0xff
        self.reg[int(self.first(), 2)] = f'{shred:08b}'

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: pc: {self.pc}, fl: {self.fl}, "
              # f"ir: {self.ir}, "
              f"ram: {self.ram_read(self.pc)}, "
              f"ram +: {self.ram_read(self.pc + 1)}, ram ++: {self.ram_read(self.pc + 2)},", end='')

        print('\nRegisters: ')
        for i in range(8):
            print(f"{self.reg[i]}", end=', ')
        print('\n\n')

    def ram_read(self, address):
        """Get the value stored in ram at address."""
        return self.ram[address]

    def ram_write(self, address, value):
        """Set the ram address to value."""
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        while True:
            ir = int(self.ram_read(self.pc), 2)
            _bytes = ir >> 6
            _alu = ir & 0b00100000
            alu = _alu >> 5
            _adv_pc = ir & 0b00010000
            adv_pc = _adv_pc >> 4
            instruction = ir & 0b00001111
            args = 0xf7

            for _ in range(_bytes):
                self.pc += 1
                self.ram_write(args, self.ram_read(self.pc))
                args -= 1

            if not adv_pc:
                self.pc += 1

            # print('b', _bytes, 'a', alu,
            #       'ad', adv_pc, 'ins', bin(ir))
            # self.trace()

            self.op_map[alu][adv_pc][instruction]()
