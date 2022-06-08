function alertFunction() {
    var attribute = this.getAttribute("data-range")
    console.log("clicked on highlight")
    alert("Clicked on the code at range: " + attribute);
}

// function link_code_highlights() {

window.onload = function () {
    const el = document.querySelectorAll('.line-highlight')
    console.log("found: " + el.length + " highlights")
    for (var i = 0; i < el.length; i++) {
        el[i].addEventListener('click', alertFunction, false)
    }
}