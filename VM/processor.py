import sys;
class RTN1000:
    def __init__(self, rom):
        self.PC = 0x0000;
        self.program = rom;
        self.reg = [0] * 32;
        self.ram = [0x00] * 65536;
        self.SP = 0x100;
        self.MAX_REG = 31;

    def Clock(self):
        ins = self.program[self.PC]
        self.PC += 1;
        a = self.program[self.PC]
        self.PC += 1;
        b = self.program[self.PC]
        self.PC += 1;
        c = self.program[self.PC]
        self.PC += 1;
        
        if(ins == 0x00): #NOP
            pass
        elif(ins == 0x01): #LD val,reg | val -> reg
            self.reg[b] = a
        elif(ins == 0x02): #LD mem,reg | ram[mem] -> reg
            self.reg[c] = self.ram[CombineBE(a,b)]
        elif(ins == 0x03): #ST reg,mem | reg -> ram[mem]
            self.ram[CombineBE(a,b)] = self.reg[c];
        elif(ins == 0x10): #ADD r1,r2,dest (dest = r1 + r2) 
            RegSet(c,(RegGet(a) + RegGet(b)));
        elif(ins == 0x11): #SUB r1,r2,dest (dest = r1 - r2)
            RegSet(c,(RegGet(a) - RegGet(b)));
        elif(ins == 0x12): #INC r1 | reg -> reg + 1
            RegSet(a, RegGet(a) + 1);
        elif(ins == 0x13): #DEC r1 | reg -> reg - 1
            RegSet(a, RegGet(a) - 1);
        elif(ins == 0x14): #ASR r1,amt | reg -> reg << amt
            RegSet(a, RegGet(a) << b);
        elif(ins == 0x15): #ASL r1,mat | reg -> reg >> amt
            RegSet(a, RegGet(a) >> b);
        elif(ins == 0x20): #JMP addr | addr -> PC
            self.PC = CombineBE(a,b);
        elif(ins == 0x21): #JMZ reg,addr | reg = 0 ? addr -> PC
            self.PC = CombineBE(b,c) if RegGet(a) == 0 else self.PC;
        elif(ins == 0x22): #JNZ reg,addr | reg != 0 ? addr -> PC
            self.PC = CombineBE(b,c) if RegGet(a) != 0 else self.PC;
        elif(ins == 0x23): #JSR addr | PC -> ram[SP++], addr -> PC
            Push(self.PC)
            self.PC = CombineBE(a,b);
        elif(ins == 0x30): #PUSH reg | reg -> ram[SP++]
            Push(RegGet(a));
        elif(ins == 0x31): #POP reg | ram[--SP] -> reg
            RegSet(a, Pop());
        elif(ins == 0xF0): #PRINT reg
            print(RegGet(a));
        elif(ins == 0xF1): #PRINT mem
            print(self.ram[a]);
        elif(ins == 0xF2): #PRINT val
            print(a);
        elif(ins == 0xF3): #PRINTSTR addr
            print(GetString(a));
        elif(ins == 0xF4): #PRGCPY | prog[r0 .. r0 + r2] -> ram[r1 .. r1 + r2]
            src = RegGet(0);
            dest = RegGet(1);
            size = RegGet(2);
            ProgCopy(src,dest,size);
        elif(ins == 0xFE): #EXIT code
            sys.exit(a);
        elif(ins == 0xFF): #EXIT
            sys.exit(RegGet(self.MAX_REG));

        print("[DEBUG] - Registers: ",self.reg," - PC: ",hex(self.PC,4)," - SP: ",hex(self.SP,4))
        

    def __str__(self):
        return ("RTN1000 - Registers: "+str(self.reg)+" - PC: "+hex(self.PC)+" - SP: "+hex(self.SP))

    def RegSet(self, reg, val):
        self.reg[reg] = val;

    def RegGet(self, reg):
        return self.reg[reg];
    
    def Pop(self):
        self.SP -= 1;
        return self.ram[SP]

    def Push(self, val):
        self.ram[self.SP];
        self.SP += 1;
        return;

    def GetStr(addr):
        out = ""
        for x in range(addr, len(self.ram)):
            if(self.ram[x] == 0): break;
            out += chr(self.ram[x])
        return out;

    def ProgCopy(source, dest, size):
        addr = dest;
        for i in range(source, source + size):
            self.ram[addr] = self.program[i];
            addr += 1;

def CombineBE(a,b):
    return (a << 8) | b

            

    
