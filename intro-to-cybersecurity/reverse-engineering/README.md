# Program Structure and Stack Fundamentals

## Program Structure

A program is typically organized into multiple layers:

```text
Program
└── Modules
    └── Functions
        └── Blocks of Instructions
```

- **Modules** organize related functionality.
- **Functions** encapsulate reusable logic.
- **Instruction blocks** contain the machine-level operations executed by the CPU.

---

# Function Execution

Most functions follow a standard structure:

1. **Prologue**
   - Sets up the stack frame
   - Preserves caller state
   - Allocates local stack space

2. **Function Body**
   - Executes program logic

3. **Epilogue**
   - Restores previous stack state
   - Returns execution to the caller

---

# The Stack

The stack is a region of memory used for:
- local variables
- function arguments
- environment variables
- return addresses
- saved registers

The stack grows downward in memory.

```text
push -> rsp decreases
pop  -> rsp increases
```

On x86-64 systems:

```text
push -> rsp -= 8
pop  -> rsp += 8
```

because stack entries are typically 8 bytes wide.

---

# Function Calls and Return Addresses

When a function is called:

1. The CPU automatically pushes the return address onto the stack.
2. Execution jumps to the called function.
3. When the function returns, the saved return address is popped from the stack.
4. Execution resumes at the original call site.

---

# Stack Frames

Each function creates its own stack frame.

## Important Registers

| Register | Purpose |
|---|---|
| `rsp` | Stack Pointer — points to the top of the stack |
| `rbp` | Base Pointer — references the current stack frame |

---

# Function Prologue

Typical x86-64 function prologue:

```asm
push rbp
mov rbp, rsp
sub rsp, <size>
```

Purpose:
- save the caller's base pointer
- establish a new stack frame
- allocate local stack space

---

# Function Epilogue

Typical x86-64 function epilogue:

```asm
mov rsp, rbp
pop rbp
ret
```

Purpose:
- deallocate local stack space
- restore the previous stack frame
- return execution to the caller

---

# Debugging and Tracing Tools

## `ltrace`

Traces library calls made by a program.

Useful for observing:
- `printf`
- `strcmp`
- `malloc`
- libc behavior

Example:

```bash
ltrace ./program
```

---

## `strace`

Traces system calls made by a program.

Useful for observing:
- `open`
- `read`
- `write`
- `execve`
- filesystem and kernel interaction

Example:

```bash
strace ./program
```
