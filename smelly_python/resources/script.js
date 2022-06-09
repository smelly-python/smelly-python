var codeSmells;

function setSmells(smells) {
    codeSmells = smells;
}

window.onload = async function () {
    for (const block of document.getElementsByClassName('hljs')) {
        hljs.lineNumbersBlock(block);
    }

    // TODO: handle multiple smells on one line
    const smellsPerLine = Object.assign({}, ...codeSmells.map(smell => ({[smell.location.line]: smell})));

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
            const smell = smellsPerLine[line];
            tr.classList.add(smell.type);
            tr.classList.add('code-smell');

            const message = document.createElement('span');
            message.className = 'code-smell-message';
            message.innerText = smell.message;
            tr.appendChild(message);
            message.style.setProperty('margin-left', -message.clientWidth / 2 + 'px');
            console.log(message)
        }
        tr.setAttribute('id', `line-${line}`);
    }
}
