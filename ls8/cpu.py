"""CPU functionality."""

import sys
import os


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0x00] * 8
        self.reg[7] = self.ram[int('0xf4', 16)]
        self.sc = self.reg[7]
        self.pc = 0x00
        self.ir = 0x00
        self.mar = 0x00
        self.mdr = 0x00
        self.fl = 0x00
        self.op_map = {1: {0: {0b0000: 'ADD',
                               0b1000: 'AND',
                               0b0111: 'CMP',
                               0b0110: 'DEC',
                               0b0011: 'DEV',
                               0b0101: 'INC',
                               0b0100: 'MOD',
                               0b0010: 'MUL',
                               0b1001: 'NOT',
                               0b1010: 'OR',
                               0b1100: 'SHL',
                               0b1101: 'SHR',
                               0b0001: 'SUB',
                               0b1011: 'XOR',
                               }},
                       0: {1: {0b0000: 'CALL',
                               0b0010: 'INT',
                               0b0011: 'IRET',
                               0b0101: 'JEQ',
                               0b1010: 'JGE',
                               0b0111: 'JGT',
                               0b1001: 'JLE',
                               0b1000: 'JLT',
                               0b0100: 'JMP',
                               0b0110: 'JNE',
                               0b0001: 'RET',
                               },
                           0: {0b0001: 'HLT',
                               0b0011: 'LD',
                               0b0010: 'LDI',
                               0b0000: 'NOP',
                               0b0110: 'POP',
                               0b1000: 'PRA',
                               0b0111: 'PRN',
                               0b0101: 'PUSH',
                               0b0100: 'ST',
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
                i = 0
                for line in f:
                    line = line.split('#')[0].strip()
                    # print('l', line)
                    if line == '':
                        continue
                    self.ram[i] = f'{int(line, 2):08b}'
                    i += 1
        else:
            raise ValueError('No program file provided.')

    def not_alu(self, op, *args):
        """Not ALU operations."""
        if len(args) > 1:
            arg_1, arg_2 = int(args[0], 2), int(args[1], 2)
        elif len(args):
            arg_1 = int(args[0], 2)

        if op == 'PRN':
            print(int(self.reg[arg_1], 2), end='')

        elif op == 'PRA':
            address = int(self.reg[arg_1], 2)
            letter = self.ram[address]
            print(chr(int(letter, 2)), end='')

        elif op == 'LDI':
            self.reg[arg_1] = args[1]

        elif op == 'HLT':
            self.exit()

        elif op == 'LD':
            self.reg[arg_1] = self.reg[arg_2]

        elif op == 'PUSH':
            self.sc -= 1
            self.ram[self.sc] = self.reg[arg_1]

        elif op == 'POP':
            self.reg[arg_1] = self.ram[self.sc]
            self.sc += 1

        elif op == 'CALL':
            self.ram[self.sc] = self.ram[self.pc + 1]
            self.sc -= 1
            self.pc = int(self.reg[arg_1], 2)

        elif op == 'RET':
            self.pc = self.ram[self.sc]
            self.sc += 1

        elif op == 'NOP':
            pass

        elif op == 'JMP':
            self.pc = int(self.reg[arg_1], 2)

        elif op == 'JEQ':
            if self.fl & 1:
                self.pc = int(self.reg[arg_1], 2)
                # print('eq', self.pc)
            else:
                self.pc += 1

        elif op == 'JNE':
            if not self.fl & 1:
                self.pc = int(self.reg[arg_1], 2)
            else:
                self.pc += 1

        elif op == 'JGT':
            if self.fl & (1 << 1):
                self.pc = int(self.reg[arg_1], 2)
            else:
                self.pc += 1

        elif op == 'JGE':
            if self.fl & 1 or self.fl & (1 << 1):
                self.pc = int(self.reg[arg_1], 2)
            else:
                self.pc += 1

        elif op == 'JLT':
            if self.fl & (1 << 2):
                self.pc = int(self.reg[arg_1], 2)
            else:
                self.pc += 1

        elif op == 'JLE':
            if self.fl & 1 or self.fl & (1 << 2):
                self.pc = int(self.reg[arg_1], 2)
            else:
                self.pc += 1

        else:
            raise ValueError(f'No such opperation exists {op}')

    def alu(self, op, *args):
        """ALU operations."""
        if len(args) > 1:
            arg_1, arg_2 = int(args[0], 2), int(args[1], 2)
        else:
            arg_1 = int(args[0], 2)

        if op == 'DEC':
            self.reg[arg_1] = f'{int(self.reg[arg_1], 2) - 1:08b}'

        elif op == "INC":
            self.reg[arg_1] = f'{int(self.reg[arg_1], 2) + 1:08b}'

        elif op == "ADD":
            added = (int(self.reg[arg_1], 2) + int(self.reg[arg_2], 2)) & 0xff
            self.reg[arg_1] = f'{added:08b}'

        elif op == "SUB":
            subbed = (int(self.reg[arg_1], 2) - int(self.reg[arg_2], 2)) * 0xff
            self.reg[arg_1] = f'{subbed:08b}'

        elif op == 'MUL':
            mulled = (int(self.reg[arg_1], 2) * int(self.reg[arg_2], 2)) & 0xff
            self.reg[arg_1] = f'{mulled:08b}'

        elif op == 'DIV':
            dived = (int(self.reg[arg_1], 2) >> int(self.reg[arg_2], 2)) & 0xff
            self.reg[arg_1] = f'{dived:08b}'

        elif op == 'MOD':
            modded = (int(self.reg[arg_1], 2) % int(self.reg[arg_2], 2)) & 0xff
            self.reg[arg_1] = f'{modded:08b}'

        elif op == 'CMP':
            comp_a, comp_b = int(self.reg[arg_1], 2), int(self.reg[arg_2], 2)
            # print(comp_a, comp_b)
            if comp_a == comp_b:
                self.fl = self.fl & 0b00000001
                self.fl = self.fl | 0b00000001
            if comp_a > comp_b:
                self.fl = self.fl & 0b00000010
                self.fl = self.fl | 0b00000010
            if comp_a < comp_b:
                self.fl = self.fl & 0b00000100
                self.fl = self.fl | 0b00000100

        elif op == 'AND':
            anded = (int(self.reg[arg_1], 2) & int(self.reg[arg_2])) & 0xff
            self.reg[arg_1] = f'{anded:08b}'

        elif op == 'OR':
            ored = (int(self.reg[arg_1]) | int(self.reg[arg_2])) & 0xff
            self.reg[arg_1] = f'{ored:08b}'

        elif op == 'XOR':
            xored = (int(self.reg[arg_1]) ^ int(self.reg[arg_2])) & 0xff
            self.reg[arg_1] = f'{xored:08b}'

        elif op == 'NOT':
            noted = int(~self.reg[arg_1], 2) & 0xff
            self.reg[arg_1] = f'{noted:08b}'

        elif op == 'SHL':
            shled = (int(self.reg[arg_1], 2) << int(self.reg[arg_2],2 )) & 0xff
            self.reg[arg_1] = f'{shled:08b}'

        elif op == 'SHR':
            shred = (int(self.reg[arg_1], 2) << int(self.reg[arg_2], 2)) & 0xff
            self.reg[arg_1] = f'{shred:08b}'

        else:
            raise ValueError(f"Unsupported ALU operation: {op}")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: pc: {self.pc}, fl: {self.fl}, ir: {self.ir}, ram: {self.ram_read(self.pc)}, "
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
            self.ir = int(self.ram_read(self.pc), 2)
            _bytes = self.ir >> 6
            _alu = self.ir & 0b00100000
            alu = _alu >> 5
            _adv_pc = self.ir & 0b00010000
            adv_pc = _adv_pc >> 4
            instruction = self.ir & 0b00001111
            args = []
            
            for _ in range(_bytes):
                self.pc += 1
                args.append(self.ram_read(self.pc))
            # print('b', _bytes, 'a', alu,
            #       'ad', adv_pc, 'ins', bin(self.ir))
            if not adv_pc:
                self.pc += 1
            op = self.op_map[alu][adv_pc][instruction]
            # print(op, args)
            # self.trace()
            if alu:
                self.alu(op, *args)
            else:
                self.not_alu(op, *args)
