function revealSubmit() {
    alert("hey the button works!!!");
    document.getElementById("hiddenSubmit").className = "visible";
}


document.getElementById("revealsubmit").addEventListener("click", revealSubmit);