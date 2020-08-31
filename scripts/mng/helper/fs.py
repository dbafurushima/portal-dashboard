import os


def scandir(root, keep=None):
    for dentry in os.scandir(str(root)):
        if keep is not None and not keep(dentry):
            continue
        yield dentry
