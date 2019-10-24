
console.log('Terminal.js Loaded!')
var term = new Terminal();
var fitAddon = new FitAddon.FitAddon();
var cmdhistory = [];
var historyLocation = null;
const promptString = "$ "

term.loadAddon(fitAddon);
term.open(document.getElementById('terminal'));
fitAddon.fit();

function prompt(term) {
    term.write("\r\n" + promptString);
}

function getTerminalLine(yPos){
    // Takes int returns string
    var lastLine = term._core.buffer.lines._array[yPos].translateToString();
    for (i = yPos; term._core.buffer.lines._array[i].isWrapped; i--){
        lastLine = term._core.buffer.lines._array[i-1].translateToString() + lastLine;
    }
    return lastLine.trim();
}

function writeToLine(lineContent, yPos, prompt){
    // Takes string, int, and bool returns void;
    term._core.buffer.lines._array[yPos].fill('');
    term._core.buffer.x = 0;
    term.write((prompt ? promptString : "") + lineContent);
}

function processLine(term, line){
    var args = line.split(" ");
    if (line.toUpperCase() == "CLEAR"){
        term.writeln('')
        setTimeout(function(){
            term.clear();
        }, 1);
    }
    else if (args[0].toUpperCase() == "ECHO"){
        if (line.slice(5) != ""){
            term.writeln('');
            term.write(line.slice(5));
        }
    }
};

function runTerminal() {
    if (term._initialized) {
        return;
    }
    term._initialized = true;

    term.prompt = () => {
        term.write("\r\n" + promptString);
    };

    term.write(promptString)

    var lastTyped = 0;
    term.onKey(e => {
        //console.log("Key Code: " + e.domEvent.keyCode)
        const printable = !e.domEvent.altKey && !e.domEvent.altGraphKey && !e.domEvent.ctrlKey && !e.domEvent.metaKey;
        var key = e.domEvent.keyCode

        if (key === 13) { //Return or Enter key
            var line = getTerminalLine(term._core.buffer.y).slice(2);
            if (line != ''){
                processLine(term, line);
                console.log(line);
                lastTyped = 0;
                cmdhistory.push(line)
                historyLocation = cmdhistory.length;
            }
            prompt(term)
        } 
        else if (key === 8) { //Backspace or delete key
            // Do not delete the prompt
            if (term._core.buffer.x > 2) {
                term.write('\b \b');
            }
        } 
        else if (key === 37) { //Left arrow
            if (term._core.buffer.x > 2) {
                term.write(e.key);
            }
        } 
        else if (key === 39) { //Right arrow
            if (term._core.buffer.x < (lastTyped + 1)) {
                term.write(e.key);
            }
        } 
        else if (key === 38) { //Up arrow
            if (historyLocation > 0) {
                historyLocation -= 1;
                writeToLine(cmdhistory[historyLocation],term._core.buffer.y,true)
            }
        } 
        else if (key === 40) { //Down arrow
            cmdhistory.push("");
            if (historyLocation < cmdhistory.length - 1) {
                historyLocation += 1;
                writeToLine(cmdhistory[historyLocation],term._core.buffer.y,true)
            }
            cmdhistory.pop();
        } 
        else if (printable) {
            term.write(e.key);
            lastTyped = term._core.buffer.x;
        }
    });
}
const input = document.querySelector('textarea');
input.addEventListener('input', processLine(term,"python"));
runTerminal();
