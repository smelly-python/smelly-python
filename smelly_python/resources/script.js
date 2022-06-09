var codeSmells;

function setSmells(smells) {
    codeSmells = smells;
}

function addToDictionary(dict, key, value) {
    if (!(key in dict)) {
        dict[key] = [];
    }
    dict[key].push(value);
}

window.onload = async function () {
    // Add line numbers
    for (const block of document.getElementsByClassName('hljs')) {
        hljs.lineNumbersBlock(block);
    }

    // TODO: handle multiple smells on one line
    const smellsPerLine = {};
    for (smell of codeSmells) {
        var currentLine = smell.location.line;
        do {
            addToDictionary(smellsPerLine, currentLine, smell);
            currentLine += 1;
        } while (currentLine <= smell.location.end_line && smell.location.end_line !== null);
    }

    var trs;
    do {
        trs = document.querySelectorAll('#code-block > code > table > tbody > tr');
        // Wait for the table to exist, as the plugin does an async function
        // that it doesn't return the Promise of :(
        await new Promise(r => setTimeout(r, 1));
    } while (trs.length === 0);
    for (const [index, tr] of trs.entries()) {
        const line = index + 1;
        if (line in smellsPerLine) {
            // TODO: handle multiple smells on one line
            const smell = smellsPerLine[line][0];
            tr.classList.add(smell.type);
            tr.classList.add('code-smell');

            const message = document.createElement('span');
            message.className = 'code-smell-message';
            message.innerText = smell.message;
            tr.appendChild(message);
            message.style.setProperty('margin-left', -message.clientWidth / 2 + 'px');
        }
        tr.setAttribute('id', `line-${line}`);
    }
    // Scroll to line number if necessary
    if (window.location.hash !== '') {
        window.scrollTo({ top: document.querySelector(window.location.hash).offsetTop});
    }
}
