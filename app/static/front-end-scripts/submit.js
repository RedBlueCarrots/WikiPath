

function redoButtons() {
    const buttons = '<button type="button" class="btn btn-primary d-none d-md-block col-0 col-md-1" id="revealPathForm">+</button><button type="button" class="btn btn-focus d-none d-md-block col-0 col-md-1" id="removePathForm">-</button>'
    $("#revealPathForm").remove()
    $("#removePathForm").remove()
    $("#path-"+($("#submitForm .path-entry").length-1)).parent().after(buttons);
    $("#revealPathForm").on("click", revealPath);
    $("#removePathForm").on("click", removePath);
    console.log("here")
}

function revealPath() {
    const newInput = `<div class="row mb-3 g-0"><div class= "col-12 col-md-10"> <input class="path-entry form-control mx-0" id="path-${$("#submitForm .path-entry").length}" name="path-${$("#submitForm .path-entry").length}" type="text" value=""></div></div>`
    $("#pathEnd").before(newInput);
    redoButtons()
}

function removePath() {
    if ($("#submitForm .path-entry").length !== 1) {
        $(".path-entry").last().parent().parent().remove()
        redoButtons()
    }

}

$("document").ready(function() {
    redoButtons()
    $("#revealPathFormSmall").on("click", revealPath);
    $("#removePathFormSmall").on("click", removePath);
    revealPath();
})