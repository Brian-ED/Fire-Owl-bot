from pynapl import APL
apl=APL.APL()
apl.eval("""
         ⎕FIX 'file://C:/Users/brian/Persinal/discBots/Fire-Owl-bot/code/dyalog-safe-exec/Safe.dyalog'
         ns←⎕NS ⍬
         """)
APLSafeEval=apl.fn("{1 ns Safe.Exec ⍵}")

print(APLSafeEval('100+111+1 2 3 4'))
