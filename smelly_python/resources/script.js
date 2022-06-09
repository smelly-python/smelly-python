var code_smells;

function setSmells(smells) {
    code_smells = smells;
}

window.onload = async function () {
    for (const block of document.getElementsByClassName('hljs')) {
        hljs.lineNumbersBlock(block);
    }

    // TODO: handle multiple smells on one line
    const smells_per_line = Object.assign({}, ...code_smells.map(smell => ({[smell.location.line]: smell})));

    var trs;
    do {
        trs = document.querySelectorAll('#code-block > code > table > tbody > tr');
        // Wait for the table to exist, as the plugin does an async function
        // that it doesn't return the Promise of :(
        await new Promise(r => setTimeout(r, 1));
    } while (trs.length === 0);
    for (const [index, tr] of trs.entries()) {
        const line = index + 1;
        if (line in smells_per_line) {
            // TODO: handle multiple smells on one line
            tr.className += smells_per_line[line].type
        }
        tr.setAttribute('id', `line-${line}`);
    }
}
