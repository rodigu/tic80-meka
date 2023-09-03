from vec import Vectic
class Particles:
 def __init__(self, count: int, idx: int, behavior: callable):
  self.particles:list["Particle"]=[Particle(Vectic(0,0), 0, idx, behavior)]
 def drw(self, origin: Vectic):
  for p in self.particles:
   if p.life > 0:
    p.drw(origin)
    p.life-=1
 
class Particle:
 def __init__(self, pos: "Vectic", life: int, idx: int, behavior: callable):
  self.pos=pos
  self.life=life
  self.idx=idx
  self.behavior=behavior
 def drw(self, origin: Vectic):
  spr(self.idx, self.pos.x+origin.x, self.pos.y+origin.y, 0)
 