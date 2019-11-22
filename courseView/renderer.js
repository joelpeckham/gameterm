// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.

const {ipcRenderer} = require('electron')

var os = require('os');
var pty = require('node-pty');
var Terminal = require('xterm').Terminal;
var FitAddon = require('xterm-addon-fit').FitAddon;

// Initialize node-pty with an appropriate shell
const shell = process.env[os.platform() === 'win32' ? 'COMSPEC' : 'SHELL'];
const ptyProcess = pty.spawn(shell, [], {
  name: 'xterm-color',
  cols: 100,
  rows: 10,
  cwd: process.cwd(),
  env: process.env
});

// Initialize xterm.js and attach it to the DOM
const xterm = new Terminal({	cursorStyle:'bar',
											    fontSize:16,fontFamily:"'IBM Plex Mono', monospace",
													allowTransparency:true,
													theme:{background: 'rgba(255, 255, 255, 0.0)'}
												  });

// Initialize xterm.js fit addon
const fitAddon = new FitAddon();
xterm.loadAddon(fitAddon);

// Attach xterm to DOM and start xterm.
xterm.open(document.getElementById('terminal'));
fitAddon.fit();

// Setup communication between xterm.js and node-pty
xterm.onData(data => ptyProcess.write(data));
ptyProcess.on('data', function (data) {
  xterm.write(data);
});

ipcRenderer.on('resize', (event) => { fitAddon.fit(); } )
