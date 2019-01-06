from os.path import join, isdir, islink
from os import error, listdir

import os

def dirwalk(top, topdown=True, onerror=None, deeplevel=0): # fix 0
    """Modified directory tree generator.

    For each directory in the directory tree rooted at top (including top
    itself, but excluding '.' and '..'), yields a 4-tuple

        dirpath, dirnames, filenames, deeplevel

    dirpath is a string, the path to the directory.  dirnames is a list of
    the names of the subdirectories in dirpath (excluding '.' and '..').
    filenames is a list of the names of the non-directory files in dirpath.
    Note that the names in the lists are just names, with no path components.
    To get a full path (which begins with top) to a file or directory in
    dirpath, do os.path.join(dirpath, name). 

    ----------------------------------------------------------------------
    + deeplevel is 0-based deep level from top directory
    ----------------------------------------------------------------------
    ...

    """

    try:
        names = listdir(top)
    except error, err:
        if onerror is not None:
            onerror(err)
        return

    dirs, nondirs = [], []
    for name in names:
        if isdir(join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs, deeplevel # fix 1
    for name in dirs:
        path = join(top, name)
        if not islink(path):
            for x in dirwalk(path, topdown, onerror, deeplevel+1): # fix 2
                yield x
    if not topdown:
        yield top, dirs, nondirs, deeplevel # fix 3



def main():
	f = open("SUMMARY.md", "w+")
	for topdir in ("Defense", "Offense"):
		for root, dirs, files, level in dirwalk(topdir):
			name = root.split("/")[-1]
			link = ""
			idFiles = [name+".md", "README.md"]
			for idFile in idFiles:
				if idFile in files:
					link = root+"/"+idFile
					break

			f.write("    "*level + "- [%(name)s](%(link)s)\n" % locals())
			for file in set(files)-set(idFiles):
				filepath = root + "/" + file
				f.write("    "*(level+1) + "- [%(file)s](%(filepath)s)\n" % locals())
	f.close()
if __name__ == '__main__':
	main()