; Combine printstr.ls8 and keyboard.ls8 to print an instruction
; before starting text editor.
    LDI R0,Start
    CALL R0
    LDI R0, Keyboard
    CALL R0

; The most simple of text editors!
;
; Declares a subroutine that prints a string at a given address
;
; Expected output: Press [esc] to quit.
Start:

	LDI R0,Instruct      ; address of "Hello, world!" bytes
	LDI R1,22            ; number of bytes to print
	LDI R2,PrintStr      ; address of PrintStr
	CALL R2              ; call PrintStr
	RET                  ; halt

; Subroutine: PrintStr
; R0 the address of the string
; R1 the number of bytes to print

PrintStr:

	LDI R2,0            ; SAVE 0 into R2 for later CMP

PrintStrLoop:

	CMP R1,R2           ; Compare R1 to 0 (in R2)
	LDI R3,PrintStrEnd  ; Jump to end if we're done
	JEQ R3

	LD R3,R0            ; Load R3 from address in R0
	PRA R3              ; Print character

	INC R0              ; Increment pointer to next character
	DEC R1              ; Decrement number of characters

	LDI R3,PrintStrLoop ; Keep processing
	JMP R3

PrintStrEnd:

	RET                 ; Return to caller

; Start of printable data

Instruct:

	ds Press [esc] to quit.
	db 0x0a       ; newline
	db 0x0a       ; newline


Keyboard:

; A simple program to test the keyboard and echo to console.
;
; Does not interpret anything; CR just moves the cursor to the start of the
; line, BS doesn't work, etc.

; Hook the keyboard interrupt

    LDI R0,0xF9          ; R0 holds the interrupt vector for I1 (keyboard)
    LDI R1,IntHandler    ; R1 holds the address of the handler
    ST R0,R1             ; Store handler addr in int vector
    LDI R5,2             ; Enable keyboard interrupts
    LDI R0,Loop
Loop:
    JMP R0               ; Infinite spin loop

; Interrupt handler
IntHandler:
    LDI R0,0xF4          ; Memory location of most recent key pressed
    LD R1,R0             ; load R1 from that memory address
    PRA R1               ; Print it
    IRET