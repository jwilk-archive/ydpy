import colorterm
import format_text

class YdpFormatter(format_text.YdpFormatter):

    def set_color(self, value):
        old_value = self._color
        self._color = value
        self.write(colorterm.reset() + value, strip = False)
        return old_value

    def set_bold_color(self):
        return self.set_color(self._color + colorterm.bold())

    def cleanup(self):
        return colorterm.reset()

    def __init__(self, encoding):
        format_text.YdpFormatter.__init__(self, encoding)
        self._color = ''
        self._color_map = \
        {
            'color: red;': colorterm.fgcolor(colorterm.RED),
            'color: green;': colorterm.fgcolor(colorterm.GREEN),
            'color: blue;': colorterm.fgcolor(colorterm.BLUE),
            'color: magenta;': colorterm.fgcolor(colorterm.MAGENTA),
        }

# vim:ts=4 sw=4 et
