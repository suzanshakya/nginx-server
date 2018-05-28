nginx-server
============

Run nginx server from command line as you would run python's SimpleHTTPServer

**Install** 
make  
export PATH=~/bin:$PATH


**Examples:**

Serve current directory in port 8000  
`# nginx-server.py`

Serve 'Movies' directory in port 8000  
`# nginx-server.py Movies`

Serve current directory in port 80  
`# sudo ~/bin/nginx-server.py . 80`
