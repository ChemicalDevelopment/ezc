# Quick Start

First, [install](/#/installing) EZC.

Now, there are a few ways to use ezc

## File

You can create files and compile those to runnable executables.

For example, open `~/Documents/`, and create a file called `test.ezc` inside it.

Now, write this:

``` bash
prec $1
x = prompt 'Enter a number'
printf 'The square root of your number is \n'
var (sqrt x)
```


<button class="btn" data-clipboard-text="prec $1
x = prompt 'Enter a number'
printf 'The square root of your number is \n'
var (sqrt x)">
    Copy to clipboard
</button>


Now, back in your terminal, make sure you are in the same directory as the file you've created, and run (when it asks for a number, type one and hit `Enter`)

``` bash
 $ ezcc test.ezc -o test.o -v5
   > EZCC
    > Version: X.X.X
    > Date: 20XX-01-26 21:12:21 -0500

  > Authors
    > Cade Brown <cade@cade.site>

  > Compiling
    > cc  /tmp/rpthB.c -lm  -lmpfr -lgmp  -o test.o

 $ ./test.o
 Enter a number: 2 <Enter>
 The square root of your number is 1.41421356237309504879
```

## Passing as an argument

You don't need a file to compile, use:

``` bash
 $ ezcc -c "var (sqrt 2)"
 1.41421356237309504879
```

This compiles whatever you put right after the `-c` argument, and then executes it, showing you the result.

This is good for quick prototyping.

# Utilities

Now, to see what all utilities you have, run:

```bash
 $ cd ~/ezc/
 $ ls
```

These utilities, like `add`, are commandline based, so you don't have to compile them.

You use them like so (typing in lines that start with `$` into terminal):


```bash
 $ ./add 2 3
 5.00000000000000000000
 $ ./sqrt 2
 1.41421356237309504879
 $ ./sqrt 2 100
 1.4142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727
 $ ./pi 
 3.14159265358979323846
 $ ./pi 100
 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170678
```

So, for each utilities (ran with `./NAME`), you can also put an argument after the last one to set the number of digits.

If you'd like to set a precision at once:

```bash
 $ export EZC_PREC=100
```