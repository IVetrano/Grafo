import random
from TDAs_auxiliares import Cola, Pila, Heap
from grafo import Grafo


#########################################################
#				OPERACIONES CON GRAFOS					#
#########################################################

def obtener_vertices_de_entrada(grafo, vertice):
	"""
	Recibe un grafo y un vertice y devuelve un conjunto con los los vertices
	que tienen al vertice pasado por parametro como adyacente.
	"""
	res = set()
	for v in grafo.obtener_vertices():
		if vertice in grafo.adyacentes(v):
			res.add(v)
	return res


def bfs(grafo, origen):
	"""
	Hace un recorrido bfs en un grafo conexo y devuelve el diccionario de padres, de orden, y de visitados
	"""
	visitados = set()
	padres = {}
	orden = {}
	padres[origen] = None
	orden[origen] = 0
	visitados.add(origen)
	q = Cola()
	q.encolar(origen)

	while not q.esta_vacia():
		v = q.desencolar()
		for w in grafo.adyacentes(v):
			if w not in visitados:
				padres[w] = v
				orden[w] = orden[v] + 1
				visitados.add(w)
				q.encolar(w)

	return padres, orden, visitados


def componentes_fuertemente_conexas(grafo, origen):
	"""
	Devuelve las componentes fuertemente conexas de un grafo dirigido
	"""
	visitados = set()
	orden = {}
	mas_bajo = {}
	cfcs = []
	orden[origen] = 0
	pila = Pila()
	apilados = set()
	_componentes_fuertemente_conexas(grafo, origen, visitados, orden, mas_bajo, pila, apilados, cfcs)
	return cfcs


def _componentes_fuertemente_conexas(grafo, v, visitados, orden, mas_bajo, pila, apilados, cfcs):
	visitados.add(v)
	mas_bajo[v] = orden[v]
	pila.apilar(v)
	apilados.add(v)
	
	
	for w in grafo.adyacentes(v):
		if w not in visitados:
			orden[w] = orden[v] + 1
			_componentes_fuertemente_conexas(grafo, w, visitados, orden, mas_bajo, pila, apilados, cfcs)
	
		if w in apilados:
			mas_bajo[v] = min(mas_bajo[v], mas_bajo[w])
	
	
	if orden[v] == mas_bajo[v] and pila.cantidad() > 0:
		nueva_cfc = []
		while True:
			w = pila.desapilar()
			apilados.remove(w)
			nueva_cfc.append(w)
			if w == v:
				break
	  
		cfcs.append(nueva_cfc)

def camino_minimo_bfs(grafo, origen):
	"""
	Recibe un grafo y un origen y hace un recorrido para encontrar el camino minimo en vertices.
	Devuelve un diccionario de padres con los padres de cada vertice para que el camino al vertice origen sea
	el minimo, y un diccionario de distancia que contiene las distancias minimas de cada vertice al vertice origen.
	"""
	visitados = set()
	padres = {}
	distancia = {}

	for v in grafo.obtener_vertices():
		distancia[v] = float("inf")

	padres[origen] = None
	distancia[origen] = 0
	visitados.add(origen)
	q = Cola()
	q.encolar(origen)

	while not q.esta_vacia():
		v = q.desencolar()
		for w in grafo.adyacentes(v):
			if w not in visitados:
				padres[w] = v
				distancia[w] = distancia[v] + 1
				visitados.add(w)
				q.encolar(w)

	return padres, distancia


def obtener_camino(padres, inicio, fin):
	"""
	Recibe un diccionario de padres, un vertice de inicio y un vertice de fin y devuelve el camino desde
	el vertice inicio al vertice fin.
	"""
	if inicio == fin:
		return [inicio]
		
	v = fin
	res = [v]
	while padres[v] != inicio:
		res.append(padres[v])
		v = padres[v]

	res.append(padres[v])
	return list(reversed(res))	

def max_frec(lista):
	"""
	Recibe una lista y devuelve el valor mas frecuente de esta.
	"""
	dic = {}
	for e in lista:
		dic[e] = dic.setdefault(e, 0) + 1
	return max(dic, key=dic.get)

def convirgio_label(grafo, label):
	"""
	Recibe un grafo y un diccionario de labels y devuelve True si la mayoria de los adyacentes de cada vertice tienen
	el mismo label que él, o False si no es asi.
	"""
	dic = {}
	for v in grafo.obtener_vertices():
		mas_frecuente = max_frec([label[ady] for ady in grafo.adyacentes(v)])
		condicion = mas_frecuente == label[v]
		dic[condicion] = dic.setdefault(condicion, 0) + 1
	return max(dic, key=dic.get)

def obtener_vertices_label(grafo, label, i):
	"""
	Recibe un grafo, un diccionario de labels y un entero i y devuelve todos los
	vertices que tengan a i como label.
	"""
	res = []
	for v in grafo.obtener_vertices():
		if label[v] == i:
			res.append(v)
	return res

def obtener_labels(label):
	"""
	Recibe un diccionario que contiene como clave los vertices y como valor labels y devuelve 
	un diccionario con los labels como clave y la cantidad de vertices que los tienen asignados.
	"""
	res = {}
	for v in label:
		res[label[v]] = res.setdefault(label[v], 0) + 1
	return res

def label_propagation(grafo, minimo):
	"""
	Recibe un grafo y un minimo, y devuelve las "comunidades" del grafo que tengan el minimo o mas vertices.
	"""
	res = []
	label = {}
	vertices = grafo.obtener_vertices()

	#Para cada vértice Vi: label[vi] = i
	for i in range(len(vertices)):
		label[vertices[i]] = i

	#Mientras no se cumpla la condicion de corte
	while not convirgio_label(grafo, label):

		#Determino un orden aleatorio para los vertices
		random.shuffle(vertices)

		#Por cada vertice, label[v] es igual al mas frecuente de los label de sus vertices de entrada
		for v in vertices:
			vertices_entrada = obtener_vertices_de_entrada(grafo, v)
			label[v] = max_frec([label[x] for x in vertices_entrada])

	#Devuelvo los vertices de los labels que superan el minimo
	labels = obtener_labels(label)
	for l in labels:
		if labels[l] >= minimo:
			res.append(obtener_vertices_label(grafo, label, l))

	return res

def pagerank(grafo):
	"""
	Aplica a un grafo el algoritmo PageRank y devuelve el diccionario de ranks.
	"""
	#Amortiguacion
	d = 0.1
	rank = {}
	for v in grafo.obtener_vertices():
		rank[v] = 1

	#Actualizo el rank una vez por cada vertice en el grafo 5 veces
	for _ in range(5):
		for v in grafo.obtener_vertices():
			actualizar_rank(grafo, rank, v, d)
	return rank

def actualizar_rank(grafo, rank, v, d):
	"""
	Recibe un grafo, un diccionario de ranks, un verticem y un valor de amortiguacion y
	actualiza el valor del vertice.
	"""
	padres = obtener_vertices_de_entrada(grafo, v)
	sumatoria = 0
	for w in padres:
		sumatoria += rank[w] / len(grafo.adyacentes(w))

	n = len(grafo.obtener_vertices())

	rank[v] = ((1 - d) / n) + d * sumatoria

def camino_largo_n(grafo, inicio, fin, n):
	"""
	Recibe un grafo, un vertice de inicio y uno de fin, y un entero positivo "n", busca
	por backtracking un camino desde inicio hasta fin de largo "n" (sin tener en cuenta los pesos de
	las aristas) y devuelve un booleano "existe" que indica si existe o no el camino, y un diccionario de
	padres para poder reconstruirlo.
	"""
	visitados = {}
	padres = {}
	existe = _camino_largo_n(grafo, inicio, fin, n, visitados, 0, padres, True)
	return existe, padres

def _camino_largo_n(grafo, v, fin, n, visitados, distancia, padres, primera):
	if v == fin and not primera:
		if distancia == n:
			return True
		return False

	visitados[v] = True
	dist = distancia + 1

	for ady in grafo.adyacentes(v):
		if (ady not in visitados or ady == fin) and distancia < n:
			padres[ady] = v
			if _camino_largo_n(grafo, ady, fin, n, visitados, dist, padres, False):
				return True

	visitados.pop(v)
	return False


def dijkstra(grafo, origen):
	"""
	Recibe un grafo y un origen y le aplica el algoritmo de Dijkstra para encontrar el camino minimo.
	Devuelve un diccionario de padres con los padres de cada vertice para que el camino al vertice origen sea
	el minimo, y un diccionario de distancia que contiene las distancias minimas de cada vertice al vertice origen.
	"""
	padres = {}
	distancia = {}

	for v in grafo.obtener_vertices():
		distancia[v] = float("inf")
	
	padres[origen] = None
	distancia[origen] = 0
	h = Heap()
	h.encolar(Vertice_distancia(origen, distancia[origen]))

	while not h.esta_vacio():
		v = h.desencolar()
		for w in grafo.adyacentes(v):
			if distancia[v] + grafo.peso_arista(v, w) < distancia[w]:
				padres[w] = v
				distancia[w] = distancia[v] + grafo.peso_arista(v, w)
				h.encolar(Vertice_distancia(w, distancia[w]))

	return padres, distancia

def obtener_aristas(grafo):
	"""
	Devuelve una lista con todas las aristas y sus pesos de la forma [(vertice_1, vertice_2, peso), ...].
	"""
	aristas = []
	for v in grafo.obtener_vertices():
		for w in grafo.adyacentes(v):
			aristas.append((v, w, grafo.peso_arista(v, w)))
	return aristas

def bellman_ford(grafo, origen):
	"""
	Recibe un grafo y un origen y le aplica el algoritmo de Bellman-Ford para encontrar el camino minimo.
	Devuelve un diccionario de padres con los padres de cada vertice para que el camino al vertice origen sea
	el minimo, y un diccionario de distancia que contiene las distancias minimas de cada vertice al vertice origen.
	"""
	distancia = {}
	padres = {}

	for v in grafo.obtener_vertices():
		distancia[v] = float("inf")

	padres[origen] = None
	distancia[origen] = 0

	aristas = obtener_aristas(grafo)

	for i in range(len(grafo.obtener_vertices())):
		for v, w, peso in aristas:
			if distancia[v] + grafo.peso_arista(v, w) < distancia[w]:
				padres[w] = v
				distancia[w] = distancia[v] + grafo.peso_arista(v, w)

	for v, w, peso in aristas:
		if distancia[v] + grafo.peso_arista(v, w) < distancia[w]:
			return None

	return padres, distancia

