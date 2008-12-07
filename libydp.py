__all__ = ('YdpDict',)

from ctypes import CDLL, Structure as CStructure
from ctypes import c_void_p, c_uint16, c_int, c_char, c_char_p
from ctypes import POINTER as c_pointer_t, pointer as c_pointer, cast
from ctypes import pythonapi as libpython, py_object
from lxml.etree import HTMLParser, HTML

libydp = CDLL('libydpdict.so.2')
ydp_read_xhtml = libydp.ydpdict_read_xhtml
ydp_read_xhtml.restype = c_pointer_t(c_char)
ydp_open = libydp.ydpdict_open
ydp_open.restype = c_void_p
ydp_get_word = libydp.ydpdict_get_word
ydp_get_word.restype = c_char_p
ydp_close = libydp.ydpdict_close
ydp_get_count = libydp.ydpdict_get_count

libc = CDLL('libc.so.6')

html_parser = HTMLParser(recover = False, no_network = True)

class YdpWord(object):
    def __init__(self, owner, nth):
        self.owner = owner
        self.nth = nth
    
    @property
    def name(self):
        return self.owner._get_word(self.nth).decode('UTF-8')
    
    @property
    def definition(self):
        result = ydp_read_xhtml(self.owner._pointer, c_int(self.nth))
        if result is None:
            raise libpython.PyErr_SetFromErrno(py_object(OSError))
        try:
            return HTML(cast(result, c_char_p).value, parser = html_parser).find('body' % globals())
        finally:
            libc.free(result)

class YdpDict(object):

    def _get_word(self, i):
        return ydp_get_word(self._pointer, c_int(i))

    def __init__(self, dat_file_name, idx_file_name):
        self._pointer = ydp_open(dat_file_name, idx_file_name, 1)
        if not self._pointer:
            self._open = False
            raise libpython.PyErr_SetFromErrno(py_object(OSError))
        self._open = True
        self._word_count = ydp_get_count(self._pointer)

    def __enter__(self):
        return self
    
    def __exit__(self, *exc_info):
        self.close()

    def __iter__(self):
        return (self[i] for i in xrange(self._word_count))

    def __getitem__(self, nth):
        return YdpWord(self, nth)
            
    def close(self):
        if self._open:
            ydp_close(self._pointer)

# vim:ts=4 sw=4 et
