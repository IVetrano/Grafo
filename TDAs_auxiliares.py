#########################################################
#					TDAs AUXILIARES						#
#########################################################
import heapq


class Nodo:
	def __init__(self, dato, prox):
		self.dato = dato
		self.prox = prox

class Cola:
	def __init__(self):
		self.prim = None
		self.ult = None

	def encolar(self, x):
		nuevo = Nodo(x, None)
		if self.ult:
			self.ult.prox = nuevo
			self.ult = nuevo
		else:
			self.prim = nuevo
			self.ult = nuevo

	def desencolar(self):
		if self.prim:
			valor = self.prim.dato
			self.prim = self.prim.prox
			if not self.prim:
				self.ult = None
			return valor
		else:
			raise ValueError("La cola esta vacia")


	def esta_vacia(self):
		return self.prim == None

	def ver_tope(self):
		return self.prim.dato


class Pila:
	def __init__(self):
		self.items = []

	def esta_vacia(self):
		return len(self.items) == 0

	def apilar(self, x):
		self.items.append(x)
	
	def desapilar(self):
		if self.esta_vacia():
			raise IndexError("La pila está vacía")
		return self.items.pop()

	def __str__(self):
		res = "| "
		for e in self.items:
			res += str(e) + ", "
		res = res.rstrip(", ") + " >"
		return res

	def ver_tope(self):
		return self.items[-1]

	def cantidad(self):
		return len(self.items)


class Heap:
	def __init__(self, lista_base=[]):
		if lista_base == []:
			self.elementos = []
			self.cantidad_elementos = 0
		else:
			self.elementos = lista_base[:]
			heapq.heapify(self.elementos)
			self.cantidad_elementos = len(self.elementos)

	def esta_vacio(self):
		return len(self.elementos) == 0

	def encolar(self, elemento):
		heapq.heappush(self.elementos, elemento)
		self.cantidad_elementos += 1

	def desencolar(self):
		if self.esta_vacio(): return None
		self.cantidad_elementos -= 1
		return heapq.heappop(self.elementos)

	def __str__(self):
		res = "| "
		for e in self.elementos:
			res += str(e) + ", "
		res = res.rstrip(", ") + " >"
		return res

	def ver_tope(self):
		if self.esta_vacio(): return None
		return self.elementos[0]

	def cantidad(self):
		return self.cantidad_elementos