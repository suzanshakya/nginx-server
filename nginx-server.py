#!/usr/bin/env python
"""\
Usage: %prog [path:.] [port:8000]
"""

import os
import sys
import shutil

conf_template = """\
error_log /dev/stderr;
pid /tmp/nginx-server.py.pid;
worker_processes 1;

daemon off;
events {
    worker_connections 1024;
}

http {
    include mime.types;
    default_type application/octet-stream;
    access_log /dev/stdout;

    gzip             on;
    gzip_http_version 1.1;
    gzip_proxied     any;
    gzip_types       text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_disable     "MSIE [1-6]\.";
    gzip_comp_level  6;

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
        path = "."
    root = get_realpath(path)
    try:
        port = sys.argv[2]
    except:
        port = "8000"

    address = "http://localhost:%s" % port

    conf = "/tmp/nginx.conf"
    mime_source = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mime.types')
    mime_dest = '/tmp/mime.types'
    shutil.copyfile(mime_source, mime_dest)
    with open(conf, "w") as f:
        conf_data = conf_template % dict(root=root, port=port)
        f.write(conf_data)
    print >>sys.stderr, "%r serving in %r" % (root, address)
    os.execvp("nginx", ["nginx", "-c", conf])

main()
