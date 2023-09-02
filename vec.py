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
 def __truediv__(self, s: int|float):
  return Vector(self.x/s,self.y/s)


if __name__=='__main__':
 a=Vector(1,2)
 b=Vector(2,3)
 print(a+b)
 a+=b
 print(a)
 print(b*1.5)
 print(a*2)
