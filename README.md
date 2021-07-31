
# lazy-mathematician

If you are a lazy mathematician, this interpreter will help you

There are 4 main commands for this language:

 1. Print
 2. Direct quantification
 3. Computing
 4. End

## Print

If the variable name comes in the input alone, its value is calculated with exactly 3 decimal places. And if there is no such variable, the 

> variable not found

 is printed.

## Direct quantification

The value to the right of the symbol `:=`, which may be a number or another variable, is dropped in the variable to the left of this symbol. If the name of a variable that did not already exist is printed on the right, a 

> variable error

 is printed, and if the right numeric expression (`val`) is not correctly displayed, 

> `val` is not a number

 is printed.

 - An incorrect form for a numerical expression means that the
   expression starts with a number but has letters in it. For example
   
> 3.6d

## Computing

If the input is `a := function(b, c)`, it is a calculation operation. If the function name is not written in the supported functions 

> function not found

 is printed. And for each of `b` and `c`, which are function arguments, a 

> variable error

 is printed if the variable is not defined, and a 

> `val` is not a number

 is printed if it does not have a correct numeric shape (and is assumed to be `val`).
 
## End

If the input is at the `end`, the program ends.

 - The distance around the operator `=:` and the arguments of the function do not matter.
 - Commands 2 and 3 can be used to define a variable.
 - The variable name contains only letters and underscores (_).

---

**Functions supported**

 -  `add`: Add your two arguments.
 - `sub`: Subtracts the second argument from the first.
 - `mul`: Multiplies two arguments.
 - `div`: Divides the first argument by the second.
 - `pow`: Bring the first argument to the second power (available in the `math` library)
 - `gcd`: Returns the largest common denominator (available in the `math` library, and make sure that the inputs to this function are integers.)
 - `log`: The logarithm of the first argument is calculated based on the second argument (available in the `math` library)
 
 ---
 
**Example**

Sample input:

```undefined
a := 3.144
a
a := add(a,4)
a
b := sub(a,3)
b
b := gcd(b,3)
b
b := log(e,f)
end
```

Sample output:
```undefined
3.144
7.144
4.144
1.000
variable error
```

---

 - code.py -> Use regex
 - code2.py -> Use token and lexer for interpretation
