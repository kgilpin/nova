# Priority dictionary using binary heaps
# David Eppstein, UC Irvine, 8 Mar 2002

import math
from UserDict import UserDict

class priorityDictionary(UserDict):
	def __init__(self):
		'''Initialize priorityDictionary by creating binary heap
of pairs (value,key).  Note that changing or removing a dict entry will
not remove the old pair from the heap until it is found by smallest() or
until the heap is rebuilt.'''
		self.__heap = []
		UserDict.__init__(self)
	
	def update(self, other):
			for key in other.keys():
				self[key] = other[key]
				
	def smallest(self):
		'''Find smallest item after removing deleted items from heap.'''
		if len(self) == 0:
			raise IndexError, "smallest of empty priorityDictionary"
		heap = self.__heap
		while not self.has_key(heap[0][1]) or self[heap[0][1]] != heap[0][0]:
			lastItem = heap.pop()
			insertionPoint = 0
			while 1:
				smallChild = 2*insertionPoint+1
				if smallChild+1 < len(heap) and \
						heap[smallChild] > heap[smallChild+1]:
					smallChild += 1
				if smallChild >= len(heap) or lastItem <= heap[smallChild]:
					heap[insertionPoint] = lastItem
					break
				heap[insertionPoint] = heap[smallChild]
				insertionPoint = smallChild
		return heap[0][1]
	
	def iterator(self):
		'''Create destructive sorted iterator of priorityDictionary.'''
		"""
		def iterfn():
			while len(self) > 0:
				x = self.smallest()
				yield x
				del self[x]
		return iterfn()
		"""
		class dictIterator:
			def __init__(self, dict):
				self._dict = dict
				self._previous = None
			
			def next(self):
				if self._previous:
					del self._dict[self._previous]
				self._previous = None
				if len(self._dict) > 0:
					self._previous = self._dict.smallest()
					# print self._previous
					return self._previous
				return None
		
		return dictIterator(self)
	
	def __setitem__(self,key,val):
		'''Change value stored in dictionary and add corresponding
pair to heap.  Rebuilds the heap if the number of deleted items grows
too large, to avoid memory leakage.'''
		# print 'Adding %s = %s' % ( key , val )
		UserDict.__setitem__(self,key,val)
		heap = self.__heap
		if len(heap) > 2 * len(self):
			self.__heap = [(v,k) for k,v in self.iteritems()]
			self.__heap.sort()	# builtin sort likely faster than O(n) heapify
		else:
			newPair = (val,key)
			insertionPoint = len(heap)
			heap.append(None)
			while insertionPoint > 0 and \
					newPair < heap[int(math.floor((insertionPoint-1)/2))]:
				heap[insertionPoint] = heap[int(math.floor((insertionPoint-1)/2))]
				insertionPoint = int(math.floor((insertionPoint-1)/2))
			heap[insertionPoint] = newPair
	
	def setdefault(self,key,val):
		'''Reimplement setdefault to call our customized __setitem__.'''
		if key not in self:
			self[key] = val
		return self[key]
