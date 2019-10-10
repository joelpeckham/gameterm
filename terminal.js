
var term = new Terminal();
var fitAddon = new FitAddon.FitAddon();
var cmdhistory = [];
var historyLocation = null;

term.loadAddon(fitAddon);
term.open(document.getElementById('terminal'));
fitAddon.fit();


function runFakeTerminal() {
    if (term._initialized) {
        return;
    }

    term._initialized = true;

    term.prompt = () => {
        term.write('\r\n$ ');
    };

    term.write('$ ')

    var lastTyped = 0;
    term.onKey(e => {
        //console.log("Key Code: " + e.domEvent.keyCode)
        const printable = !e.domEvent.altKey && !e.domEvent.altGraphKey && !e.domEvent.ctrlKey && !e.domEvent.metaKey;
        var key = e.domEvent.keyCode

        if (key === 13) { //Return or Enter key
            var lastLine = term._core.buffer.lines._array[term._core.buffer.y].translateToString().trim().slice(2);
            processLine(lastLine);
            lastTyped = 0;
            historyLocation = cmdhistory.length;
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
            console.log(cmdhistory);
            if (historyLocation > 0) {
                term._core.buffer.lines._array[term._core.buffer.y].fill('');
                term._core.buffer.x = 0;
                historyLocation -= 1;
                term.write("$ " + cmdhistory[historyLocation]);
            }
        } 
        else if (key === 40) { //Down arrow
            console.log(cmdhistory);
            cmdhistory.push("");
            if (historyLocation < cmdhistory.length - 1) {
                term._core.buffer.lines._array[term._core.buffer.y].fill('');
                term._core.buffer.x = 0;
                historyLocation += 1;
                term.write("$ " + cmdhistory[historyLocation]);
            }
            cmdhistory.pop();
        } 
        else if (printable) {
            term.write(e.key);
            lastTyped = term._core.buffer.x;
        }
    });
}

function processLine(line){
    var args = line.split(" ");
    if (line != ''){
        cmdhistory.push(line)
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
    }
};

function prompt(term) {
    term.write('\r\n$ ');
}

runFakeTerminal();