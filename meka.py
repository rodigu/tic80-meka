# title:   MEKA
# author:  https://cohost.org/digo
# desc:    Armored Core de-make
# site:    https://github.com/rodigu
# license: MIT License (change this to your license of choice)
# version: 0.1
# script:  python
import math

F=0
S=lambda _:_

def TIC():
 global F
 global S
 S(F)
 F+=1

class K:
 up=23
 left=1
 right=4
 down=19
 shift=64

class Meka:
 def __init__(self, m: list["Part"], x=0, y=0):
  self.pos: Vector=Vector(x, y)
  self.frame=m[0]
  self.legs: "Leg"=m[1]
  self.l_w=m[2]
  self.r_w=m[3]
  self.moving=False
 def drw(self, F):
  self.frame.drw_anim(1, F, self.pos, 0)
  if not self.moving: self.legs.drw(self.pos, 0)
  else: self.legs.drw_anim(0, F, self.pos, 0)
  self.l_w.drw_anim(0,F,self.pos, 0)
  self.r_w.drw_anim(0,F,self.pos, 0, 1, 1)
  self.move(F)
 def move(self, F):
  self.moving=False
  mv=Vector(0,0)
  speed=self.legs.speed
  if key(K.shift): speed=self.legs.bst_speed
  if key(K.up): mv.y-=speed
  if key(K.down): mv.y+=speed
  if key(K.left): mv.x-=speed
  if key(K.right): mv.x+=speed
  if mv==Vector.zero(): self.moving=True
  if mv.x!=0 and mv.y!=0: mv/=1.5
  self.pos+=mv

class Part:
 def __init__(self, d: int, idx: int, weight:int, clr: int, energy=10):
  self.weight=weight
  self.defense=d
  self.idx=idx
  self.clr=clr
  self.energy=energy
 def drw(self, pos: "Vector", *args):
  pal(13,self.clr)
  spr(self.idx, pos.x, pos.y, *args)
  pal()
 def drw_anim(self, mod: int, F: int, pos: "Vector", *args):
  pal(13,self.clr)
  spr(self.idx, pos.x, pos.y+math.sin(F/10+mod)-0.5, *args)
  pal()

class Leg(Part):
 def __init__(self, d: int, typ: int, speed: int, weight: int, clr: int, bst_speed: int=0):
  super(Leg, self).__init__(d, 257+typ*3*16, weight, clr)
  self.speed=speed
  if bst_speed==0: bst_speed=1.5*speed
  self.bst_speed=bst_speed
 def drw_anim(self, mod: int, F: int, pos: "Vector", *args):
  pal(13,self.clr)
  spr(self.idx+16+(16 if F%20<10 else 0), pos.x, pos.y, *args)
  pal()

class Vector:
 def __init__(self, x:int, y:int):
  self.x=x
  self.y=y
 def __add__(self, v: "Vector"):
  return Vector(v.x+self.x, v.y+self.y)
 def __iadd__(self, v: "Vector"):
  self.x+=v.x
  self.y+=v.y
  return self
 def __sub__(self, v: "Vector"):
  return Vector(self.x-v.x,self.y-v.y)
 def __isub__(self, v: "Vector"):
  self.x-=v.x
  self.y-=v.y
  return self
 def __mul__(self, s: int|float):
  return Vector(self.x*s, self.y*s)
 def __imul__(self, s: int|float):
  self.x*=s
  self.y*=s
  return self
 def __repr__(self):
  return f"Vector({self.x}, {self.y})"
 def __truediv__(self, s):
  if isinstance(s,Vector):
   return Vector(self.x/s.x, self.y/s.y)
  return Vector(self.x/s,self.y/s)
 def __floordiv__(self, s):
  if isinstance(s,Vector):
   return Vector(self.x//s.x, self.y//s.y)
  return Vector(self.x//s,self.y//s)
 def __floor__(self):
  return self//1
 def __len__(self):
  return self.norm()
 def __eq__(self, v: "Vector"):
  return self.x==v.x and self.y==v.y
 def dist(self, v: "Vector"):
  return math.sqrt(self.dist2(v))
 def dist2(self, v: "Vector"):
  return (self.x-v.x)**2 +(self.y-v.y)**2
 def norm(self):
  return self.dist(Vector.zero())
 def normalized(self):
  return self / self.norm()
 def rot(self,t: int|float):
  return Vector(self.x*math.cos(t)-self.x*math.sin(t), self.y*math.sin(t)+self.y*math.cos(t))
 def zero():
  return Vector(0,0)
 
def create_game():
  m1=Meka([Part(1,256,1,2),Leg(1,0,0.4,1,2),Part(1,258,1,2),Part(1,258,1,2)])
  def g(F):
   cls(0)
   m1.drw(F)
  return g

S=create_game()

def pal(c0=None,c1=None):
 if(c0==None and c1==None):
  for i in range(16):
   poke4(0x3FF0*2+i,i)
 else: poke4(0x3FF0*2+c0,c1)


# <TILES>
# 204:ddddddd0d00000d0d00200d0d00200d0d00200d0d00000d0d00000d0d00000d0
# 205:ddddddd0d00000d0d0000000d0222000d0000000d0000000d00000d0ddddddd0
# 206:d00000d0d00000d0d020dd00d0200000d020dd00d00000d0d00000d0d00000d0
# 207:ddddddd0d00000d0d00000d0d00000d0d02220d0d00000d0d00000d0d00000d0
# </TILES>

# <SPRITES>
# 000:000dd000000dd00000000000000dd000000dd000000dd0000000000000000000
# 001:0000000000000000000000000000000000000000000000000000000000d00d00
# 002:0000000000000000000000000d0000000d000000000000000000000000000000
# 017:00000000000000000000000000000000000000000000000000000d0000d00000
# 018:0000000000000000000000000d000000dd000000000000000000000000000000
# 019:000dd000000dd000000000000d0dd0d0dd0dd0dd0d0dd0d00000000000dddd00
# 033:00000000000000000000000000000000000000000000000000d0000000000d00
# 034:0000000000000000dd0000000d0000000d000000000000000000000000000000
# 049:0000000000000000000000000000000000000000000000000000000000dddd00
# 050:0000000000000000d00000000d0000000d000000000000000000000000000000
# 065:00000000000000000000000000000000000000000000000000000000000ddd00
# 066:000000000d000000d00000000d0000000d000000000000000000000000000000
# 081:0000000000000000000000000000000000000000000000000000000000ddd000
# 082:000000000d000000dd0000000d0000000d000000000000000000000000000000
# 097:00000000000000000000000000000000000000000000000000d00d0000d00d00
# 098:00000000d0000000d00000000d0000000d000000000000000000000000000000
# 113:00000000000000000000000000000000000000000000000000d00d0000000d00
# 114:0000000000000000000000000d000000dd0000000d0000000000000000000000
# 129:00000000000000000000000000000000000000000000000000d00d0000d00000
# </SPRITES>

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

