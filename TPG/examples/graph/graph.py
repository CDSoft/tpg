#!/usr/bin/python

from Tkinter import *
from TPG import *
from math import cos,sin,tan,acos,asin,atan,sqrt

class Graph(Frame):

	def __init__(self, name, env, cmds, master=None):
		Frame.__init__(self, master)
		self.env = env
		self.master.title("Grapher - %s"%name)
		self.master.minsize(env.XMAX,env.YMAX+30)
		self.master.maxsize(env.XMAX,env.YMAX+30)
		self.w = Canvas(self, width=env.XMAX, height=env.YMAX)
		self.w.pack(fill='x')
		for obj in cmds.objects():
			obj.trace(self.w)
		self.pack()
		quit = Button(self, text="Quit", command=self.quit)
		quit.pack(fill='x')
		quit.focus_set()

class Commands(Node):
	
	def objects(self):
		objs = []
		for cmd in self:
			objs = objs + cmd.objects()
		objs.sort()
		return objs

class Idents(Node):
	pass

class Ident(Node):
	
	def name(self):
		return self[0]

	def val(self):
		e = self.env.getVar(self)
		if e==None: return 0
		return e.val()

class Repere(Node):
	def init(self, color, x_range, y_range, z_range):
		self.color, self.xrange, self.yrange, self.zrange = color, x_range, y_range, z_range
		self.xmin, self.xmax = self.xrange.minmax()
		self.xstep = self.xrange.step()
		self.ymin, self.ymax = self.yrange.minmax()
		self.ystep = self.yrange.step()
		if self.zrange!=None:
			self.zmin, self.zmax = self.zrange.minmax()
			self.zstep = self.zrange.step()
		self.env.setRepere(self)

	def objects(self):
		return [self]

	def proj(self, *coords):
		dim = len(coords)
		if dim==2:
			x, y = coords
			X, Y = (x-self.xmin)*self.XMAX/(self.xmax-self.xmin), (y-self.ymax)*self.YMAX/(self.ymin-self.ymax)
			return X, Y
		elif dim==3:
			x, y, z = coords
			x1, y1 = y-0.4*x, z-0.4*x
			X, Y = (x1-self.xmin)*self.XMAX/(self.xmax-self.xmin), (y1-self.ymax)*self.YMAX/(self.ymin-self.ymax)
			return X, Y
		else:
			raise "Dimension non implémentée"

	def trace(self, canvas):
		if self.zrange==None:
			self.draw2D(canvas)
		else:
			self.draw3D(canvas)

	def draw2D(self, canvas):
		if self.color==None:
			color = "#000000"
		else:
			r_, g_, b_ = self.color.val()
			color = "#%02x%02x%02x"%(r_,g_,b_)
		x = self.xmin
		while x<=self.xmax:
			X, Y = self.proj(x,0)
			canvas.create_line(X,Y-5,X,Y+5,fill=color)
			x += self.xstep
		y = self.ymin
		while y<=self.ymax:
			X, Y = self.proj(0,y)
			canvas.create_line(X-5,Y,X+5,Y,fill=color)
			y += self.ystep
		X0, Y0 = self.proj(0,0)
		X1, Y1 = self.proj(self.xmin,self.ymin)
		X2, Y2 = self.proj(self.xmax,self.ymax)
		canvas.create_line(X0,Y1,X0,Y2,fill=color)
		canvas.create_line(X1,Y0,X2,Y0,fill=color)

	def draw3D(self, canvas):
		pass
#		objs = []
#		if self.color==None:
#			color = "#000000"
#		else:
#			r_, g_, b_ = self.color.val()
#			color = "#%02x%02x%02x"%(r_,g_,b_)
#		x = self.xmin
#		while x<=self.xmax:
#			objs.append(Poly(Point(
#			X, Y = self.proj(x,0,0)
#			canvas.create_line(X,Y-5,X,Y+5,fill=color)
#			x += self.xstep
#		y = self.ymin
#		while y<=self.ymax:
#			X, Y = self.proj(0,y,0)
#			canvas.create_line(X-5,Y,X+5,Y,fill=color)
#			y += self.ystep
#		z = self.zmin
#		while z<=self.zmax:
#			X, Y = self.proj(0,0,z)
#			canvas.create_line(X-2,Y-2,X+2,Y+2,fill=color)
#			z += self.zstep

class Intervs(Node):
	pass

class Range(Node):

	def init(self, *args):
		print "range:", [ a.val() for a in self]

	def min(self): return self[0].val()
	def max(self): return self[1].val()
	def step(self): return self[2].val()
	def minmax(self): return self.min(), self.max()

class Graphe(Node):
	
	def init(self, params, intervs):
		self.params, self.intervs = params, intervs
		self.dim = len(self.params)
		self.env.check(self.dim in (1,2))
		self.color = Color(0,None,(255,255),(255,255),(255,255))

	def setColor(self, c):
		self.color = c

	Var2D = [ Ident(0,None,id) for id in ('x', 'y', 'r', 'theta', 'color') ]
	Var3D = [ Ident(0,None,id) for id in ('x', 'y', 'z', 'r', 'rho', 'theta', 'phi', 'color') ]
	
	def objects(self):
		objs = []
		eqs = tuple(self)[2:]
		vars = [p.name() for p in self.params] + [eq[0].name() for eq in eqs]
		eps = 1e-6
		if self.dim==1:
			if 'x' in vars and 'y' in vars: currentPoint = self.currentPoint2D_Cart
			elif 'r' in vars and 'theta' in vars: currentPoint = self.currentPoint2D_Pol
			else: return []
			p1 = self.params[0]
			amin, amax, astep = self.intervs[0].min(), self.intervs[0].max(), self.intervs[0].step()
			a = amin
			prev = None
			while a<=amax+eps:
				apply(self.env.undefVar, self.__class__.Var2D)
				self.env.setVar(p1,Float(0,None,a))
				for eq in eqs:
					eq.compute()
				try:
					current = currentPoint()
				except ValueError:
					current = None
				except ZeroDivisionError:
					current = None
				if prev!=None and current!=None:
					objs.append(Segment(prev,current))
				prev = current
				a += astep
		elif self.dim==2:
			if 'x' in vars and 'y' in vars and 'z' in vars: currentPoint = self.currentPoint3D_Cart
			if 'r' in vars and 'theta' in vars and 'phi' in vars: currentPoint = self.currentPoint3D_Sph
			if 'rho' in vars and 'phi' in vars and 'z' in vars: currentPoint = self.currentPoint3D_Cyl
			p1, p2 = self.params[0], self.params[1]
			amin, amax, astep = self.intervs[0].min(), self.intervs[0].max(), self.intervs[0].step()
			bmin, bmax, bstep = self.intervs[1].min(), self.intervs[1].max(), self.intervs[1].step()
			M = []
			a = amin
			while a<=amax+eps:
				V = []
				b = bmin
				while b<=bmax+eps:
					apply(self.env.undefVar,self.__class__.Var3D)
					self.env.setVar(p1,Float(0,None,a))
					self.env.setVar(p2,Float(0,None,b))
					for eq in eqs:
						eq.compute()
					try:
						current = currentPoint()
					except ValueError:
						current = None
					except ZeroDivisionError:
						current = None
					V.append(current)
					b += bstep
				M.append(V)
				a += astep
			for a in xrange(len(M)-1):
				for b in xrange(len(M[a])-1):
					points = [ p for p in (M[a][b],M[a+1][b],M[a+1][b+1],M[a][b+1]) if p!=None ]
					if points != []:
						objs.append(Poly(points))
		else:
			raise "Dimension non implémentée"
		return objs

	def currentPoint2D_Cart(self):
		x = self.env.getVar(Ident(0,None,'x'))
		y = self.env.getVar(Ident(0,None,'y'))
		if x==None or y==None: return None
		x, y = x.val(), y.val()
		return Point(self.env.repere,self.color,x,y)

	def currentPoint2D_Pol(self):
		r = self.env.getVar(Ident(0,None,'r'))
		theta = self.env.getVar(Ident(0,None,'theta'))
		if r==None or theta==None: return None
		r, theta = r.val(), theta.val()
		return Point(self.env.repere,self.color,r*cos(theta),r*sin(theta))

	def currentPoint3D_Cart(self):
		x = self.env.getVar(Ident(0,None,'x'))
		y = self.env.getVar(Ident(0,None,'y'))
		z = self.env.getVar(Ident(0,None,'z'))
		if x==None or y==None or z==None: return None
		x, y, z = x.val(), y.val(), z.val()
		return Point(self.env.repere,self.color,x,y,z)

	def currentPoint3D_Sph(self):
		r = self.env.getVar(Ident(0,None,'r'))
		theta = self.env.getVar(Ident(0,None,'theta'))
		phi = self.env.getVar(Ident(0,None,'phi'))
		if r==None or theta==None or phi==None: return None
		r, theta, phi = r.val(), theta.val(), phi.val()
		return Point(self.env.repere,self.color,r*sin(theta)*cos(phi),r*sin(theta)*sin(phi),r*cos(theta))

	def currentPoint3D_Cyl(self):
		rho = self.env.getVar(Ident(0,None,'rho'))
		phi = self.env.getVar(Ident(0,None,'phi'))
		z = self.env.getVar(Ident(0,None,'z'))
		if z==None or phi==None or z==None: return None
		rho, phi, z = rho.val(), phi.val(), z.val()
		return Point(self.env.repere,self.color,rho*cos(phi),rho*sin(phi),z)

class Point:
	
	def __init__(self, rep, color, *coords):
		self.color = color.val()
		dim = len(coords)
		self.dist = coords[0]
		if dim==2:
			self.x, self.y = rep.proj(coords[0], coords[1])
		elif dim==3:
			self.x, self.y = rep.proj(coords[0], coords[1], coords[2])
		else:
			raise "Dimension non implémentée"

class Segment:

	def __init__(self, a, b):
		r_ = (a.color[0]+b.color[0])/2
		g_ = (a.color[1]+b.color[1])/2
		b_ = (a.color[2]+b.color[2])/2
		self.color = "#%02x%02x%02x"%(r_,g_,b_)
		self.a, self.b = a, b

	def trace(self, canvas):
		canvas.create_line(self.a.x, self.a.y, self.b.x, self.b.y, fill=self.color)

class Poly:

	def __init__(self, points):
		r_, g_, b_ = 0, 0, 0
		self.dist = 0
		for p in points:
			r_ += p.color[0]
			g_ += p.color[1]
			b_ += p.color[2]
			self.dist += p.dist
		n = len(points)
		r_ /= n
		g_ /= n
		b_ /= n
		self.dist /= n
		self.color = "#%02x%02x%02x"%(r_,g_,b_)
		self.point = points
		self.trace_n = [None, self.trace_1, self.trace_2, self.trace_3, self.trace_4][n]

	def __cmp__(self,other):
		if isinstance(other,Poly):
			return cmp(self.dist,other.dist)
		return 0

	def trace(self, canvas):
		self.trace_n(canvas)
		coords = []
		for x,y in [(p.x,p.y) for p in self.point+[self.point[0]]]:
			coords.append(x)
			coords.append(y)
		apply(canvas.create_line,coords)

	def trace_1(self, canvas):
		canvas.create_polygon(self.point[0].x,self.point[0].y,fill=self.color)
	def trace_2(self, canvas):
		canvas.create_polygon(self.point[0].x,self.point[0].y,self.point[1].x,self.point[1].y,fill=self.color)
	def trace_3(self, canvas):
		canvas.create_polygon(self.point[0].x,self.point[0].y,self.point[1].x,self.point[1].y,self.point[2].x,self.point[2].y,fill=self.color)
	def trace_4(self, canvas):
		canvas.create_polygon(self.point[0].x,self.point[0].y,self.point[1].x,self.point[1].y,self.point[2].x,self.point[2].y,self.point[3].x,self.point[3].y,fill=self.color)

class Color(Node):
	color = Ident(0,None,'color')
	def init(self, r, g, b):
		self.r, self.g, self.b = r, g, b
	def val(self):
		if self.env==None: return (0,0,0)
		c = self.env.getVar(self.__class__.color)
		if c==None: c = 0
		else: c = c.val()
		r0, r1 = self.r[0].val(), self.r[1].val()
		g0, g1 = self.g[0].val(), self.g[1].val()
		b0, b1 = self.b[0].val(), self.b[1].val()
		r = int(c*(r1-r0)+r0)
		g = int(c*(g1-g0)+g0)
		b = int(c*(b1-b0)+b0)
		return r,g,b

class Eq(Node):

	def compute(self):
		self.env.setVar(self[0], self[1])

class Fonction(Node):
	def init(self, f, args, e):
		self.env.setVar(self[0],self)
	def objects(self):
		return []

	def val(self):
		return self[2].val()

class Fun(Node):

	def val(self):
		fonction = self.env.getVar(self[0])
		if fonction==None: return 0
		i = 0
		for param in self[1]:
			self.env.setVar(fonction[1][i],param)
			i += 1
		return fonction.val()

class Pow(Node):
	def val(self):
		return self[0].val()**self[1].val()

class Mod(Node):
	def val(self):
		return self[0].val()%self[1].val()

class Add(Node):
	def val(self):
		return self[0].val()+self[1].val()

class Sub(Node):
	def val(self):
		return self[0].val()-self[1].val()

class Div(Node):
	def val(self):
		return self[0].val()/self[1].val()

class Mul(Node):
	def val(self):
		return self[0].val()*self[1].val()

class Float(Node):

	def val(self):
		return self[0]

class Neg(Node):

	def val(self):
		return -self[0].val()

class Cos(Node):
	def val(self): return cos(self[0].val())
		
class Sin(Node):
	def val(self): return sin(self[0].val())
		
class Tan(Node):
	def val(self): return tan(self[0].val())
		
class Acos(Node):
	def val(self): return acos(self[0].val())
		
class Asin(Node):
	def val(self): return asin(self[0].val())
		
class Atan(Node):
	def val(self): return atan(self[0].val())
		
class Abs(Node):
	def val(self): return abs(self[0].val())
		
class Sqrt(Node):
	def val(self): return sqrt(self[0].val())
		
Grammar ="""

{{
	from string import atof
}}

parser MathParser:

	{{

	def init(self):
		self.symbol = {}

	def setRepere(self, rep):
		self.repere = rep
		rep.XMAX, rep.YMAX = self.XMAX, self.YMAX

	def undefVar(self, *vars):
		for var in vars:
			try:
				del self.symbol[var.name()]
			except KeyError:
				pass

	def setVar(self, var, val):
		self.symbol[var.name()] = val

	def getVar(self, var):
		try:
			return self.symbol[var.name()]
		except KeyError:
			return None

	def setWindow(self, xres, yres):
		self.XMAX, self.YMAX = xres, yres

}}

lex skip -> '\s+' | '#.*' .

START/cmds -> COMMANDS/cmds .

COMMANDS/cmds -> cmds = Commands<> ( COMMAND/c cmds-c )* '$'.

COMMAND/c ->
	REPERE/c
|	FONCTION/c
|	GRAPHE/c
.

REPERE/Repere<c,x,y,z> ->
	'repere' ':'
		RANGE/x
		RANGE/y
		(	RANGE/z
		|	z = None
		)
		( 'color' COLOR/c | c=None )
	.

RANGE/Range<min,max,step> -> '\(' EXPR/min ',' EXPR/max ( ',' EXPR/step | step=Div<Sub<max,min>,Float<20>> ) '\)' .

RANGES/intervs -> intervs=Intervs<> RANGE/i intervs-i ( ',' RANGE/i intervs-i )* .

FONCTION/Fonction<f,args,e> ->
	IDENT/f
	( '\(' IDENTS/args '\)' | args=Idents<> )
	'='
	EXPR/e
	.

IDENT/Ident<id> -> '[a-zA-Z]\w*'/id .

IDENTS/ids -> ids=Idents<> IDENT/id ids-id ( ',' IDENT/id ids-id )* .

GRAPHE/g ->
	'for' IDENTS/params 'in' RANGES/intervs ':'
		{{ self.check(len(params)==len(intervs)) }}
	g = Graphe<params,intervs>
	(	IDENT/id '=' EXPR/e
		{{ self.check(id not in params) }}
		g-Eq<id,e>
	|	'color' COLOR/c {{ g.setColor(c) }}
	)+
	.

COLOR/Color<r,g,b> -> 
	COLOR_COMP/r
	COLOR_COMP/g
	COLOR_COMP/b
	.

COLOR_COMP/<min,max> -> EXPR/min ( ':' EXPR/max | max=min ) .

EXPR/e ->
	TERM/e
	(	'\+' TERM/t e=Add<e,t>
	|	'\-' TERM/t e=Sub<e,t>
	)*
	.

TERM/t ->
	FACT/t
	(	'\*' FACT/f t=Mul<t,f>
	|	'\/' FACT/f t=Div<t,f>
	|	'\%' FACT/f t=Mod<t,f>
	)*
	.

FACT/f -> SATOM/f ( '\^' FACT/e f=Pow<f,e> )? .

SATOM/a ->
	'\-' '\-' SATOM/a
|	'\-' SATOM/a a=Neg<a>
|	ATOM/a
.

ATOM/a ->
	REAL/a
|	BUILTIN_FONCTION/a
|	FUN/a
|	'\(' EXPR/a '\)'
.

REAL/Float<r> ->
	(	'\d+\.\d*'/r
	|	'\d*\.\d+'/r
	|	'\d+'/r
	)
	{{ r = atof(r) }}
	.

FUN/Fun<f,args> -> IDENT/f ( '\(' IDENTS/args '\)' | args=Idents<> ) .

BUILTIN_FONCTION/f ->
	'cos' X/x f=Cos<x>
|	'sin' X/x f=Sin<x>
|	'tan' X/x f=Tan<x>
|	'acos' X/x f=Acos<x>
|	'asin' X/x f=Asin<x>
|	'atan' X/x f=Atan<x>
|	'abs' X/x f=Abs<x>
|	'sqrt' X/x f=Sqrt<x>
.

X/x -> '\(' EXPR/x '\)' .

"""
		
if __name__ == "__main__":
	if len(sys.argv)==1:
		name = 'stdin'
		f = sys.stdin
	elif len(sys.argv)==2:
		name = sys.argv[1]
		f = open(name)
	else:
		raise "Syntax : %s <equation file>"%(sys.argv[0])
	input = f.read()
	f.close()
	exec(TPParser()(Grammar))
	env = MathParser()
	env.setWindow(800,600)
	cmds = env(input)
	Graph(name,env,cmds).mainloop()
