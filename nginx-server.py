#!/usr/bin/env python
"""\
Usage: %prog [path:.] [port:8000]
"""

import os
import sys
import subprocess

conf_template = """\
error_log stderr;
worker_processes 1;

daemon off;
events {
    worker_connections 1024;
}

http {
    %(include_mime)s
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

def include_mime():
    # default location when nginx is installed by home brew in Mac OS
    default_location = "/usr/local/etc/nginx/mime.types"
    if os.path.exists(default_location):
        mime_file = default_location
    else:
        file_to_locate = "*/nginx/mime.types"
        proc = subprocess.Popen(["locate", file_to_locate], stdout=subprocess.PIPE)
        output, error = proc.communicate()
        files = filter(os.path.exists, output.split("\n"))
        if files:
            mime_file = files[0]
        else:
            print >>sys.stderr, "We could not locate %r file." % file_to_locate
            mime_file = None
    if mime_file:
        return "include %s;" % mime_file
    else:
        return ""

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
    with open(conf, "w") as f:
        conf_data = conf_template % dict(root=root, port=port, include_mime=include_mime())
        f.write(conf_data)
    print >>sys.stderr, "%r serving in %r" % (root, address)
    os.execvp("nginx", ["nginx", "-c", conf])

main()
