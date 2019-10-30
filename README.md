# gameterm
Teaching computing concepts through a "gameified" command line.
This is an open source project by Joel Peckham and Professor Robert Ordóñez of Southern Adventist University.

# how to run on local system

First clone or download the project.

For gameterm to run correctly, the gameterm-master directory must be hosted by an HTTP server.
This can be easily achieved by changing your working directory to the gameterm-master directory like this:
```
cd ~/user/Downloads/gameterm-master
```
Start the HTTP server like this:
```
python -m SimpleHTTPServer
```
After the HTTP server is running, http://0.0.0.0:8000/index.html may be opened in your browser.
