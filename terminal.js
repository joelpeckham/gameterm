console.log('Terminal.js Loaded!');
var term = new Terminal();
var fitAddon = new FitAddon.FitAddon();

term.loadAddon(fitAddon);
term.open(document.getElementById('terminal'));
fitAddon.fit();

function getTermLine(){
	console.log(term.buffer.cursorY)
	return term.buffer.getLine(term.buffer.cursorY).translateToString(true)
}
term.onKey(e => {
    //console.log("Key Code: " + e.domEvent.keyCode)
    const printable = !e.domEvent.altKey && !e.domEvent.altGraphKey && !e.domEvent.ctrlKey && !e.domEvent.metaKey;
    var key = e.domEvent.keyCode
    //simulateKey(e.domEvent.keyCode,"press")
	//simulateKey(e.domEvent.keyCode)
	

	var kdEvent = new KeyboardEvent('keydown', e.domEvent);
	document.getElementById('code').dispatchEvent(kdEvent);
	var kpEvent = new KeyboardEvent('keypress', e.domEvent);
	document.getElementById('code').dispatchEvent(kpEvent);
});
