; build curved histogram.

; expected output
; *
; **
; ****
; ********
; ****************
; ********************************
; ****************************************************************

    LDI R0,7  ; Number of lines
    LDI R1,1  ; Starting number of *
    LDI R2,PrintLine
    LDI R3,0xa0
    ST R3,R1
    CALL R2

Halt:

    HLT

PrintLine:

    LDI R2,0
    CMP R2,R0
    LDI R3,Halt
    JEQ R3
    LDI R3,0xa0
    ST R3,R1
    LDI R3,PrintStar
    CALL R3
    LDI R3,0x0a
    PRA R3
    LDI R3,0xa0
    LD R1,R3
    LDI R3,1
    SHL R1,R3
    DEC R0
    LDI R3,Printline
    JMP R3


PrintStar:

    LDI R3,Star
    LD R2,R3
    PRA R2
    LDI R2,0
    DEC R1
    CMP R2,R1
    LDI R3,PrintStar
    JNE R3
    RET

Star:

    ds *
