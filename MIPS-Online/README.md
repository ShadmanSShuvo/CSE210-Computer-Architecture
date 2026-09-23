# MIPS Online Exam Solutions (CSE 210)

This directory contains MIPS assembly solutions, analysis, and C-to-MIPS translation references for the **CSE 210 Computer Architecture Sessional MIPS Online Evaluation** at BUET.

---

## 📑 Contents

- [Overview & Exam Context](#overview--exam-context)
- [Section B — `splitScore`](#section-b--splitscore)
- [Section C — `arrayScore`](#section-c--arrayscore)
- [Section A — `arrayScore`](#section-a--arrayscore)
- [Quick Mapping Reference](#quick-mapping-you-should-memorize-for-the-quiz)
- [Key Exam Takeaways & Stack Conventions](#key-exam-takeaways--stack-conventions)
- [File Manifest](#file-manifest)

---

## 🔍 Overview & Exam Context

The MIPS online evaluation tests students' proficiency in translating recursive C procedures into standard 32-bit MIPS assembly. Key evaluated concepts include:
1. **Stack Frame Management:** Allocating stack space with `$sp`, preserving `$ra`, saving argument registers (`$a0-$a3`), and saving local variables across recursive calls.
2. **Base Condition & Branching:** Accurate translation of conditional statements and termination logic.
3. **Array Indexing & Pointer Arithmetic:** Byte-addressable word alignment using `sll $reg, $index, 2` followed by adding base address.
4. **Return Value Conventions:** Passing results via `$v0` and cleaning up stack frames before `jr $ra`.

---

## Section B — `splitScore`

C function:

```c
int splitScore(int *A, int low, int high, int bias) {
    if (high < low) return 0;

    if (high != low) {
        if (A[low] != bias)
            return A[low];
        else
            return -A[low];
    }

    int mid = (low + high) / 2;
    int left = splitScore(A, low, mid, bias);
    int right = splitScore(A, mid + 1, high, bias);

    return left + right + A[mid];
}
```

The corresponding MIPS procedure:

```asm
# ------------------------------------------------
# int splitScore(int *A, int low, int high, int bias)
#
# Arguments:
#   $a0 = A
#   $a1 = low
#   $a2 = high
#   $a3 = bias
#
# Return:
#   $v0 = result
# ------------------------------------------------

splitScore:

    # Stack frame
    addi $sp, $sp, -24
    sw   $ra, 20($sp)
    sw   $a0, 16($sp)
    sw   $a1, 12($sp)
    sw   $a2, 8($sp)
    sw   $a3, 4($sp)

    # if (high < low) return 0
    slt  $t0, $a2, $a1
    bne  $t0, $zero, split_base

    # if (high != low)
    bne  $a2, $a1, high_not_low

    # mid = (low + high) / 2
    add  $t1, $a1, $a2
    sra  $t1, $t1, 1          # mid

    # left = splitScore(A, low, mid, bias)
    move $a0, $a0
    move $a1, $a1
    move $a2, $t1
    move $a3, $a3
    jal  splitScore

    # save left
    sw   $v0, 0($sp)

    # right = splitScore(A, mid+1, high, bias)
    lw   $a0, 16($sp)
    lw   $a1, 12($sp)
    lw   $a2, 8($sp)
    lw   $a3, 4($sp)

    addi $a1, $t1, 1
    jal  splitScore

    # left + right
    lw   $t2, 0($sp)
    add  $v0, $t2, $v0

    # + A[mid]
    lw   $a0, 16($sp)
    sll  $t3, $t1, 2
    add  $t3, $a0, $t3
    lw   $t4, 0($t3)

    add  $v0, $v0, $t4
    j    split_exit


# --------------------------------
# if (high != low)
# --------------------------------
high_not_low:

    # address of A[low]
    sll  $t0, $a1, 2
    add  $t0, $a0, $t0
    lw   $t1, 0($t0)

    # if (A[low] != bias)
    bne  $t1, $a3, return_array_low

    # return -A[low]
    sub  $v0, $zero, $t1
    j    split_exit


return_array_low:

    move $v0, $t1
    j    split_exit


# --------------------------------
# return 0
# --------------------------------
split_base:

    li   $v0, 0


split_exit:

    lw   $ra, 20($sp)
    lw   $a0, 16($sp)
    lw   $a1, 12($sp)
    lw   $a2, 8($sp)
    lw   $a3, 4($sp)

    addi $sp, $sp, 24
    jr   $ra
```

---

## Section C — `arrayScore`

The paper gives:

```c
int arrayScore(int A[], int low, int high){
    if (low > high) return 0;

    int sum = 0;

    for(int i = low; i != high; i++) {
        sum += A[i] * (i - low + 1);
    }

    int left = arrayScore(A, low-1, high);
    int right = arrayScore(A, low, high+1);

    return left - right + sum + A[low] + A[high];
}
```

### MIPS Translation

```asm
# ------------------------------------------------
# int arrayScore(int A[], int low, int high)
#
# $a0 = A
# $a1 = low
# $a2 = high
# $v0 = result
# ------------------------------------------------

arrayScore:

    addi $sp, $sp, -32

    sw   $ra, 28($sp)
    sw   $a0, 24($sp)
    sw   $a1, 20($sp)
    sw   $a2, 16($sp)

    # if (low > high) return 0
    slt  $t0, $a2, $a1
    bne  $t0, $zero, array_base

    # sum = 0
    li   $t0, 0

    # i = low
    move $t1, $a1

array_loop:

    # while (i != high)
    beq  $t1, $a2, array_loop_done

    # A[i]
    sll  $t2, $t1, 2
    add  $t2, $a0, $t2
    lw   $t3, 0($t2)

    # (i - low + 1)
    sub  $t4, $t1, $a1
    addi $t4, $t4, 1

    # A[i] * (i-low+1)
    mul  $t5, $t3, $t4

    # sum += ...
    add  $t0, $t0, $t5

    # i++
    addi $t1, $t1, 1

    j    array_loop


array_loop_done:

    # Save sum
    sw   $t0, 12($sp)

    # --------------------------------
    # left = arrayScore(A, low-1, high)
    # --------------------------------

    lw   $a0, 24($sp)
    lw   $a1, 20($sp)
    lw   $a2, 16($sp)

    addi $a1, $a1, -1

    jal  arrayScore

    # Save left
    sw   $v0, 8($sp)

    # --------------------------------
    # right = arrayScore(A, low, high+1)
    # --------------------------------

    lw   $a0, 24($sp)
    lw   $a1, 20($sp)
    lw   $a2, 16($sp)

    addi $a2, $a2, 1

    jal  arrayScore

    # --------------------------------
    # left - right
    # --------------------------------

    lw   $t0, 8($sp)
    sub  $v0, $t0, $v0

    # + sum
    lw   $t1, 12($sp)
    add  $v0, $v0, $t1

    # --------------------------------
    # + A[low]
    # --------------------------------

    lw   $a0, 24($sp)
    lw   $a1, 20($sp)

    sll  $t2, $a1, 2
    add  $t2, $a0, $t2
    lw   $t3, 0($t2)

    add  $v0, $v0, $t3

    # --------------------------------
    # + A[high]
    # --------------------------------

    lw   $a2, 16($sp)

    sll  $t2, $a2, 2
    add  $t2, $a0, $t2
    lw   $t3, 0($t2)

    add  $v0, $v0, $t3

    j    array_exit


array_base:

    li   $v0, 0


array_exit:

    lw   $ra, 28($sp)
    lw   $a0, 24($sp)
    lw   $a1, 20($sp)
    lw   $a2, 16($sp)

    addi $sp, $sp, 32
    jr   $ra
```

> [!WARNING]
> **Issue in Section C Problem Statement:**
> As written in the original question PDF:
> ```c
> left  = arrayScore(A, low-1, high);
> right = arrayScore(A, low, high+1);
> ```
> Notice these recursive calls move **away** from the base termination condition `low > high`, causing non-termination or infinite stack consumption on normal inputs. This reflects a typo in the original question paper; the translation faithfully represents the written logic.

---

## Section A — `arrayScore`

The paper gives this structure:

```c
int arrayScore(int A[], int low, int high, int factor){
    if (low > high) return 0;

    int sum = 0;

    for(int i = low; i != high; i++) {

        if(A[i] > high){
            sum += A[i] * (i - low + 1);
        }

        else if(A[i] != low){
            sum += A[i] * i;
        }

        else{
            sum -= A[i] * factor;
        }
    }

    int mid = (low + high) / 2;

    int left = arrayScore(A, mid, high+1, factor-1);

    return left + sum + A[mid];
}
```

### MIPS Translation

```asm
# ------------------------------------------------
# int arrayScore(int A[], int low, int high, int factor)
#
# $a0 = A
# $a1 = low
# $a2 = high
# $a3 = factor
#
# $v0 = result
# ------------------------------------------------

arrayScoreA:

    addi $sp, $sp, -32

    sw   $ra, 28($sp)
    sw   $a0, 24($sp)
    sw   $a1, 20($sp)
    sw   $a2, 16($sp)
    sw   $a3, 12($sp)

    # if (low > high) return 0
    slt  $t0, $a2, $a1
    bne  $t0, $zero, A_base

    # sum = 0
    li   $t0, 0

    # i = low
    move $t1, $a1


A_loop:

    # i != high ?
    beq  $t1, $a2, A_loop_done

    # address of A[i]
    sll  $t2, $t1, 2
    add  $t2, $a0, $t2
    lw   $t3, 0($t2)

    # ----------------------------------------
    # if (A[i] > high)
    # ----------------------------------------

    slt  $t4, $a2, $t3

    bne  $t4, $zero, A_if


    # ----------------------------------------
    # else if (A[i] != low)
    # ----------------------------------------

    beq  $t3, $a1, A_else


    # sum += A[i] * i
    mul  $t4, $t3, $t1
    add  $t0, $t0, $t4

    j    A_increment


A_if:

    # (i - low + 1)
    sub  $t4, $t1, $a1
    addi $t4, $t4, 1

    # A[i] * (i-low+1)
    mul  $t4, $t3, $t4

    # sum += ...
    add  $t0, $t0, $t4

    j    A_increment


A_else:

    # A[i] * factor
    mul  $t4, $t3, $a3

    # sum -= ...
    sub  $t0, $t0, $t4


A_increment:

    # i++
    addi $t1, $t1, 1

    j    A_loop


A_loop_done:

    # save sum
    sw   $t0, 8($sp)

    # ----------------------------------------
    # mid = (low + high) / 2
    # ----------------------------------------

    add  $t1, $a1, $a2
    sra  $t1, $t1, 1

    # save mid
    sw   $t1, 4($sp)

    # ----------------------------------------
    # left =
    # arrayScore(A, mid, high+1, factor-1)
    # ----------------------------------------

    lw   $a0, 24($sp)

    move $a1, $t1

    lw   $a2, 16($sp)
    addi $a2, $a2, 1

    lw   $a3, 12($sp)
    addi $a3, $a3, -1

    jal  arrayScoreA

    # ----------------------------------------
    # left + sum
    # ----------------------------------------

    lw   $t0, 8($sp)
    add  $v0, $v0, $t0

    # ----------------------------------------
    # + A[mid]
    # ----------------------------------------

    lw   $a0, 24($sp)
    lw   $t1, 4($sp)

    sll  $t2, $t1, 2
    add  $t2, $a0, $t2
    lw   $t3, 0($t2)

    add  $v0, $v0, $t3

    j    A_exit


A_base:

    li   $v0, 0


A_exit:

    lw   $ra, 28($sp)
    lw   $a0, 24($sp)
    lw   $a1, 20($sp)
    lw   $a2, 16($sp)
    lw   $a3, 12($sp)

    addi $sp, $sp, 32
    jr   $ra
```

---

## Quick Mapping You Should Memorize for the Quiz

| C Operation | MIPS Assembly |
| :--- | :--- |
| `A[i]` (load) | `sll $t0, $i, 2`<br>`add $t0, $base, $t0`<br>`lw $tX, 0($t0)` |
| `A[i] = x` (store) | `sll $t0, $i, 2`<br>`add $t0, $base, $t0`<br>`sw $tX, 0($t0)` |
| `i++` | `addi $i, $i, 1` |
| `i--` | `addi $i, $i, -1` |
| `i * 4` | `sll $t, $i, 2` |
| `i / 2` | `sra $t, $i, 1` |
| `i > j` | `slt $t, $j, $i` |
| `i < j` | `slt $t, $i, $j` |
| `i == j` | `beq $i, $j, label` |
| `i != j` | `bne $i, $j, label` |
| `return x` | `move $v0, $x` |
| function call | `jal function` |
| return to caller | `jr $ra` |

---

## Key Exam Takeaways & Stack Conventions

> [!IMPORTANT]
> **Preserving Registers Across Calls:**
> Because all sections are recursive:
> 1. You **must save `$ra`** on the stack before issuing any `jal`. Without this, subsequent recursive calls overwrite your return address.
> 2. You **must save and reload argument registers (`$a0-$a3`)** if their values are reused after the child recursive call completes.
> 3. Always maintain 4-byte (word) stack alignment (stack pointer decrements should be multiples of 4 or 8, e.g., `-24`, `-32`).

---

## 📂 File Manifest

- [`MIPS_Online.pdf`](./MIPS_Online.pdf): Official problem question sheet for the MIPS online exam.
- [`README.md`](./README.md): Detailed write-up, C function breakdowns, and MIPS translations.
