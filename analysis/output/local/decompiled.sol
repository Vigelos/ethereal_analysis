// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

/// @title            Decompiled Contract
/// @author           Jonathan Becker <jonathan@jbecker.dev>
/// @custom:version   heimdall-rs v0.8.2
///
/// @notice           This contract was decompiled using the heimdall-rs decompiler.
///                     It was generated directly by tracing the EVM opcodes from this contract.
///                     As a result, it may not compile or even be valid solidity code.
///                     Despite this, it should be obvious what each function does. Overall
///                     logic should have been preserved throughout decompiling.
///
/// @custom:github    You can find the open-source decompiler here:
///                       https://heimdall.rs

contract DecompiledContract {
    
    
    /// @custom:selector    0x11479fea
    /// @custom:signature   Unresolved_11479fea(uint256 arg0, uint256 arg1, uint256 arg2, uint256 arg3) public payable returns (uint256)
    /// @param              arg8 ["uint256", "bytes32", "int256"]
    /// @param              arg9 ["uint256", "bytes32", "int256"]
    /// @param              arg10 ["uint256", "bytes32", "int256"]
    /// @param              arg11 ["uint256", "bytes32", "int256"]
    function Unresolved_11479fea(uint256 arg0, uint256 arg1, uint256 arg2, uint256 arg3) public payable returns (uint256) {
        require(msg.value);
        require(0x44 > msg.data.length);
        require(0xc4 > msg.data.length);
        require(0x0104 > msg.data.length);
        require(0x0164 > msg.data.length);
        uint256 var_a = var_a + 0x0380;
        require(!0x30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47 > arg8);
        uint256 var_b = 0;
        return 0;
        require(!0x30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47 > arg9);
        var_b = 0;
        return 0;
        require(!0x30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47 > arg10);
        var_b = 0;
        return 0;
        require(!0x30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47 > arg11);
        var_b = 0;
        return 0;
        var_c = 0x2c235c58c31ea661cda842be40babc5f55216450cdc2ba3e7cfdd0c38726ad92;
        var_d = 0x07b664f0c88018661cce182aef0362013b398927fd1b608e5d2de1cf68f9b95b;
        var_e = 0x274bd7231500754153d2c36b404f3806d27ee83d9f3929be6c0b05cac5d090bd;
        var_f = 0x1bebd67c2ab80ed58474ffcd173fb20bfcd15094410a5e8c0c948af57ceaeb1e;
        uint256 var_g = arg8;
        (bool success, bytes memory ret0) = address(0x07).{ gas: gasleft() - 0x07d0 }staticcall(abi.encode(0x274bd7231500754153d2c36b404f3806d27ee83d9f3929be6c0b05cac5d090bd, 0x1bebd67c2ab80ed58474ffcd173fb20bfcd15094410a5e8c0c948af57ceaeb1e, arg8));
        var_b = 0;
        return 0;
        var_g = var_h;
        var_i = var_j;
        (bool success, bytes memory ret0) = address(0x06).{ gas: gasleft() - 0x07d0 }staticcall(abi.encode(0x274bd7231500754153d2c36b404f3806d27ee83d9f3929be6c0b05cac5d090bd, 0x1bebd67c2ab80ed58474ffcd173fb20bfcd15094410a5e8c0c948af57ceaeb1e, var_h, var_j));
        var_b = 0;
        return 0;
        var_e = 0x15361ae10614c1f1cd8c2fd2a53491eb95bbd15507a2515defc38ea226c54360;
        var_f = 0x1a200a94c040aae7de7ecdf4773fff7f4be656e51b65957134332a0bd3efedfa;
        var_g = arg9;
        (bool success, bytes memory ret0) = address(0x07).{ gas: gasleft() - 0x07d0 }staticcall(abi.encode(0x15361ae10614c1f1cd8c2fd2a53491eb95bbd15507a2515defc38ea226c54360, 0x1a200a94c040aae7de7ecdf4773fff7f4be656e51b65957134332a0bd3efedfa, arg9));
        var_b = 0;
        return 0;
        var_g = var_h;
        var_i = var_j;
        (bool success, bytes memory ret0) = address(0x06).{ gas: gasleft() - 0x07d0 }staticcall(abi.encode(0x15361ae10614c1f1cd8c2fd2a53491eb95bbd15507a2515defc38ea226c54360, 0x1a200a94c040aae7de7ecdf4773fff7f4be656e51b65957134332a0bd3efedfa, var_h, var_j));
        var_b = 0;
        return 0;
        var_e = 0x0af34571f0b0f3f8e1935f2ed0508e4496fa01c57869f638f60a6c5f63d23643;
        var_f = 0x256fe3487628807083293ff8193191fba9ea23b768d0fa5022dadc19d2fe50d7;
        var_g = arg10;
        (bool success, bytes memory ret0) = address(0x07).{ gas: gasleft() - 0x07d0 }staticcall(abi.encode(0x0af34571f0b0f3f8e1935f2ed0508e4496fa01c57869f638f60a6c5f63d23643, 0x256fe3487628807083293ff8193191fba9ea23b768d0fa5022dadc19d2fe50d7, arg10));
    }
}