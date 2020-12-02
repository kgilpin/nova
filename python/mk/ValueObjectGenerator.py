from CodeGenerator import CodeGenerator
from MiscUtils import AbstractError
from time import asctime, localtime, time
import string
import os, sys
from types import *

try:
	from mx import DateTime
except ImportError:
	DateTime = None

def public(list):
	return [ obj for obj in list if not obj.has_key('restriction') ]

def publicOrPrivate(list):
	return [ obj for obj in list if not obj.has_key('restriction') or obj['restriction'] == 'private' ]

class ValueObjectGenerator(CodeGenerator):

	def defaultConfig(self):
		return {
			'DestDir': 'api',
		}

	def generate(self, dirname):
		self.requireDir(dirname)
		self.requireDir(os.path.join(dirname, 'api'))
		self._model.writePy(self, os.path.join(dirname, 'api'))


class Model:

	def writePy(self, generator, dirname):
		fileName = os.path.join(dirname, 'beans.py')
		print 'opening %s' % fileName
		self.out = open(fileName, 'w')	
		self.writePyImports()
		for klass in public(self._allKlassesInOrder):
			klass.writePy(generator, self.out, publicOrPrivate)

		self.out.close()

	def writePyImports(self):
		wr = self.out.write
		wr('import types\n')
		if DateTime:
			wr('from mx import DateTime\n')

class Klass:

	def writePy(self, generator, out, filter):
		self._filter = filter
		self._pyGenerator = generator
		self._pyOut = out
		self.writePyClassDef()

	def writePyClassDef(self):
		wr = self._pyOut.write
		if self.superklass() is None or not len(self._filter([ self.superklass() ])):
			wr('\nclass %s:\n' % self.name())
		else:
			wr('\nclass %s(%s):\n' % (self.name(), self.supername()))
		self.writePyInit()
		wr('\n')

	def writePyInit(self):
		wr = self._pyOut.write

		wr('\n\tdef __init__(self')
		self._writeInitArgDecls()		
		wr('):\n')
		wr('\t\t# Construct the %s with all its attributes\n' % self.name())

		self._writeInitArgAssignments()		

	def _writeInitArgDecls(self):
		if self.superklass() is not None:
			self.superklass()._writeInitArgDecls()
		wr = self._pyOut.write
		for attr in self._filter(self.attrs()):
			wr(', the%s' % attr.name())

	def _writeInitArgAssignments(self):
		if self.superklass() is not None:
			self.superklass()._writeInitInvocation()
		wr = self._pyOut.write
		for attr in self._filter(self.attrs()):
			wr('\t\tself.%s = the%s\n' % ( attr.name(), attr.name() ))
					
	def _writeInitInvocation(self):
		if self.superklass() is not None:
			self.superklass()._writeInitInvocation()
		wr = self._pyOut.write
		wr('\t\t%s.__init__(self' % self.name())
		for attr in self._filter(self.attrs()):
			wr(', the%s' % attr.name())
		wr(')\n')
		