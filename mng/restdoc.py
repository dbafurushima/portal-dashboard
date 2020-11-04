from .style import ReSTStyle


class ReSTDocument(object):

    def __init__(self, target='man'):
        self.style = ReSTStyle(self)
        self.target = target
        self.keep_data = True
        self._writes = []
        self.hrefs = {}

    def _write(self, s):
        if self.keep_data and s is not None:
            self._writes.append(s)

    def write(self, content):
        """
        Write content into the document.
        """
        self._write(content)

    def writeln(self, content):
        """
        Write content on a newline.
        """
        self._write('%s%s\n' % (self.style.spaces(), content))

    def peek_write(self):
        """
        Returns the last content written to the document without
        removing it from the stack.
        """
        return self._writes[-1]

    def pop_write(self):
        """
        Removes and returns the last content written to the stack.
        """
        return self._writes.pop()

    def push_write(self, s):
        """
        Places new content on the stack.
        """
        self._writes.append(s)

    def getvalue(self):
        """
        Returns the current content of the document as a string.
        """
        if self.hrefs:
            self.style.new_paragraph()
            for refname, link in self.hrefs.items():
                self.style.link_target_definition(refname, link)
        return ''.join(self._writes).encode('utf-8')

    def handle_data(self, data):
        if data and self.keep_data:
            self._write(data)
