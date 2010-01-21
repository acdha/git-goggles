import math

from gitgoggles.utils import force_unicode, force_str, console, colored

class AsciiCell(object):
    def __init__(self, value, color=None, background=None, reverse=False, width=None):
        self.value = force_unicode(value)
        self.color = color
        self.background = background
        self.attrs = reverse and ['reverse'] or []
        self.width = width and int(width) or len(self.value)
        self.lines = int(math.ceil(len(self.value) / float(self.width)))

    def line(self, num):
        return self.value[num * self.width:(1 + num) * self.width]

class AsciiRow(object):
    def __init__(self, *cells):
        super(AsciiRow, self).__init__(self)
        self.cells = [ isinstance(x, AsciiCell) and x or AsciiCell(x) for x in cells ]
        self.lines = max([ x.lines for x in self.cells ])

    def __iter__(self):
        for cell in self.cells:
            yield cell

    def __len__(self):
        return len(self.cells)

class AsciiTable(object):
    def __init__(self, headers, left_padding=None, right_padding=None, horizontal_rule=True):
        self.headers = AsciiRow(*headers)
        self.rows = []
        self._widths = [ x.width for x in self.headers ]
        self.left_padding = left_padding and int(left_padding) or 0
        self.right_padding = right_padding and int(right_padding) or 0
        self.horizontal_rule = horizontal_rule

    def add_row(self, data):
        if len(data) != len(self.headers):
            raise Exception('The number of columns in a row must be equal to the header column count.')
        self.rows.append(AsciiRow(*data))

    def __str__(self):
        self.__unicode__()

    def __unicode__(self):
        self._print()

    def _print_horizontal_rule(self):
        bits = []
        console(u'+')
        for column, width in zip(self.headers, self._widths):
            console(u'-' * (self.right_padding + self.left_padding + width))
            console(u'+')
        console(u'\n')

    def _print_headers(self):
        self._print_horizontal_rule()
        self._print_row(self.headers)
        self._print_horizontal_rule()

    def _print_rows(self):
        for row in self.rows:
            self._print_row(row)
            if self.horizontal_rule:
                self._print_horizontal_rule()

    def _print_row(self, row):
        bits = []
        for line in xrange(row.lines):
            console(u'|')
            for cell, width in zip(row, self._widths):
                console(colored(u' ' * self.left_padding + cell.line(line).ljust(width) + u' ' * self.right_padding, cell.color, cell.background, attrs=cell.attrs))
                console(u'|')
            console(u'\n')

    def render(self):
        self._calculate_widths()

        self._print_headers()
        self._print_rows()
        if not self.horizontal_rule:
            self._print_horizontal_rule()

    def _calculate_widths(self):
        for row in self.rows:
            for column, cell in enumerate(row):
                self._widths[column] = max(self._widths[column], cell.width)
