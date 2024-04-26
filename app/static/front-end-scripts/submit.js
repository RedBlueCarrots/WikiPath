var inputs = document.querySelectorAll('.formPathHidden');
var index = 0;



function revealPath() {
    if (index < inputs.length) {
        inputs[index].removeAttribute("class")
        index++
    }
}


document.getElementById("revealPathForm").addEventListener("click", revealPath);