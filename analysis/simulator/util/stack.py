class EVM_Stack:
    def __init__(self):
        #  bottom   --->    top
        # low index ---> high index
        self.stack = []

        # init stack with 16 empty elements
        for i in range(16):
            self.stack.append("[Unknown] stack [{}]".format(i))
    
    def get_top_idx(self):
        return len(self.stack) - 1

    def deep_copy(self):
        new_stack = EVM_Stack()
        new_stack.stack = [i for i in self.stack]
        return new_stack

    def has_element_on_topOrSecond(self,element):
        if element in self.stack[self.get_top_idx()] or element in self.stack[self.get_top_idx()-1]:
            return True
        return False

    def has_element(self, element):
        if element in self.stack:
            return True
        return False
    
    def print_stack(self):
        print("Stack size after execution: {}".format(len(self.stack)))
        print("--------------------")
        # print stack from top to 15
        for i in range(self.get_top_idx(), self.get_top_idx()-7, -1):
            print(self.stack[i])
        print("...")
        print("--------------------")


    # PUSH1 ...... PUSH32
    def execute_PUSH(self, value):
        data = "[Variable] {}".format(value)
        self.stack.append(data)

    # DUP1 ...... DUP16
    def execute_DUP(self, n):
        # duplicat from unknown stack
        self.stack.append(self.stack[self.get_top_idx() - n + 1])
    
    # SWAP1 ...... SWAP16
    def execute_SWAP(self, n):
        a = self.stack[self.get_top_idx()]
        b = self.stack[self.get_top_idx() - n]
        self.stack[self.get_top_idx()] = b
        self.stack[self.get_top_idx() - n] = a    
    
    # ADD, SUB, MUL, MOD, AND, OR, XOR, DIV, EXP
    def execute_arithmetic(self, op):
        a = self.stack[self.get_top_idx()]
        b = self.stack[self.get_top_idx() - 1]
        self.stack[self.get_top_idx()-1] = "({}) {} ({})".format(a, op, b)
        # if op == "MUL":
        #     print("======MUL========")
        #     print("({}) {} ({})".format(a, op, b))
        self.stack = self.stack[:-1]
    
    def execute_mod_arithmetic(self, op):
        a = self.stack[self.get_top_idx() - 2]
        b = self.stack[self.get_top_idx() - 1]
        m = self.stack[self.get_top_idx() ]
        self.stack[self.get_top_idx()-2] = "({}) {} ({}) % ({})".format(a, op[:3], b, m)
        self.stack = self.stack[:-2]

    # SHL, SHR, SAR
    def execute_shift(self, op):
        a = self.stack[self.get_top_idx()]
        b = self.stack[self.get_top_idx() - 1]
        symbol = "<<" if op == "SHL" else ">>" if op == "SHR" else ">>>"
        self.stack[self.get_top_idx()-1] = "({}) {} ({})".format(a, symbol, b)
        self.stack = self.stack


    # GT, LT, EQ, ISZERO
    def execute_comparison(self, op):
        # GT, LT, EQ
        if op in ["GT", "LT", "EQ"]:
            a = self.stack[self.get_top_idx()]
            b = self.stack[self.get_top_idx()-1]
            self.stack[self.get_top_idx()-1] = "({}) {} ({})".format(a, op, b)
            self.stack = self.stack[:-1]
        # ISZERO
        elif op == "ISZERO":
            a = self.stack[self.get_top_idx()]
            self.stack[self.get_top_idx()] = "ISZERO({})".format(a)
    
    # SLOAD, SSTORE, MSTORE, MLOAD
    def execute_access(self, op):
        if op == "SLOAD":
            self.stack[self.get_top_idx()] = "Storage[{}]".format(self.stack[self.get_top_idx()])
        elif op == "MLOAD":
            self.stack[self.get_top_idx()] = "Memory[{}]".format(self.stack[self.get_top_idx()])
        elif op == "SSTORE":
            self.stack = self.stack[:-2]
        elif op == "MSTORE":
            self.stack = self.stack[:-2]
    
    # POP
    def execute_POP(self):
        self.stack = self.stack[:-1]

    # JUMP, JUMPI
    def execute_jump(self, op):
        if op == "JUMP":
            jumpdest = self.stack[self.get_top_idx()]
            self.stack = self.stack[:-1]
            return jumpdest, None
        elif op == "JUMPI":
            jumpdest = self.stack[self.get_top_idx()]
            condition = self.stack[self.get_top_idx()-1]
            self.stack = self.stack[:-2]
            return jumpdest, condition

    def execute_SHA3(self):
        self.stack[self.get_top_idx()] = "SHA3({})".format(self.stack[self.get_top_idx()])

    # CODESIZE, CODECOPY
    def execute_codeop(self,op):
        if op == "CODESIZE":
            self.stack.append("codesize")
        elif op == "CODECOPY":
            self.stack = self.stack[:-3]

    def execute_NOT(self):
        self.stack[self.get_top_idx()] = "NOT({})".format(self.stack[self.get_top_idx()])

    def execute_call(self, op):
        if op == "CALLVALUE":
            self.stack.append("call.value")
        elif op == "CALLDATALOAD":
            self.stack[self.get_top_idx()] = "call.data[{}]".format(self.stack[self.get_top_idx()])
        elif op == "CALLDATASIZE":
            self.stack.append("size(call.data)")
        elif op == "CALLDATACOPY":
            self.stack = self.stack[:-3]