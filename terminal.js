class TerminalLine {
  constructor(prompt, content) {
    this.prompt = height;
    this.content = content;
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

term.write("Hello!")
