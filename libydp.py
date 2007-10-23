#!/usr/bin/python2.5

__all__ = ('CYdpDict',)

from ctypes import CDLL, Structure as CStructure
from ctypes import c_void_p, c_uint16, c_uint32, c_int, c_char, c_char_p
from ctypes import POINTER as c_pointer_t, pointer as c_pointer, cast
from ctypes import pythonapi as libpython, py_object
from lxml.etree import HTML

liby = CDLL('libydpdict.so.1')
libc = CDLL('libc.so.6')

class YdpWord(object):
	def __init__(self, owner, nth):
		self.owner = owner
		self.nth = nth
	
	@property
	def name(self):
		return self.owner.words[self.nth].decode('UTF-8')
	
	@property
	def definition(self):
		read_xhtml = liby.ydpdict_read_xhtml
		read_xhtml.restype = c_pointer_t(c_char)
		result = read_xhtml(c_pointer(self.owner), c_uint32(self.nth))
		if result is None:
			raise libpython.PyErr_SetFromErrno(py_object(OSError))
		try:
			return HTML(cast(result, c_char_p).value).find('body' % globals())
		finally:
			libc.free(result)

class YdpDict(CStructure):
	_fields_ = \
	(
		('dat', c_void_p),
		('idx', c_void_p),
		('words', c_pointer_t(c_char_p)),
		('word_count', c_uint16),
		('indices', c_void_p),
		('encoding', c_int),
		('xhtml_header', c_int),
		('xhtml_title', c_char_p),
		('xhtml_style', c_char_p),
		('xhtml_use_style', c_int)
	)

	def __init__(self, dat_file_name, idx_file_name):
		rv = liby.ydpdict_open(c_pointer(self), dat_file_name, idx_file_name, 1)
		if rv != 0:
			self._open = False
			raise libpython.PyErr_SetFromErrno(py_object(OSError))
		self._open = True

	def __enter__(self):
		return self
	
	def __exit__(self, *exc_info):
		self.close()

	def __iter__(self):
		return (self[i] for i in xrange(self.word_count))

	def __getitem__(self, nth):
		return YdpWord(self, nth)
			
	def close(self):
		if self._open:
			liby.ydpdict_close(c_pointer(self))

# vim:ts=4 sw=4 noet
