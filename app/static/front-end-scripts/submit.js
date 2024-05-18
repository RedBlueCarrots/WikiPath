//Moves the buttons to the appropriate form
function redoButtons() {
    const buttons = $("#buttons").clone().html();
    $("#revealPathForm").remove();
    $("#removePathForm").remove();
    $("#path-" + ($("#submitForm .path-entry").length - 1)).parent().after(buttons);
    $("#revealPathForm").on("click", revealPath);
    $("#removePathForm").on("click", removePath);
    if ($("#submitForm .path-entry").length == 1) {
        $("#removePathForm").addClass("faded");
        $("#removePathFormSmall").addClass("faded");
    }
    else {
        $("#removePathFormSmall").removeClass("faded");

    }
}

function revealPath() {
    const formlength = $(' #submitForm .path-entry').length;
    const newId = "path-" + formlength;
    let template = $("#inputTemplate").clone();
    template.find("input").attr({
        "name": newId,
        "id": newId
    })
    const newInput = template.html();
    $("#pathEnd").before(newInput);
    redoButtons()
    return newId
}


function removePath() {
    if ($("#submitForm .path-entry").length !== 1) {
        $(".path-entry").last().parent().parent().remove();
        redoButtons();
    }

}

function addError(error, id) {
    const errorTemplate = $("#errorTemplate").clone();
    errorTemplate.find("div").html(error);
    const errorElem = errorTemplate.html();
    $("#" + id).parent().parent().append(errorElem);
}

function addPreviousPaths(articleList) {
    let numArticles = articleList.length;
    //articleList includes starting and ending articles, so ignore them in the loop
    for (let entry = 1; entry < numArticles - 1; entry++) {
        const newId = revealPath();
        $("#" + newId).attr("value", articleList[entry]);
    }
    //i.e. articleList contained either just start and end, or nothing at all
    if (numArticles <= 2) {
        revealPath();
    }

}

function addPathErrors(errorList) {
    //For every non-empty path entry, if its value is in the list of error articles, 
    //add an error message below
    $(".path-entry[value!='']").each(function (index) {
        errorList.includes($(this).attr("value")) && addError($(this).attr("value") + " is not a valid article", $(this).attr("id"));
    })
}

function addPathErrors(errorList, articleList) {
    let path_entries = $(".path-entry[value!='']");

    if(articleList[0] != "") {
        for(let i = 0; i < articleList.length; i++) {
            if(errorList.includes(articleList[i])) {
                if (i == 0) {
                    addError(articleList[i] + " does not link to " + articleList[i + 1], path_entries.eq(i).attr("id"));
                } else {
                    addError(articleList[i] + " does not link to " + articleList[i + 1], path_entries.eq(i-1).attr("id"));
                }
                
            }
        }
    }
}

$("document").ready(function () {
    $("#revealPathFormSmall").on("click", revealPath);
    $("#removePathFormSmall").on("click", removePath);
    let articleList = $("#submitForm").data("path").split("|");
    addPreviousPaths(articleList);
    const articleErrorList = $("#submitForm").data("article-errors").split("|");
    const pathErrorList = $("#submitForm").data("path-errors").split("|");
    addArticleErrors(articleErrorList);
    addPathErrors(pathErrorList, articleList);
})
