from vec import Vectic
import random

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
  part.pos+=Vectic(random.randint(-1,1),random.randint(-1,1))
 
class Particle:
 def __init__(self, pos: "Vectic", life: int, idx: int, behavior: callable):
  self.pos=pos
  self.life=life
  self.idx=idx
  self.behavior=behavior
 def drw(self):
  spr(self.idx, self.pos.x, self.pos.y, 0)