

function redoButtons() {
    const buttons = `<button type="button" class="btn btn-focus d-none d-md-block col-0 col-md-1" id="removePathForm">-</button>
    <button type="button" class="btn btn-primary d-none d-md-block col-0 col-md-1" id="revealPathForm">+</button>`
    $("#revealPathForm").remove()
    $("#removePathForm").remove()
    $("#path-"+($("#submitForm .path-entry").length-1)).parent().after(buttons);
    $("#revealPathForm").on("click", revealPath);
    $("#removePathForm").on("click", removePath);
}

function revealPath() {
    const newId = "path-" + $("#submitForm .path-entry").length;
    const newInput = `
    <div class="row mb-3 g-0">
        <div class= "col-12 col-md-10"> 
            <input class="path-entry form-control mx-0" id="${newId}" name="${newId}" type="text" value="">
        </div>
    </div>`
    $("#pathEnd").before(newInput);
    redoButtons()
    return newId
}

function removePath() {
    if ($("#submitForm .path-entry").length !== 1) {
        $(".path-entry").last().parent().parent().remove()
        redoButtons()
    }

}

$("document").ready(function() {
    $("#revealPathFormSmall").on("click", revealPath);
    $("#removePathFormSmall").on("click", removePath);
    let articleList = $("#submitForm").data("path").split("|");
    let numArticles = articleList.length;
    for (let entry = 1; entry < numArticles-1; entry++){
        const newId = revealPath();
        $("#"+newId).attr("value", articleList[entry]);
    }
    if (numArticles===2){
        revealPath();
    }
})