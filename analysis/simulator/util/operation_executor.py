import time
from .stack import EVM_Stack
from .disassembler import Instruction

# Status returned by executor:
# - Exit: Mission completed, stop all executions
# - Halt: stop the execution of this branch
# - Normal: continue the execution
# - Jump: Jump to the offset given in the next parameter
# - JumpI: Jump to the offset given in the next parameter,
#          and create a branch of not jumping to the offset


class OperationExecutor:
    def __init__(self, debug=False):
        self.debug = debug
        self.stack = EVM_Stack()

    def execute(self, instruction: Instruction):
        operation = instruction.operation
        offset = instruction.offset
        data = instruction.data


        # if operation is PUSH1 ~ PUSH32
        if operation.startswith("PUSH"):
            self.stack.execute_PUSH(data)
        # if operation is DUP1 ~ DUP16
        elif operation.startswith("DUP"):
            n = int(operation[3:])
            self.stack.execute_DUP(n)
        # if operation is SWAP1 ~ SWAP16
        elif operation.startswith("SWAP"):
            n = int(operation[4:])
            self.stack.execute_SWAP(n)
        # if operation is ADD, SUB, MUL, MOD
        elif operation in ["ADD", "SUB", "MUL", "MOD", "AND", "OR", "XOR", "DIV", "EXP"]:
            self.stack.execute_arithmetic(operation)
        # if operation is ADDMOD, MULMOD
        elif operation in ["ADDMOD","MULMOD"]:
            self.stack.execute_mod_arithmetic(operation)
        # if operation in ["SHL", "SHR", "SAR"]:
        elif operation in ["SHL", "SHR", "SAR"]:
            self.stack.execute_shift(operation)
        # if operation is GT, LT, EQ, ISZERO
        elif operation in ["GT", "LT", "EQ", "ISZERO"]:
            self.stack.execute_comparison(operation)
        # if operation in JUMP, JUMPI
        elif operation in ["JUMP", "JUMPI"]:
            jumpdest, condition = self.stack.execute_jump(operation)
            # print before return
            if self.debug:
                self.stack.print_stack()
            return operation, jumpdest
        elif operation in ["SLOAD", "SSTORE", "MSTORE", "MLOAD"]:
            self.stack.execute_access(operation)
        elif operation == "NOT":
            self.stack.execute_NOT()
        elif operation == "POP":
            self.stack.execute_POP()
        elif operation in ["CALLVALUE", "CALLDATALOAD", "CALLDATASIZE", "CALLDATACOPY"]:
            self.stack.execute_call(operation)
        elif operation in ["INVALID", "REVERT"]:
            # print before return
            if self.debug:
                self.stack.print_stack()
            return "Halt", 0
        elif operation == "JUMPDEST":
            pass
        elif operation == "SHA3":
            self.stack.execute_SHA3()
        elif operation in ["CODESIZE", "CODECOPY"]:
            self.stack.execute_codeop(operation)
        else:
            # print before return
            if self.debug:
                self.stack.print_stack()
            print("Unknown operation: {}".format(operation))
            exit(0)
            raise Exception("Unknown operation: {}".format(operation))
        
        # print before return
        if self.debug:
            self.stack.print_stack()
        # ask user to continue or abort
            input("Press Enter to continue...")
        
        return "Normal", None
