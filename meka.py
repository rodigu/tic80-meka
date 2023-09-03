# title:   MEKA
# author:  https://cohost.org/digo
# desc:    Armored Core de-make
# site:    https://github.com/rodigu
# license: MIT License (change this to your license of choice)
# version: 0.1
# script:  python
import math
import random

F=0

def TIC():
 global F
 global G
 G.curr_state(F)
 F+=1

class Particles:
 def __init__(self, count: int, idx: int, behavior: callable):
  self.particles:list["Particle"]=[Particle(Vectic(0,0), 0, idx, behavior) for _ in range(count)]
  self.curr_reset=0
 def drw(self):
  for p in self.particles:
   if p.life > 0:
    p.drw()
    p.behavior(p)
    p.life-=1
 def reset_particle(self, life:int, origin: "Vectic"):
  self.particles[self.curr_reset].life=life
  self.particles[self.curr_reset].pos=Vectic(origin.x, origin.y)
  self.curr_reset=(self.curr_reset+1)%len(self.particles)
 def scatter(part: "Particle"):
  part.pos+=Vectic(random.randint(-1,1)/3,random.randint(-1,1)/3)
 
class Particle:
 def __init__(self, pos: "Vectic", life: int, idx: int, behavior: callable):
  self.pos=pos
  self.life=life
  self.idx=idx
  self.behavior=behavior
 def drw(self):
  spr(self.idx, self.pos.x, self.pos.y, 0)

class K:
 def up()->bool:
  return key(23) or btn(0)
 def left()->bool:
  return key(1) or btn(2)
 def right()->bool:
  return key(4) or btn(3)
 def down()->bool:
  return key(19) or btn(1)
 def boost()->bool:
  return key(48) or key(64)

class Meka:
 def __init__(self, frame: "Frame", legs: "Leg", l: "Weapon", r: "Weapon", x=0, y=0):
  self.pos: Vectic=Vectic(x, y)
  self.frame=frame
  self.legs: "Leg"=legs
  self.l_w=l
  self.r_w=r
  self.moving=False
  self.dust=Particles(15,259,Particles.scatter)
  self.health=self.total_health()
 def total_health(self):
  return 5*self.frame.defense+2*self.legs.defense+self.l_w.defense+self.r_w.defense
 def drw(self, F):
  self.dust.drw()
  self.frame.drw_anim(1, F, self.pos, 0)
  if not self.moving: self.legs.drw(self.pos, 0)
  else: self.legs.drw_anim(0, F, self.pos, 0)
  self.l_w.drw_anim(0,F,self.pos, 0)
  self.r_w.drw_anim(0,F,self.pos, 0, 1, 1)
  self.move(F)
 def move(self, F):
  self.moving=False
  mv=Vectic(0,0)
  speed=self.legs.speed
  if K.boost() and self.frame.energy>0:
   self.frame.decrease_energy(self.legs.bst_cost)
   if self.frame.can_bst():
    sfx(48)
    speed=self.legs.bst_speed
    self.dust.reset_particle(20, self.pos)
  else:
   sfx(-1)
   self.frame.recover_energy()
  if K.up(): mv.y-=speed
  if K.down(): mv.y+=speed
  if K.left(): mv.x-=speed
  if K.right(): mv.x+=speed
  if mv!=Vectic.zero(): self.moving=True
  if mv.x!=0 and mv.y!=0: mv/=1.5
  self.pos+=mv
 def energy(self):
  return self.frame.energy
 def total_energy(self):
  return self.frame.total_energy

class Part:
 def __init__(self, d: int, idx: int, weight:int, clr: int):
  self.weight=weight
  self.defense=d
  self.idx=idx
  self.clr=clr
 def drw(self, pos: "Vectic", *args):
  pal(13,self.clr)
  spr(self.idx, pos.x, pos.y, *args)
  pal()
 def drw_anim(self, mod: int, F: int, pos: "Vectic", *args):
  pal(13,self.clr)
  spr(self.idx, pos.x, pos.y+math.sin(F/10+mod)-0.5, *args)
  pal()

class Frame(Part):
 def __init__(self, d: int, energy: int, weight: int, clr: int, recovery: int):
  super(Frame, self).__init__(d, 256, weight, clr)
  self.energy=energy
  self.total_energy=energy
  self.recovery=recovery
 def recover_energy(self):
  if self.energy>self.total_energy: self.energy=self.total_energy
  if self.energy==self.total_energy: return
  self.energy+=self.recovery
 def decrease_energy(self, amount:int):
  if self.energy<=0: return
  self.energy-=amount
 def can_bst(self):
  return self.energy>self.total_energy/5

class Weapon(Part):
 def __init__(self, d: int, typ: int, atk: int, weight: int, clr: int):
  super(Weapon, self).__init__(d, 258+typ*16, weight, clr)
  self.atk=atk

class Leg(Part):
 def __init__(self, d: int, typ: int, speed: int, weight: int, clr: int, bst_speed: int, bst_cost: int):
  super(Leg, self).__init__(d, 257+typ*3*16, weight, clr)
  self.speed=speed
  if bst_speed==0: bst_speed=1.5*speed
  self.bst_speed=bst_speed
  self.bst_cost=bst_cost
 def drw_anim(self, mod: int, F: int, pos: "Vectic", *args):
  pal(13,self.clr)
  spr(self.idx+16+(16 if F%20<10 else 0), pos.x, pos.y, *args)
  pal()

class Game:
 def __init__(self):
  self.player=Meka(Frame(1,50,1,2,2),Leg(1,0,0.4,1,2,1,1),Weapon(1,0,1,1,2),Weapon(1,0,1,1,2))
  self.curr_state=Game.create_game(self)
  self.curr_map=Vectic(0,0)
 def create_game(self):
  def g(F):
   cls(0)
   self.player.drw(F)
   self.drw_ui()
  return g
 def drw_map():
  cm=Game.curr_map
  map(cm.x,cm.y,cm.x+30,cm.y+17,0,0)
 def coord_to_map(v: "Vectic"):
  x=v.x//8
  y=v.y//8
  return x+Game.curr_map.x,y+Game.curr_map.y
 def flag_at(v: "Vectic"):
  idx=mget(v.x,v.y)
  flags={}
  for i in range(8):
   if fget(idx,i): flags[i]=True
  return flags
 def drw_ui(self):
  e=self.player.energy()
  total_e=self.player.total_energy()
  r_w=100
  rect(0,0,r_w*self.player.health/self.player.total_health(),5,2)
  rect(0,8,r_w*e/total_e,5,4)

class Vectic:
 def __init__(A,x,y):
  A.x=x
  A.y=y
 def __add__(A,v):return Vectic(v.x+A.x,v.y+A.y)
 def __iadd__(A,v):
  A.x+=v.x
  A.y+=v.y
  return A
 def __sub__(A,v):return Vectic(A.x-v.x,A.y-v.y)
 def __isub__(A,v):
  A.x-=v.x
  A.y-=v.y
  return A
 def __mul__(A,s):return Vectic(A.x*s,A.y*s)
 def __imul__(A,s):
  A.x*=s
  A.y*=s
  return A
 def __repr__(A):return f"Vectic({A.x}, {A.y})"
 def __truediv__(A,s):
  if isinstance(s,Vectic):return Vectic(A.x/s.x,A.y/s.y)
  return Vectic(A.x/s,A.y/s)
 def __floordiv__(A,s):
  if isinstance(s,Vectic):return Vectic(A.x//s.x,A.y//s.y)
  return Vectic(A.x//s,A.y//s)
 def __floor__(A):return A//1
 def __len__(A):return A.norm()
 def __eq__(A,v):return A.x==v.x and A.y==v.y
 def dist(A,v):return math.sqrt(A.dist2(v))
 def dist2(A,v):return(A.x-v.x)**2+(A.y-v.y)**2
 def norm(A):return A.dist(Vectic.zero())
 def normalized(A):return A/A.norm()
 def rot(A,t):return Vectic(A.x*math.cos(t)-A.x*math.sin(t),A.y*math.sin(t)+A.y*math.cos(t))
 def copy(A):return Vectic(A.x,A.y)
 def zero():return Vectic(0,0)

def pal(c0=None,c1=None):
 if(c0==None and c1==None):
  for i in range(16):
   poke4(0x3FF0*2+i,i)
 else: poke4(0x3FF0*2+c0,c1)

G=Game()

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
# 003:00000000000000000000c00000000c0000c00000000c00000000000000000000
# 016:cc000000c000000000000000000c000000000000000000c000000cc000000000
# 017:00000000000000000000000000000000000000000000000000000d0000d00000
# 018:0000000000000000000000000d000000dd000000000000000000000000000000
# 019:000dd000000dd000000000000d0dd0d0dd0dd0dd0d0dd0d00000000000dddd00
# 032:000000000cc000000c000000000c000000000c000000cc000000000000000000
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
# 000:020002000200020002000200020002000200020002000200020002000200020002000200020002000200020002000200020002000200020002000200102000000000
# 048:932ba33bb33cb33cb34dd34ce35df35df35de35ee35ee36fe36fe36de360e370e371e372e372d383d384d384d386c387c387c386b386c386b386c386107000000000
# </SFX>

# <PATTERNS>
# 000:800002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 001:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e00002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 002:d00002000000000000700002000000000000900002000000000000b00002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 003:800002000000000000d00002000000000000600002000000b00002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# </PATTERNS>

# <TRACKS>
# 000:1800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002300ff
# </TRACKS>

# <PALETTE>
# 000:1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57
# </PALETTE>

