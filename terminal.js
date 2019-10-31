console.log('Terminal.js Loaded!');
var term = new Terminal({fontFamily:"'IBM Plex Mono', monospace"});
var fitAddon = new FitAddon.FitAddon();

term.loadAddon(fitAddon);
term.open(document.getElementById('terminal'));
fitAddon.fit();

function getTermLine(lineNum){
	lineNum = (lineNum == undefined) ? term.buffer.cursorY : lineNum
	line = term.buffer.getLine(lineNum)
	lineString = ''
	while (line.isWrapped){lineString = line.translateToString(true) + lineString; lineNum--; line = term.buffer.getLine(lineNum);}
	return line.translateToString(true) + lineString;
}

term.onKey(e => {kbe = new KeyboardEvent('keypress', e.domEvent); document.getElementById("keyTrigger").dispatchEvent(kbe);});
