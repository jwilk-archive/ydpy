__all__ = ('YdpDict',)

import ctypes
import lxml.etree

libydp = ctypes.CDLL('libydpdict.so.2')
ydp_read_xhtml = libydp.ydpdict_read_xhtml
ydp_read_xhtml.restype = ctypes.POINTER(ctypes.c_char)
ydp_open = libydp.ydpdict_open
ydp_open.restype = ctypes.c_void_p
ydp_get_word = libydp.ydpdict_get_word
ydp_get_word.restype = ctypes.c_char_p
ydp_close = libydp.ydpdict_close
ydp_get_count = libydp.ydpdict_get_count

libc = ctypes.CDLL(None)

html_parser = lxml.etree.HTMLParser(recover = False, no_network = True)

class YdpWord(object):
    def __init__(self, owner, nth):
        self.owner = owner
        self.nth = nth
    
    @property
    def name(self):
        return self.owner._get_word(self.nth).decode('UTF-8')
    
    @property
    def definition(self):
        result = ydp_read_xhtml(self.owner._pointer, ctypes.c_int(self.nth))
        if result is None:
            raise ctypes.pythonapi.PyErr_SetFromErrno(ctypes.py_object(OSError))
        try:
            return lxml.etree.HTML(
                ctypes.cast(result, ctypes.c_char_p).value,
                parser=html_parser
            ).find('body' % globals())
        finally:
            libc.free(result)

class YdpDict(object):

    def _get_word(self, i):
        return ydp_get_word(self._pointer, ctypes.c_int(i))

    def __init__(self, dat_file_name, idx_file_name):
        self._pointer = ydp_open(dat_file_name, idx_file_name, 1)
        if not self._pointer:
            self._open = False
            raise ctypes.pythonapi.PyErr_SetFromErrno(ctypes.py_object(OSError))
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
