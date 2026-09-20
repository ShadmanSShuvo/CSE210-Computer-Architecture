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

# Section C — `arrayScore`

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

### MIPS

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

### ⚠️ Important issue with Section C

As written in the PDF:

```c
left  = arrayScore(A, low-1, high);
right = arrayScore(A, low, high+1);
```

these recursive calls move **away from the base condition** `low > high`. So for normal inputs, this does not terminate. The PDF may contain an error/formatting corruption here.

Don't memorize the recursive logic of C until you confirm the original question.

---

# Section A — `arrayScore`

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

### MIPS

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

## Quick mapping you should memorize for the quiz

| C             | MIPS                     |
| ------------- | ------------------------ |
| `A[i]`        | `lw $tX, 0($base + i*4)` |
| `A[i] = x`    | `sw $tX, 0($base + i*4)` |
| `i++`         | `addi $i, $i, 1`         |
| `i--`         | `addi $i, $i, -1`        |
| `i * 4`       | `sll $t, $i, 2`          |
| `i / 2`       | `sra $t, $i, 1`          |
| `i > j`       | `slt $t, $j, $i`         |
| `i < j`       | `slt $t, $i, $j`         |
| `i == j`      | `beq $i, $j, label`      |
| `i != j`      | `bne $i, $j, label`      |
| `return x`    | `move $v0, $x`           |
| function call | `jal function`           |
| return        | `jr $ra`                 |

**One important exam point:** because A and B are recursive, you **must save `$ra` and the arguments on the stack** before making another `jal`. Otherwise the recursive calls overwrite the return address.
