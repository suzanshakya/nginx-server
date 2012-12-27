#!/usr/bin/env python
"""\
Usage: %prog [path:.] [port:8000]
"""

import os
import sys
import webbrowser

conf_template = """\
worker_processes 1;

daemon off;
events {
    worker_connections 1024;
}

http {
    include /usr/local/etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen %(port)s;

        location / {
            root "%(root)s/";
            autoindex on;
            index index.html index.htm;
        }
    }
}
"""

def get_realpath(path):
    return os.path.realpath(os.path.join(os.path.abspath(os.curdir), path))

def main():
    try:
        path = sys.argv[1]
    except:
        path = '.'
    root = get_realpath(path)
    try:
        port = sys.argv[2]
    except:
        port = "8000"

    address = "http://localhost:%s" % port

    conf = '/tmp/nginx.conf'
    with open(conf, 'w') as f:
        conf_data = conf_template % dict(root=root, port=port)
        f.write(conf_data)
    print >>sys.stderr, "%r serving in %r" % (root, address)
    webbrowser.open(address)
    os.execvp('nginx', ['nginx', '-c', conf])

main()
