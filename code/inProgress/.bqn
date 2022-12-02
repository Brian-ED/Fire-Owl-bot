`?´ #https://mlochbaum.github.io/BQN/help/choose.html
?

~@#%^&*()_–+={}|\"',<>./
# left to right evaluation, right to left linking with ` and ´
    4+1_2_3
5_6_7
    1_2+3_4
4_6
    1_2_3\´+0 # / takes a function (+) and returns a function, ´ is for linking
6             # which is then applied to 1_2_3 and 0,
              # 0 being the start value for the reduce.

    1_2_3\´+  # some functions would have the default be built in.
6
    4!\´+     # ! is index generator. 4!→0 1 2 3 
6
    4_5$3_3         # Reshape
[4_5_4
 5_4_5
 4_5_4]

    4_5$3_3 : "x" # when given a string argument, : is define
[4_5_4
 5_4_5
 4_5_4]
    
    x ; 4_5$3_3 # ; is syntax to make assignment more readable
[4_5_4
 5_4_5
 4_5_4]

    x=[4_5_4      # = returns 1 if both left and right are the same.
       5_4_5      # if x is 1, error with code 1,
       4_5_4] !´1 # so !´ is assert.
                              
    3+`?´




# Stuff from K

Verbs:    : + - * % ! & | < > = ~ , ^ # _ $ ? @ . 0: 1:
notation: [c]har [i]nt [n]umber(int|float) [s]ymbol [a]tom [d]ict
          [f]unc(monad) [F]unc(dyad) [xyz]any
special:  var:y     set    a:1;a -> 1
          (v;..):y  unpack (b;(c;d)):(2 3;4 5);c -> 4
          :x        return {:x+1;2}[3] -> 4
          $[x;y;..] cond   $[0;`a;"\0";`b;`;`c;();`d;`e] -> `e
          o[..]     recur  {$[x<2;x;+/o'x-1 2]}9 -> 34
          [..]      progn  [0;1;2;3] -> 3

::  self      ::12 -> 12
 :  right     1 :2 -> 2   "abc":'"d" -> "ddd"
 +x flip      +("ab";"cd") -> ("ac";"bd")
N+N add       1 2+3 -> 4 5
 -N negate    - 1 2 -> -1 -2
N-N subtract  1-2 3 -> -1 -2
 *x first     *`a`b -> `a   *(0 1;"cd") -> 0 1
N*N multiply  1 2*3 4 -> 3 8
 %N sqrt      %25 -> 5.0   %-1 -> 0n
N%N divide    4 3%2 -> 2 1   4 3%2.0 -> 2.0 1.5
 !i enum      !3 -> 0 1 2   !-3 -> -3 -2 -1
 !I odometer  !2 3 -> (0 0 0 1 1 1;0 1 2 0 1 2)
 !d keys      !`a`b!0 1 -> `a`b
 !S ns keys   a.b.c:1;a.b.d:2;!`a`b -> ``c`d
x!y dict      `a`b!1 2 -> `a`b!1 2
i!I div       -10!1234 567 -> 123 56
i!I mod       10!1234 567 -> 4 7
 &I where     &3 -> 0 0 0   &1 0 1 4 2 -> 0 2 3 3 3 3 4 4
 &x deepwhere &(0 1 0;1 0 0;1 1 1) -> (0 1 2 2 2;1 0 0 1 2)
N&N min/and   2&-1 3 -> -1 2   0 0 1 1&0 1 0 1 -> 0 0 0 1
 |x reverse   |"abc" -> "cba"   |12 -> 12
N|N max/or    2|-1 3 -> 2 3   0 0 1 1|0 1 0 1 -> 0 1 1 1
 <X ascend    <"abacus" -> 0 2 1 3 5 4
 >X descend   >"abacus" -> 4 5 3 1 0 2
 <s open      fd:<`"/path/to/file.txt"
 >i close     >fd
N<N less      0 2<1 -> 1 0
N>N more      0 1>0 2 -> 0 0
 =X group     ="abracadabra" -> "abrcd"!(0 3 5 7 10;1 8;2 9;,4;,6)
 =i unitmat   =3 -> (1 0 0;0 1 0;0 0 1)
N=N equal     0 1 2=0 1 3 -> 1 1 0
 ~x not       ~(0 2;``a;"a \0";::;{}) -> (1 0;1 0;0 0 1;1;0)
x~y match     2 3~2 3 -> 1   "4"~4 -> 0   0~0.0 -> 0
 ,x enlist    ,0 -> ,0   ,0 1 -> ,0 1   ,`a!1 -> +(,`a)!,,1
x,y concat    0,1 2 -> 0 1 2  "a",1 -> ("a";1)
 ^x null      ^(" a";0 1 0N;``a;0.0 0n) -> (1 0;0 0 1;1 0;0 1)
a^y fill      1^0 0N 2 3 0N -> 0 1 2 3 1   "b"^" " -> "b"
X^y without   "abracadabra"^"bc" -> "araadara"
 #x length    #"abc" -> 3   #4 -> 1   #`a`b`c!0 1 0 -> 3
i#y reshape   3#2 -> 2 2 2
I#y reshape   2 3#` -> (```;```)
f#y replicate (3>#:')#(0;2 1 3;5 4) -> (0;5 4)   {2}#"ab" -> "aabb"
x#d take      `c`d`f#`a`b`c`d!1 2 3 4 -> `c`d`f!3 4 0N
 _n floor     _12.34 -12.34 -> 12 -13
 _c lowercase _"Ab" -> "ab"
i_Y drop      2_"abcde" -> "cde"   `b_`a`b`c!0 1 2 -> `a`c!0 2
I_Y cut       2 4 4_"abcde" -> ("cd";"";,"e")
f_Y weed out  (3>#:')_(0;2 1 3;5 4) -> ,2 1 3
X_i delete    "abcde"_2 -> "abde"
 $x string    $(12;"ab";`cd;+) -> ("12";(,"a";,"b");"cd";,"+")
i$C pad       5$"abc" -> "abc  "   -3$"a" -> "  a"
s$y cast      `c$97 -> "a"   `i$-1.2 -> -1   `$"a" -> `a
s$y int       `I$"-12" -> -12
 ?x uniq      ?"abacus" -> "abcus"
X?y find      "abcde"?"bfe" -> 1 0N 4
i?x roll      3?1000 -> 11 398 293   1?0 -> ,-8164324247243690787
i?x deal      -3?1000 -> 11 398 293 /guaranteed distinct
 @x type      @1 -> `b   @"ab" -> `C   @() -> `A   @(@) -> `v
x@y apply(1)  {x+1}@2 -> 3   "abc"@1 -> "b"   (`a`b!0 1)@`b -> 1
 .S get       a:1;.`a -> 1   b.c:2;.`b`c -> 2
 .C eval      ."1+2" -> 3
 .d values    .`a`b!0 1 -> 0 1
x.y apply(n)  {x*y+1}. 2 3 -> 8   (`a`b`c;`d`e`f). 1 0 -> `d

@[x;y;f]   amend  @["ABC";1;_:] -> "AbC"   @[2 3;1;{-x}] -> 2 -3
@[x;y;F;z] amend  @["abc";1;:;"x"] -> "axc"   @[2 3;0;+;4] -> 6 3
.[x;y;f]   drill  .[("AB";"CD");1 0;_:] -> ("AB";"cD")
.[x;y;F;z] drill  .[("ab";"cd");1 0;:;"x"] -> ("ab";"xd")
.[f;y;f]   try    .[+;1 2;"E:",] -> 3   .[+;1,`2;"E:",] -> "E:typ"
?[x;y;z]   splice ?["abcd";1 3;"xyz"] -> "axyzd"