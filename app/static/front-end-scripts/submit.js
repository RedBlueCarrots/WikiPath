//Moves the buttons to the appropriate form
function redoButtons() {
    const buttons = $("#buttons").clone().html();
    $("#revealPathForm").remove();
    $("#removePathForm").remove();
    $("#path-" + ($("#submitForm .path-entry").length - 1)).parent().after(buttons);
    $("#revealPathForm").on("click", revealPath);
    $("#removePathForm").on("click", removePath);
}

function revealPath() {
    const formlength = $(' #submitForm .path-entry').length;
    const path = "path-" + formlength;
    let template = $("#inputTemplate").clone();
    template.find("input").attr({
        "name": path,
        "id": path
    })
    newInput = template.html();
    $("#pathEnd").before(newInput);
    redoButtons()
}

function removePath() {
    if ($("#submitForm .path-entry").length !== 1) {
        $(".path-entry").last().parent().parent().remove()
        redoButtons()
    }

}

$("document").ready(function () {
    $("#revealPathFormSmall").on("click", revealPath);
    $("#removePathFormSmall").on("click", removePath);
    revealPath();
})