# title:   MEKA
# author:  https://cohost.org/digo
# desc:    Armored Core de-make
# site:    https://github.com/rodigu
# license: MIT License (change this to your license of choice)
# version: 0.1
# script:  python

t=0
x=96
y=24

def TIC():
 global t
 global x
 global y

 if btn(0): y-=1
 if btn(1): y+=1
 if btn(2): x-=1
 if btn(3): x+=1

 cls(13)
 spr(
  1+t%60//30*2,
  x,y,
  colorkey=14,
  scale=3,
  w=2,h=2
 )
 print("HELLO WORLD!",84,84)
 t+=1


class Meka:
 def __init__(self, m: list[int]):
  
  self.frame=m[0]
  self.legs=m[1]
  self.l_w=m[2]
  self.r_w=m[3]
 
 def drw(self):
  
  pass


# <TILES>
# 001:eccccccccc888888caaaaaaaca888888cacccccccacc0ccccacc0ccccacc0ccc
# 002:ccccceee8888cceeaaaa0cee888a0ceeccca0ccc0cca0c0c0cca0c0c0cca0c0c
# 003:eccccccccc888888caaaaaaaca888888cacccccccacccccccacc0ccccacc0ccc
# 004:ccccceee8888cceeaaaa0cee888a0ceeccca0cccccca0c0c0cca0c0c0cca0c0c
# 017:cacccccccaaaaaaacaaacaaacaaaaccccaaaaaaac8888888cc000cccecccccec
# 018:ccca00ccaaaa0ccecaaa0ceeaaaa0ceeaaaa0cee8888ccee000cceeecccceeee
# 019:cacccccccaaaaaaacaaacaaacaaaaccccaaaaaaac8888888cc000cccecccccec
# 020:ccca00ccaaaa0ccecaaa0ceeaaaa0ceeaaaa0cee8888ccee000cceeecccceeee
# </TILES>

# <WAVES>
# 000:00000000ffffffff00000000ffffffff
# 001:0123456789abcdeffedcba9876543210
# 002:0123456789abcdef0123456789abcdef
# </WAVES>

# <SFX>
# 000:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000304000000000
# </SFX>

# <TRACKS>
# 000:100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# </TRACKS>

# <PALETTE>
# 000:1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57
# </PALETTE>

