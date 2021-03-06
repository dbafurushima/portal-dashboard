from hashlib import sha256
from .log import app_log


class ChecksumFile:
    """[summary]
    """
    def __init__(self):
        self._hashes = []

    def add(self, filepath):
        """[summary]
        """
        h = sha256()
        app_log.debug("computing SHA256 sum of %s" % filepath)
        with filepath.open('rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                h.update(data)
        self._hashes.append((h.hexdigest(), filepath.name))

    @property
    def content(self):
        """[summary]
        """
        text = ''
        for filehash in self._hashes:
            text += '%s  %s\n' % (filehash[0], filehash[1])
        return text
