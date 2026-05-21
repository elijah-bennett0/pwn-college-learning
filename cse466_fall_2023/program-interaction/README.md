# ELF Loading, Process Initialization, and Linux Process Fundamentals

# Loading the Binary

## Reading the ELF Interpreter

The ELF interpreter (loader) used by a binary can be viewed with:

```bash
readelf -a /bin/cat | grep interpret
```

This returns the dynamic loader responsible for loading the binary.

Example:

```text
/lib64/ld-linux-x86-64.so.2
```

---

## Temporarily Overriding the Loader

A loader can be manually specified when launching a program:

```bash
/path/to/loader /path/to/binary
```

Example:

```bash
/lib64/ld-linux-x86-64.so.2 ./binary
```

---

## Permanently Changing the Loader

The interpreter can also be modified permanently using `patchelf`:

```bash
patchelf --set-interpreter /path/to/loader ./binary
```

---

# Linux Virtual Memory

Each Linux process receives its own virtual memory space.

Typical regions include:

- the program binary
- shared libraries
- heap (dynamic allocations)
- stack (local variables/function frames)
- memory-mapped regions
- helper regions
- kernel-space mappings inaccessible to user processes

---

## Virtual Memory vs Physical Memory

| Type | Description |
|---|---|
| Virtual Memory | Private address space assigned to a process |
| Physical Memory | Actual RAM shared across the system |

Process memory mappings can be viewed with:

```bash
cat /proc/self/maps
```

---

# The Standard C Library (`libc`)

Most Linux binaries dynamically link against:

```text
libc.so
```

`libc` provides common functionality such as:

- `printf`
- `scanf`
- `malloc`
- `free`
- `socket`
- `atoi`

and many other standard functions.

---

# Binary Initialization

## Constructors

ELF binaries may define constructors: functions that execute before `main()`.

Example:

```c
__attribute__((constructor))
void test() {
    puts("test");
}
```

Constructor functions are commonly used for:
- initialization logic
- setup routines
- library initialization

---

# Program Startup

Most dynamically linked ELF binaries eventually call:

```text
__libc_start_main()
```

inside `libc`, which then invokes the program's `main()` function.

---

## Typical `main()` Signature

```c
int main(int argc, void **argv, void **envp);
```

### Arguments

| Argument | Purpose |
|---|---|
| `argc` | Argument count |
| `argv` | Command-line arguments |
| `envp` | Environment variables |

---

# Program Input Sources

A process typically receives input from:

- loaded binaries/libraries
- command-line arguments
- environment variables
- files
- sockets
- stdin

---

# Syscalls

Programs interact with the operating system through system calls.

Examples:

- `open`
- `read`
- `write`
- `execve`

System calls can be traced using:

```bash
strace ./program
```

Documentation:

```bash
man 2 open
```

---

# Signals

Signals are asynchronous notifications sent by the operating system to a process.

Unlike syscalls:
- syscalls are requests *from the program to the OS*
- signals are notifications *from the OS to the program*

---

## Signal Handlers

Signals pause execution and invoke a signal handler function.

Example handler:

```c
void handler(int sig) {

}
```

If no custom handler exists, the default action is performed:
- terminate
- ignore
- stop
- continue

depending on the signal.

---

## Useful Signal Resources

```bash
man 7 signal
kill -l
```

---

# Common Syscall Patterns

Typical process interactions:

```text
fork -> execve -> wait
open -> read -> write
```

---

# Process Termination

A process terminates when it:

- receives an unhandled signal
- calls the `exit()` syscall

---

## Zombie Processes

After termination, a process remains in a zombie state until its parent calls:

```c
wait()
```

At that point:
- the exit code is collected
- kernel resources are released
- the process is fully cleaned up

---

# Notes on Child Processes

When using:
- `subprocess.Popen`
- `pwn.process`

ensure child processes are properly waited on.

Example:

```python
proc.wait()
```

Failing to do so may leave zombie processes behind.

---

# Debugging and Tracing Tools

| Tool | Purpose |
|---|---|
| `strace` | Trace system calls |
| `ltrace` | Trace library calls |
| `readelf` | Inspect ELF metadata |
| `patchelf` | Modify ELF interpreters/RPATH |
| `gdb` | Runtime debugging |
| `objdump` | Static disassembly |

---

# Resources

## C Socket Programming

https://www.binarytides.com/socket-programming-c-linux-tutorial/

---

## Using Pipes in C

https://jameshfisher.com/2017/02/17/how-do-i-call-a-program-in-c-with-pipes/

---

## Named FIFO Pipes

https://www.geeksforgeeks.org/cpp/named-pipe-fifo-example-c-program/

---

## UNIX I/O Redirection

https://web.archive.org/web/20220629044814/http://bencane.com:80/2012/04/16/unix-shell-the-art-of-io-redirection/

---

## Pwntools Cheatsheet

https://gist.github.com/anvbis/64907e4f90974c4bdd930baeb705dedf
