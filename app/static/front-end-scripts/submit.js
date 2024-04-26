

function revealPath() {
    const newInput = `<div><input class="path-entry" id="path-${$("#submitForm .path-entry").length}" name="path-${$("#submitForm .path-entry").length}" type="text" value=""></div>`
    $("#submitForm").append(newInput);
}

function removePath() {
    $(".path-entry").last().remove()
}

$("document").ready(function() {
    $("#revealPathForm").on("click", revealPath);
    $("#removePathForm").on("click", removePath);
})