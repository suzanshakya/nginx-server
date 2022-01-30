#!/usr/bin/env python
"""\
Usage: %prog [path:.] [port:8000]
"""

from __future__ import print_function
import os
import sys
import shutil
import socket
from tempfile import mkdtemp

conf_template = """\
error_log /dev/stderr;
pid %(temp_dir)s/nginx-server.py.pid;
worker_processes 1;

daemon off;
events {
    worker_connections 1024;
}

http {
    include mime.types;
    types_hash_max_size 2048;
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

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def is_port_in_use(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s.connect_ex(('localhost', port)) == 0
    finally:
        s.close()

def get_realpath(path):
    return os.path.realpath(os.path.join(os.path.abspath(os.curdir), path))

def main():
    try:
        path = sys.argv[1]
    except:
        path = "."

    if not os.path.exists(path):
        raise SystemExit("Directory %r doesn't exist." % path)
    elif not os.path.isdir(path):
        raise SystemExit("%r is not a directory." % path)

    root = get_realpath(path)

    try:
        port = sys.argv[2]
    except:
        port = 8000
        while is_port_in_use(port):
            print("Port %d is already in use. Trying %d" % (port, port+1), file=sys.stderr)
            port += 1

    address = "http://%s:%s" % (get_ip(), port)

    temp_dir = mkdtemp(prefix="nginx-server-")

    mime_source = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mime.types')
    mime_dest = os.path.join(temp_dir, "mime.types")
    shutil.copyfile(mime_source, mime_dest)

    conf = os.path.join(temp_dir, "nginx.conf")
    with open(conf, "w") as f:
        conf_data = conf_template % dict(root=root, port=port, temp_dir=temp_dir)
        f.write(conf_data)

    print("%r serving in %r" % (root, address), file=sys.stderr)
    try:
        os.execvp("nginx", ["nginx", "-c", conf])
    except FileNotFoundError:
        sys.exit("FAILED: nginx not found!")

main()
