import transliterate

class YdpFormatter(object):

	class UnhandledTag(Exception):
		pass

	def parse_body(self, node):
		for subnode in node:
			self(subnode)
		self.write('\n\n')

	def parse_p(self, node):
		self._strip = True
		self.write(node.text)
		for subnode in node:
			self(subnode)
		self.write('\n')
		self.write(node.tail)
	
	def parse_a(self, node):
		self.write(node.text)
		for subnode in node:
			self(subnode)
		self.write(node.tail)

	def parse_b(self, node):
		tmp_color = self.set_bold_color()
		self.write(node.text)
		for subnode in node:
			self(subnode)
		self.set_color(tmp_color)
		self.write(node.tail)
	
	def parse_i(self, node):
		self.write(node.text)
		for subnode in node:
			self(subnode)
		self.write(node.tail)
	
	def parse_sup(self, node):
		self.write('^')
		self.write(node.text)
		for subnode in node:
			self(subnode)
		self.write(node.tail)

	def parse_span(self, node):
		style = node.get('style')
		if style == 'display: block; margin-left: 1em;':
			from StringIO import StringIO
			tmp_file = self._file
			self._file = StringIO()
			for subnode in node:
				self(subnode)
			result = unicode(self)
			self._file = tmp_file
			self.write('\n  ')
			self.write(result.replace('\n', '\n  '))
			self.write('\n')
			self._strip = True
		else:
			color = self._color_map[style]
			tmp_color = self.set_color(color)
			self.write(node.text)
			for subnode in node:
				self(subnode)
			self.set_color(tmp_color)
		self.write(node.tail)
	
	def parse_br(self, node):
		self.write('\n')
		self.write(node.tail)
		self._strip = True

	def write(self, value, strip = True):
		value = value or ''
		if self._strip and strip:
			if value:
				value = value.lstrip()
				self._strip = False
		self._file.write(value)

	def set_color(self, value):
		pass

	def set_bold_color(self):
		pass

	def cleanup(self):
		return ''

	def fork(self):
		return self.__class__()

	def __init__(self, encoding):
		from StringIO import StringIO
		from collections import defaultdict
		self._file = StringIO()
		self._strip = False
		self._color_map = defaultdict(str)
		self._encoding = encoding

	def __str__(self):
		return unicode(self).encode(self._encoding, 'transliterate')

	def __unicode__(self):
		return self._file.getvalue()

	def __call__(self, node):
		if node.tag.isalpha():
			try:
				getattr(self, 'parse_%s' % node.tag)(node)
				return
			except AttributeError:
				pass
		raise YdpFormatter.UnhandledTag(node.tag)

# vim:ts=4 sw=4 noet
