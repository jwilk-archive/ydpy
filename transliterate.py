# encoding=UTF-8

from codecs import register_error as _register_error

FALLBACK = \
{
	u'\xa0': '\x20',
	u'°': '^o',
	u'·': '.',
	u'Ä': 'A',
	u'Ó': 'O',
	u'Ö': 'O',
	u'Ü': 'U',
	u'ß': 'ss',
	u'á': 'a',
	u'â': 'a',
	u'ä': 'a',
	u'æ': '<ae>',
	u'ç': 'c',
	u'é': 'e',
	u'ë': 'e',
	u'í': 'i',
	u'ï': 'i',
	u'ð': '<6>',
	u'ó': 'o',
	u'ô': 'o',
	u'ö': 'o',
	u'ü': 'u',
	u'ă': 'a',
	u'ą': 'a',
	u'Ć': 'C',
	u'ć': 'c',
	u'č': 'c',
	u'Ę': 'E',
	u'ę': 'e',
	u'Ł': 'L',
	u'ł': 'l',
	u'ń': 'n',
	u'ŋ': '<n>',
	u'ŕ': 'r',
	u'Ś': 'S',
	u'ś': 's',
	u'Ź': 'Z',
	u'ź': 'z',
	u'Ż': 'Z',
	u'ż': 'z',
	u'ɑ': '<a>',
	u'ɔ': '<o>',
	u'ə': '<e>',
	u'ɛ': '<E>',
	u'ɪ': '<i>',
	u'ʃ': '<|>',
	u'ʌ': '<^>',
	u'ʒ': '<3>',
	u'ˈ': "''",
	u'ː': ':',
	u'θ': '<0>',
	u'–': '--',
	u'‘': "`",
	u'’': "'",
	u'”': "''",
	u'„': ',,',
	u'†': '<t>',
	u'‡': '<tt>',
	u'…': '...',
}

def handler(exception):
	if isinstance(exception, (UnicodeEncodeError, UnicodeTranslateError)):
		return u''.join(FALLBACK.get(ch, u'<?>') for ch in exception.object[exception.start:exception.end]), exception.end
	else:
		raise TypeError("Don't know how to handle %s in error callback" % exception.__class__.__name__)

_register_error('transliterate', handler)

# vim:ts=4 sw=4 noet
