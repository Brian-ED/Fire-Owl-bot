import numpy as np 

# ↩≠≍˘⁼⌜˝≤⍉⌊↓↕∊𝕗𝕘⊸⊏∘○⟜≡⊐π⌽↑𝕤∧⊔∨𝕨𝕩⥊×˜←· ˙√⇐⟩⎉⚇⍟◶⊘⎊≥⌈⍷𝔽𝔾«⊑⌾»≢⊒⍳𝕣𝕊⍋⍒𝕎𝕏⋈⊢⊣


from numpy import concatenate as Join # ∾
def Add(x,y):return np.add(x,y)       # +

# -
def Minus(*x):
    if len(x)==1:
        r=np.negative(*x)
    elif len(x)==2:
        r=np.subtract(*x)
    return r

def Not(x):return np.invert(x)        # ¬
def Divide(x,y):return np.divide(x,y) # ÷
def Multiply(x,y):return np.multiply(x,y) # ×

# ⥊
def Reshape(*x):
    flat=np.reshape(x[0],-1)
    if len(x)==1:
        r=flat
    elif len(x)==2:
        r=np.reshape(flat,x[1])
    else: '1'
    return r




x=np.array(((1,2,3),(4,5,6),(7,8,9)))

print(np.concatenate((x,x,x)))