console.log('Terminal.js Loaded!');
var term = new Terminal({fontFamily:"'IBM Plex Mono', monospace"});
var fitAddon = new FitAddon.FitAddon();

term.loadAddon(fitAddon);
term.open(document.getElementById('terminal'));
fitAddon.fit();


function getTermLine(){
	return term.buffer.getLine(term.buffer.cursorY).translateToString(true)
}


term.onKey(e => {kbe = new KeyboardEvent('keypress', e.domEvent); term.element.dispatchEvent(kbe);});
