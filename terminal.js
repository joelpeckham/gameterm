class TerminalLine {
  constructor() {
    this.height = height;
  }
}

var term = new Terminal({	cursorStyle:'bar',
													fontSize:16,fontFamily:"'IBM Plex Mono', monospace",
													allowTransparency:true,
													theme:{background: 'rgba(255, 255, 255, 0.0)'}
												});

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

function getCursorY(){return term.buffer.cursorY;}

function getTopTermLineNum(){return term.buffer.baseY;}

function getLastTermLineNum(){
	for (i = term.buffer.length - 1; i >= term.buffer.baseY; i--){
		lineCandidate = term.buffer.getLine(i).translateToString().trim();
		if(lineCandidate && lineCandidate != "") return i;
	}
	return 0;
}

term.onKey(e => {
	let kbe = new KeyboardEvent('keypress', e.domEvent);
	document.getElementById("keyTrigger").dispatchEvent(kbe);
});
