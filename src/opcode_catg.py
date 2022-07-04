opcode_bytecode = ["nop", \
    ["move", "from"], "return", "const", "monitor", ["sget", "sput"], \
    "check-cast", ["new-instance", "instance-of", "iget", "iput"], "throw", \
        "goto", "cmp", ["if", "switch"], \
            ["invoke-virtual","invoke-super", "invoke-direct", "invoke-static", "invoke-interface"], \
                ["array-length", "new-array", "filled-new-array", "fill-array-data", "aget", "aput"],\
                    ["sparse-switch", "packed-switch"], \
                        ["int", "long", "double", "float", "byte", "char", "short"]]

opcode_assembly = [["ldr", "str", "adr", "ldm", "stm", "swp"], \
    ["add", "sub", "and", "orr", "bic", "orn", "eor", "lsl", "lsr", "asr", "ror", "rsb", "adc", "sbc", "rsc", "mul"],\
        "nop", ["b", "bl", "bx"], ["mov", "mvn"],\
            ["cmp", "cmn", "tst", "teq"], ]
