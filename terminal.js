console.log('Terminal.js Loaded!');
var term = new Terminal();
var fitAddon = new FitAddon.FitAddon();

term.loadAddon(fitAddon);
term.open(document.getElementById('terminal'));
fitAddon.fit();


function getTermLine(){
	return term.buffer.getLine(term.buffer.cursorY).translateToString(true)
}


term.onKey(e => {term.element.dispatchEvent(new KeyboardEvent(e.domEvent.type, e.domEvent))});
