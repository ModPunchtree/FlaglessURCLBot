
from genericURCLOptimiser.constants import alpha

##################################################################################

# clean code
    # 1 cut off $optimise
    # 2 delete line comments
    # 3 delete empty lines
    # 4 relatives to labels
    # 5 convert BZR/BZN to BRZ/BNZ

# label/branching optimisations
    # 1 delete duplicate labels
    # 2 shortcut branches
    # 3 delete useless branches

# constant folding

# single instruction optimisations
    # 1  ADD   -> LSH, MOV, INC, DEC, NOP
    # 2  RSH   -> MOV, NOP
    # 3  LOD   -> NOP
    # 4  STR   -> 
    # 5  JMP   -> 
    # 6  BGE   -> JMP, BRZ, BNZ, BRN, BRP, NOP
    # 7  NOR   -> NOT, MOV, NOP
    # 8  SUB   -> MOV, NEG, DEC, INC, NOP
    # 9  MOV   -> IMM, NOP
    # 10 LSH   -> NOP
    # 11 DEC   -> NOP
    # 12 NEG   -> NOP
    # 13 AND   -> MOV, NOP
    # 14 OR    -> MOV, NOP
    # 15 NOT   -> MOV
    # 16 XNOR  -> XOR, NOT, MOV, NOP
    # 17 XOR   -> MOV, NOT, NOP
    # 18 NAND  -> NOT, MOV, NOP
    # 19 BRL   -> JMP, BRZ, BNZ, BRN, BRP, NOP
    # 20 BRG   -> JMP, BRZ, BNZ, BRN, BRP, NOP
    # 21 BRE   -> JMP, BRZ, NOP
    # 22 BNE   -> JMP, BNZ, NOP
    # 23 BOD   -> JMP, NOP
    # 24 BEV   -> JMP, NOP
    # 25 BLE   -> JMP, BRZ, BNZ, NOP
    # 26 BRZ   -> JMP, NOP
    # 27 BNZ   -> JMP, NOP
    # 28 BRN   -> JMP, NOP
    # 29 BRP   -> JMP, NOP
    # 30 PSH   -> 
    # 31 POP   -> INC
    # 32 CAL   -> 
    # 33 RET   -> 
    # 34 HLT   -> 
    # 35 MLT   -> LSH, BSL, MOV, NOP
    # 36 DIV   -> RSH, BSR, MOV, NOP
    # 37 MOD   -> AND, MOV, NOP
    # 38 BSR   -> RSH, MOV, NOP
    # 39 BSL   -> LSH, MOV, NOP
    # 40 SRS   -> MOV, NOP
    # 41 BSS   -> SRS, BSR, MOV, NOP
    # 42 SETE  -> MOV, NOP
    # 43 SETNE -> MOV, NOP
    # 44 SETG  -> MOV, NOP
    # 45 SETL  -> MOV, NOP
    # 46 SETGE -> MOV, NOP
    # 47 SETLE -> MOV, NOP

# miscellaneous optimisations
    # SETBNZ
    # LODSTR
    # STRLOD
    # PSHPOP
    # POPPSH

# pre-execution optimisation
# list of lists?

##################################################################################

def genericURCLoptimiser(raw: str, BITS: int) -> list:
    
    # clean code
    # 1 cut off $optimise
    if type(raw) == str:
        if raw.startswith("$optimise"):
            code = raw[9: ]
        else:
            code = raw
        code = code.split("\n")
    elif raw[0] == "$optimise":
        code = raw[1: ]
    else:
        code = raw
    
    # 2 delete line comments
    code = [i[: i.index("//")] if i.find("//") != -1 else i for i in code]
    
    # 3 delete empty lines
    code = list(filter(None, code))
    
    # 4 relatives to labels
    global uniqueNum; uniqueNum = 0
    code = relativesToLabels(code)
    
    # 5 convert BZR/BZN to BRZ/BNZ
    code = ["BRZ" + i[3:] if i.startswith("BZR")
            else "BNZ" + i[3: ] if i.startswith("BZN")
            else i for i in code]

    # optimisation loop
    while True:
        returnedCode = optimise(code, BITS)
        if code == returnedCode:
            return code
        code = returnedCode

def optimise(code: list, BITS: int) -> list:
    # label/branching optimisations
    # 1 delete duplicate labels
    code = deleteDuplicateLabels(code)
    
    # 2 shortcut branches
    returnedCode = shortcutBranches(code)
    if code == returnedCode:
        return returnedCode
    else:
        code = returnedCode
        
    # 3 delete useless branches
    returnedCode = deleteUselessBranches(code)
    if code == returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # constant folding
    returnedCode = constantFolding(code, BITS)
    if code == returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # single instruction optimisations
    returnedCode = singleInstructionOptimisations(code, BITS)
    if code == returnedCode:
        return returnedCode
    else:
        code = returnedCode
        
    # miscellaneous optimisations
    returnedCode = miscellaneousOptimisations(code, BITS)
    if code == returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # pre-execution optimisation #####################################################################
    
    
    return code

def relativesToLabels(code: list) -> list:
    for i, j in enumerate(code):
        if j.find("+") != -1:
            num = readNum(j[j.find("+") + 1: ])
            code.insert(i + j, ".relativeLabel" + uniqueNumber())
            return relativesToLabels(code)
        elif j.find("-") != -1:
            num = readNum(j[j.find("-") + 1: ])
            code.insert(i - j, ".relativeLabel" + uniqueNumber())
            return relativesToLabels(code)
    return code

def readNum(text: str) -> int:
    temp = ""
    for i in text:
        if (i.isnumeric()) or (i == "x"):
            temp += i
        else:
            return int(temp, 0)
    return int(temp, 0)
    
def uniqueNumber() -> str:
    global uniqueNum
    uniqueNum += 1
    return str(uniqueNum)

def deleteDuplicateLabels(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            return code
        if j.startswith(".") and code[i + 1].startswith("."):
            code.pop(i)
            for k, l in code:
                while (l.find(j) != -1) and (i[l.find(j) + 1: l.find(j) + 2] in [i for i in alpha()]):
                    l = l.replace(j, code[i], 1)
                code[k] = l
                return deleteDuplicateLabels(code)

def shortcutBranches(code: list) -> list:
    for i, j in enumerate(code):
        if j.startswith(("JMP", "BGE", "BLE", "BRG", "BRL", "BRZ", "BNZ", "BOD", "BEV", "BRP", "BRN")):
            if j.startswith("JMP"):
                label = j[4: ]
                rest = ""
            else:
                label = j[4: j.find(",")]
                rest = j[j.find(","): ]
            location = code[code.index(label) + 1]
            if location.startswith("JMP"):
                label2 = location[4: ]
                code[i] = j[:4] + label2 + rest
                return shortcutBranches(code)
    return code

def deleteUselessBranches(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            return code
        if j.startswith(("JMP", "BGE", "BLE", "BRG", "BRL", "BRZ", "BNZ", "BOD", "BEV", "BRP", "BRN")):
            if j.startswith("JMP"):
                label = j[4: ]
            if code[i + 1] == label:
                code.pop(i)
                return deleteUselessBranches(code)

def singleInstructionOptimisations(code: list, BITS: int) -> list:
    for i, j in enumerate(code):
        op = readOperation(j)
        ops = readOps(j[len(op): ])
        
        # 1  ADD   -> LSH, MOV, INC, DEC, NOP
        if op == "ADD":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "DEC " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "DEC " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "1":
                code[i] == "INC " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == "1":
                code[i] == "INC " + ops[0] + ", " + ops[2]
                return code
            elif (ops[2] == "0") or (ops[2] == "R0"):
                code[i] == "MOV " + ops[0] + ", " + ops[1]
                return code
            elif (ops[1] == "0") or (ops[1] == "R0"):
                code[i] == "MOV " + ops[0] + ", " + ops[2]
                return code
            elif ops[1] == ops[2]:
                code[i] == "LSH " + ops[0] + ", " + ops[1]
                return code
            
        # 2  RSH   -> MOV, NOP
        elif op == "RSH":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif (ops[1] == "R0") or (ops[1] == "0") or (ops[1] == "1"):
                code[i] = "MOV " + ops[0] + ", 0"
                return code
        
        # 3  LOD   -> NOP
        elif op == "LOD":
            if ops[0] == "R0":
                code.pop(i)
                return code
        
        # 4  STR   -> 
        elif op == "STR":
            pass
        
        # 5  JMP   -> 
        elif op == "JMP":
            pass
        
        # 6  BGE   -> JMP, BRZ, BNZ, BRN, BRP, NOP
        elif op == "BGE":
            if ops[1] == ops[2]:
                code[i] = "JMP " + ops[0]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "JMP " + ops[0]
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "BRZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "1":
                code[i] = "BNZ " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == str(2 ** (BITS - 1)):
                code[i] = "BRN " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** (BITS - 1)):
                code[i] = "BRP " + ops[0] + ", " + ops[2]
                return code
        
        # 7  NOR   -> NOT, MOV, NOP
        elif op == "NOR":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif (ops[2] == "0") or (ops[2] == "R0"):
                code[i] = "NOT " + ops[0] + ", " + ops[1]
                return code
            elif (ops[1] == "0") or (ops[1] == "R0"):
                code[i] = "NOT " + ops[0] + ", " + ops[2]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 0"
                return code

        # 8  SUB   -> MOV, NEG, DEC, INC, NOP
        elif op == "SUB":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[2] == "1":
                code[i] = "DEC " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "INC " + ops[0] + ", " + ops[1]
                return code
            elif (ops[1] == "0") or (ops[1] == "R0"):
                code[i] = "NEG " + ops[0] + ", " + ops[1]
                return code
            elif (ops[2] == "0") or (ops[2] == "R0"):
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code

        # 9  MOV   -> IMM, NOP
        elif op == "MOV":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1][0].isnumeric():
                code[i] = "IMM " + ops[0] + ", " + ops[1]
                return code

        # 10 LSH   -> NOP
        elif op == "LSH":
            if ops[0] == "R0":
                code.pop(i)
                return code

        # 11 DEC   -> NOP
        elif op == "DEC":
            if ops[0] == "R0":
                code.pop(i)
                return code
            
        # 12 NEG   -> NOP
        elif op == "NEG":
            if ops[0] == "R0":
                code.pop(i)
                return code
        
        # 13 AND   -> MOV, NOP
        elif op == "AND":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif (ops[1] == "0") or (ops[1] == "R0") or (ops[2] == "0") or (ops[2] == "R0"):
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif (ops[1] == str(2 ** BITS - 1)) or (ops[1] == ops[2]):
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "MOV " + ops[0] + ", " + ops[2]
                return code
            
        # 14 OR    -> MOV, NOP
        elif op == "OR":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "MOV " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", " + ops[2]
                return code
    
        # 15 NOT   -> MOV
        elif op == "NOT":
            if ops[0] == "R0":
                code.pop(i)
                return code      
            
        # 16 XNOR  -> XOR, NOT, MOV, NOP
        elif op == "XNOR":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] == "NOT " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] == "NOT " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] == "MOV " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] == "MOV " + ops[0] + ", " + ops[1]
                return code
            
        # 17 XOR   -> MOV, NOT, NOP
        elif op == "XOR":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] == "MOV " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] == "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] == "NOT " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] == "NOT " + ops[0] + ", " + ops[1]
                return code
            
        # 18 NAND  -> NOT, MOV, NOP
        if op == "NAND":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0" or ops[2] == "0" or ops[2] == "R0":
                code[i] = "IMM " + ops[0] + ", " + str(2 ** BITS - 1)
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "NOT " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "NOT " + ops[0] + ", " + ops[2]
                return code
        
        # 19 BRL   -> JMP, BRZ, BNZ, BRN, BRP, NOP
        elif op == "BRL":
            if ops[1] == ops[2]:
                code.pop(i)
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "BNZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "1":
                code[i] = "BRZ " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == str(2 ** (BITS - 1)):
                code[i] = "BRP " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** (BITS - 1) - 1):
                code[i] = "BRN " + ops[0] + ", " + ops[2]
                return code
        
        # 20 BRG   -> JMP, BRZ, BNZ, BRN, BRP, NOP
        elif op == "BRG":
            if ops[1] == ops[2]:
                code.pop(i)
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "BNZ " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "1":
                code[i] = "BRZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** (BITS - 1) - 1):
                code[i] = "BRN " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** (BITS - 1)):
                code[i] = "BRP " + ops[0] + ", " + ops[2]
                return code
        
        # 21 BRE   -> JMP, BRZ, NOP
        elif op == "BRE":
            if ops[1] == ops[2]:
                code[i] = "JMP " + ops[0]
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "BRZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "BRZ " + ops[0] + ", " + ops[1]
                return code
        
        # 22 BNE   -> JMP, BNZ, NOP
        elif op == "BNE":
            if ops[1] == ops[2]:
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "BNZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "BNZ " + ops[0] + ", " + ops[1]
                return code
        
        # 23 BOD   -> JMP, NOP
        elif op == "BOD":
            if ops[1] == "R0":
                code.pop(i)
                return code
        
        # 24 BEV   -> JMP, NOP
        elif op == "BEV":
            if ops[1] == "R0":
                code[i] = "JMP " + ops[0]
                return code
        
        # 25 BLE   -> JMP, BRZ, BNZ, NOP
        elif op == "BLE":
            if ops[1] == ops[2]:
                code[i] = "JMP " + ops[0]
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "BRZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "JMP " + ops[0]
                return code
            elif ops[1] == "1":
                code[i] = "BNZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[1] == str(2 ** (BITS - 1)):
                code[i] = "BRN " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** (BITS - 1) - 1):
                code[i] = "BRP " + ops[0] + ", " + ops[1]
                return code
        
        # 26 BRZ   -> JMP, NOP
        elif op == "BRZ":
            if ops[1] == "R0":
                code[i] = "JMP " + ops[0]
                return code
        
        # 27 BNZ   -> JMP, NOP
        elif op == "BNZ":
            if ops[1] == "R0":
                code.pop(i)
                return code
        
        # 28 BRN   -> JMP, NOP
        elif op == "BRN":
            if ops[1] == "R0":
                code.pop(i)
                return code
            
        # 29 BRP   -> JMP, NOP
        elif op == "BRP":
            if ops[1] == "R0":
                code[i] = "JMP " + ops[0]
                return code
        
        # 30 PSH   -> 
        elif op == "PSH":
            pass
        
        # 31 POP   -> INC
        elif op == "POP":
            if ops[1] == "R0":
                code[i] = "INC SP, SP"
                return code
        
        # 32 CAL   -> 
        elif op == "CAL":
            pass
        
        # 33 RET   -> 
        elif op == "RET":
            pass
        
        # 34 HLT   -> 
        elif op == "HLT":
            pass
        
        # 35 MLT   -> LSH, BSL, MOV, NOP
        elif op == "MLT":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0" or ops[2] == "0" or ops[2] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[1] == "1":
                code[i] = "MOV " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "1":
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == "3":
                code[i] = "LSH " + ops[0] + ", " + ops[2]
                code.insert(i + 1, "ADD " + ops[0] + ", " + ops[0] + ", " + ops[2])
                return code
            elif ops[2] == "3":
                code[i] = "LSH " + ops[0] + ", " + ops[1]
                code.insert(i + 1, "ADD " + ops[0] + ", " + ops[0] + ", " + ops[1])
                return code
            elif ops[1] == "5":
                code[i] = "LSH " + ops[0] + ", " + ops[2]
                code.insert(i + 1, "LSH " + ops[0] + ", " + ops[0])
                code.insert(i + 1, "ADD " + ops[0] + ", " + ops[0] + ", " + ops[2])
                return code
            elif ops[2] == "5":
                code[i] = "LSH " + ops[0] + ", " + ops[1]
                code.insert(i + 1, "LSH " + ops[0] + ", " + ops[0])
                code.insert(i + 1, "ADD " + ops[0] + ", " + ops[0] + ", " + ops[1])
                return code
            elif ops[1][0].isnumeric():
                if int(ops[1], 0) in [2 ** i for i in range(BITS)]:
                    shift = str([2 ** i for i in range(BITS)].index(int(ops[1], 0)))
                    code[i] = "BSL " + ops[0] + ", " + ops[2] + ", " + shift
                    return code
            if ops[2][0].isnumeric():
                if int(ops[2], 0) in [2 ** i for i in range(BITS)]:
                    shift = str([2 ** i for i in range(BITS)].index(int(ops[2], 0)))
                    code[i] = "BSL " + ops[0] + ", " + ops[1] + ", " + shift
                    return code
        
        # 36 DIV   -> RSH, BSR, MOV, NOP
        elif op == "DIV":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "SETE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
            elif ops[2] == "1":
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code
            if ops[2][0].isnumeric():
                if int(ops[2], 0) in [2 ** i for i in range(BITS)]:
                    shift = str([2 ** i for i in range(BITS)].index(int(ops[2], 0)))
                    code[i] = "BSR " + ops[0] + ", " + ops[1] + ", " + shift
                    return code
        
        # 37 MOD   -> AND, MOV, NOP
        elif op == "MOD":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == "1":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            if ops[2][0].isnumeric():
                if int(ops[2], 0) in [2 ** i for i in range(BITS)]:
                    code[i] = "AND " + ops[0] + ", " + ops[1] + ", " + str(int(ops[2], 0) - 1)
                    return code
        
        # 38 BSR   -> RSH, MOV, NOP
        elif op == "BSR":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] == "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == "1":
                code[i] == "RSH " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == "2":
                code[i] == "RSH " + ops[0] + ", " + ops[1]
                code[i] == "RSH " + ops[0] + ", " + ops[0]
                return code
            elif ops[2][0].isnumeric():
                if int(ops[2], 0) >= BITS:
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
        
        # 39 BSL   -> LSH, MOV, NOP
        elif op == "BSL":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] == "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == "1":
                code[i] == "LSH " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == "2":
                code[i] == "LSH " + ops[0] + ", " + ops[1]
                code[i] == "LSH " + ops[0] + ", " + ops[0]
                return code
            elif ops[2][0].isnumeric():
                if int(ops[2], 0) >= BITS:
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
        
        # 40 SRS   -> MOV, NOP
        elif op == "SRS":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            
        # 41 BSS   -> SRS, BSR, MOV, NOP
        elif op == "BSS":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == "1":
                code[i] = "SRS " + ops[0] + ", " + ops[1]
                return code
            elif ops[1][0].isnumeric():
                if int(ops[1], 0) < 2 ** (BITS - 1):
                    code[i] = "BSR " + ops[0] + ", " + ops[1] + ", " + ops[2]
                    return code

        # 42 SETE  -> MOV, NOP
        elif op == "SETE":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == ops[2]:
                code[i] = "IMM " + ops[0] + ", 1"
                return code
            elif ops[1][0].isnumeric():
                if ops[2] == "R0" and ops[1] != "0":
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
                elif ops[2] == "R0" and ops[1] == "0":
                    code[i] = "IMM " + ops[0] + ", 1"
                    return code
            if ops[2][0].isnumeric():
                if ops[1] == "R0" and ops[2] != "0":
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
                elif ops[1] == "R0" and ops[2] == "0":
                    code[i] = "IMM " + ops[0] + ", 1"
                    return code
                
        # 43 SETNE -> MOV, NOP
        elif op == "SETNE":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == ops[2]:
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[1][0].isnumeric():
                if ops[2] == "R0" and ops[1] != "0":
                    code[i] = "IMM " + ops[0] + ", 1"
                    return code
                elif ops[2] == "R0" and ops[1] == "0":
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
            if ops[2][0].isnumeric():
                if ops[1] == "R0" and ops[2] != "0":
                    code[i] = "IMM " + ops[0] + ", 1"
                    return code
                elif ops[1] == "R0" and ops[2] == "0":
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
        
        # 44 SETG  -> MOV, NOP
        elif op == "SETG":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == ops[2]:
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "SETNE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 0"
                return code
        
        # 45 SETL  -> MOV, NOP
        elif op == "SETL":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == ops[2]:
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "SETNE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
        
        # 46 SETGE -> MOV, NOP
        elif op == "SETGE":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 1"
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "SETE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "IMM " + ops[0] + ", 1"
                return code
        
        # 47 SETLE -> MOV, NOP
        elif op == "SETLE":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "SETE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 1"
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "SETE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
            
        else:
            raise Exception("FATAL - Unrecognised instruction: " + str(code[i]))
    return code

def readOperation(instruction: str) -> str:
    if instruction.find(" ") != -1:
        return instruction[: instruction.index(" ")]
    else:
        return instruction

def readOps(text: str) -> tuple:
    ops = ()
    temp = ""
    for i in text:
        if i == ",":
            ops += (temp,)
        else:
            temp += i
    if temp:
        ops += (temp,)
    return ops

def constantFolding(code: list, BITS: int) -> list:
    for i, j in enumerate(code):
        op = readOperation(j)
        ops = readOps(j[len(op): ])
        
        if op in ("ADD", "RSH", "BGE", "NOR", "SUB", "MOV", "LSH", "DEC", "NEG", "AND", "OR", "NOT", "XNOR", "XOR", "NAND", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "MLT", "DIV", "MOD", "BSR", "BSL", "SRS", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE"):
            if op == "ADD":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) + int(ops[2], 0))
                    return code
            elif op == "RSH":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) // 2)
                    return code
            elif op == "BGE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) >= int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "NOR":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str((2 ** BITS - 1) - (int(ops[1], 0) | int(ops[2], 0)))
                    return code
            elif op == "SUB":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) >= int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) - int(ops[2], 0))
                    else:
                        code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) - int(ops[2], 0) + (2 ** BITS))
                    return code
            elif op == "MOV":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + ops[1]
                    return code
            elif op == "LSH":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) * 2)
                    return code
            elif op == "DEC":
                if ops[1][0].isnumeric():
                    if ops[1] == "0":
                        code[i] = "IMM " + ops[0] + ", " + str(int(2 ** BITS - 1))
                    else:
                        code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) - 1)
                    return code
            elif op == "NEG":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str((2 ** BITS) - int(ops[1], 0))
                    return code
            elif op == "AND":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) & int(ops[2], 0))
                    return code
            elif op == "OR":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) | int(ops[2], 0))
                    return code
            elif op == "NOT":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str((2 ** BITS - 1) - int(ops[1], 0))
                    return code
            elif op == "XNOR":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str((2 ** BITS - 1) - (int(ops[1], 0) ^ int(ops[2], 0)))
                    return code
            elif op == "XOR":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) ^ int(ops[2], 0))
                    return code
            elif op == "NAND":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str((2 ** BITS - 1) - (int(ops[1], 0) & int(ops[2], 0)))
                    return code
            elif op == "BRL":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) < int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BRG":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) > int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BRE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) == int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BNE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) != int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BOD":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) % 2 == 1:
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BEV":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) % 2 == 0:
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BRL":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) <= int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BRZ":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) == 0:
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BNZ":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) != 0:
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BRN":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) >= (2 ** (BITS - 1)):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BRP":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) < (2 ** (BITS - 1)):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "MLT":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + correctValue(int(ops[1], 0) * int(ops[2], 0))
                    return code
            elif op == "DIV":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) // int(ops[2], 0))
                    return code
            elif op == "MOD":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) % int(ops[2], 0))
                    return code
            elif op == "BSR":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) // 2 ** int(ops[2], 0))
                    return code
            elif op == "BSL":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + correctValue(int(ops[1], 0) * 2 ** int(ops[2], 0))
                    return code
            elif op == "SRS":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) >= 2 ** (BITS - 1): 
                        code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) // 2 + 2 ** (BITS - 1))
                    else:
                        code[i] = "IMM " + ops[0] + ", " + correctValue(int(ops[1], 0) // 2)
                    return code
            elif op == "BSS":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) >= 2 ** (BITS - 1):
                        num = int(ops[1], 0)
                        for i in range(int(ops[2], 0)):
                            num // 2 + 2 ** (BITS - 1)
                        code[i] = "IMM " + ops[0] + ", " + str(num)
                    else:
                        code[i] = "IMM " + ops[0] + ", " + correctValue(int(ops[1], 0) // int(ops[2], 0))
                    return code
            elif op == "SETE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) == int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
            elif op == "SETNE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) != int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
            elif op == "SETG":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) > int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
            elif op == "SETL":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) > int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
            elif op == "SETGE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) >= int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
            elif op == "SETLE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) <= int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
        
    return code

def correctValue(value: str, BITS: int) -> str:
    num = int(value, 0)
    if num >= (2 ** BITS):
        num %= 2 ** BITS
    while num < 0:
        num += 2 ** BITS
    return str(num)

def miscellaneousOptimisations(code: list, BITS: int) -> list:
    
    # SETBNZ
    returnedCode = SETBRZ(code)
    if code == returnedCode:
        return returnedCode
    else:
        code = returnedCode
        
    # LODSTR
    returnedCode = LODSTR(code)
    if code == returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # STRLOD
    returnedCode = STRLOD(code)
    if code == returnedCode:
        return returnedCode
    else:
        code = returnedCode
        
    # PSHPOP
    returnedCode = PSHPOP(code)
    if code == returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # POPPSH
    returnedCode = POPPSH(code)
    if code == returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    return code

def SETBRZ(code: list) -> list:
    for i, j in enumerate(code)[: -1]:
        if j.startswith("SET") and code[i + 1].startswith("BRZ") and code[i + 1][code[i + 1].find(",") + 2: ] == j[j.find(" ") + 1: j.find(",")]:
            if j[3: 5] == "GE":
                code[i + 1] = "BRL " + code[i + 1][4: code[i + 1].index(",")] + j[j.index(","): ]
                code.pop(i)
                return SETBRZ(code)
            elif j[3: 5] == "LE":
                code[i + 1] = "BRG " + code[i + 1][4: code[i + 1].index(",")] + j[j.index(","): ]
                code.pop(i)
                return SETBRZ(code)
            elif j[3] == "G":
                code[i + 1] = "BLE " + code[i + 1][4: code[i + 1].index(",")] + j[j.index(","): ]
                code.pop(i)
                return SETBRZ(code)
            elif j[3] == "L":
                code[i + 1] = "BGE " + code[i + 1][4: code[i + 1].index(",")] + j[j.index(","): ]
                code.pop(i)
                return SETBRZ(code)
    return code

def LODSTR(code: list) -> list:
    for i, j in enumerate(code)[: -1]:
        if j.startswith("LOD") and code[i + 1].startswith("STR") and j[j.find(" ") + 1: j.find(",")] == code[i + 1][code[i + 1].index(",") + 2: ] and j[j.find(",") + 2: ] == code[i + 1][code[i + 1].find(" ") + 1: code[i + 1].find(",")]:
            code.pop(i + 1)
            return LODSTR(code)
    return code

def STRLOD(code: list) -> list:
    for i, j in enumerate(code)[: -1]:
        if j.startswith("STR") and code[i + 1].startswith("LOD") and j[j.find(" ") + 1: j.find(",")] == code[i + 1][code[i + 1].find(",") + 2: ]:
            code[i + 1] = "MOV " + code[i + 1][4: code[i + 1].index(",")] + j[j.index(","): ]
            return STRLOD(code)
    return code

def PSHPOP(code: list) -> list:
    for i, j in enumerate(code)[: -1]:
        if j.startswith("PSH") and code[i + 1].startswith("POP"):
            code[i + 1] = "MOV " + j[j.index(" ") + 1: ] + ", " + code[i + 1][code[i + 1].index(" ") + 1: ]
            code.pop(i)
            return PSHPOP(code)
    return code

def POPPSH(code: list) -> list:
    for i, j in enumerate(code)[: -1]:
        if j.startswith("POP") and code[i + 1].startswith("PSH"):
            code[i] = "LOD " + j[j.index(" ") + 1: ] + ", SP"
            code[i + 1] = "STR SP, " + code[i + 1][code[i + 1].index(" ") + 1: ]
            return POPPSH(code)
    return code
