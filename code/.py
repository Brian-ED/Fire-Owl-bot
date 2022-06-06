from pynapl import APL
apl=APL.APL()

d = [['replywith:','Responses'],['reactwith:','Reacts']]
dfn=apl.fn("{y x←⊃⍸⍺∘.≡⊃¨⍵⋄(⊂x⊃⊃∘⌽¨⍵),⍨¯1 0{|⍺:⍺⎕C⍵⋄⍵}¨{1↓∊' ',⍪⍵}¨⍺⊆⍨0@y⊢1⍴⍨≢⍺}")
KeyStr,ValStr,k=dfn(args[1:],d)
if ValStr: data[123][k][KeyStr]=ValStr
