# -*- coding: utf-8 -*-

import os, sys, re
import subprocess


def create_qrc(dirname, prefix=None):
    basename = os.path.basename(dirname)

    file_list = []

    for root, dirs, files in os.walk(dirname):
        file_list += [os.path.relpath(os.path.join(root, filename), dirname)
                      for filename in files]

    file_list.sort()

    contents = '<!DOCTYPE RCC>\n<RCC version="1.0">\n\n'

    if prefix:
        contents += '<qresource prefix="/{}">\n'.format(prefix)
    else:
        contents += '<qresource>\n'

    for filename in file_list:
        if (filename.endswith('.webp') or filename.endswith('.png') or
                filename.endswith('.jpg') or filename.endswith('.ttf') or
                filename.endswith('.svga') ):
            contents += '\t<file>' + filename.replace('\\', '/') + '</file>\n'

    contents += '</qresource>\n\n</RCC>\n'

    with open(os.path.join(dirname, basename + '.qrc'), 'w') as f:
        f.write(contents)

def compile_rc(dirname):
    try:
        r = re.compile('.*\\\lib\\\site-packages$')
        paths = sys.path
        sitepath = ''
        for path in paths:
            if r.search(path):
                sitepath = path
        if not sitepath:
            return
        pyrccpath = '{}\PyQt4\pyrcc4.exe'.format(sitepath)

        basename = os.path.basename(dirname)
        qrc_file = os.path.join(dirname, basename + '.qrc')
        py_file = os.path.join(dirname, basename + '_rc.py')
        if not needsupdate(qrc_file, py_file):
            return
        pipe = subprocess.Popen([pyrccpath, qrc_file, '-o', py_file])
        pipe.wait()
    except Exception, e:
        print e

def needsupdate(src, targ):
    return not os.path.exists(targ) or os.path.getmtime(src) > os.path.getmtime(targ)

if __name__ == "__main__":
    flag = True
    while flag:
        dirname = raw_input("请输入资源目录：".decode('utf-8').encode('gbk'))
        prefix = raw_input("请输入资源前缀：".decode('utf-8').encode('gbk'))
        create_qrc(dirname, prefix)
        compile_rc(dirname)
        flag = False
