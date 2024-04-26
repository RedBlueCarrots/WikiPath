var inputs = document.querySelectorAll('.formPathHidden');
var index = 0;



function revealPath() {
    if (index < inputs.length) {
        inputs[index].removeAttribute("class")
        index++
    }
}

function removePath() {
    if (index > 0){
        index = index - 1;
        inputs[index].classList.add("formPathHidden");
    }
}


document.getElementById("revealPathForm").addEventListener("click", revealPath);
document.getElementById("removePathForm").addEventListener("click", removePath);