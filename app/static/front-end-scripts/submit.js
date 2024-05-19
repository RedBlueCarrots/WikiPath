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
    if(id == "pathStart") {
        $("#" + id).after(errorElem);
    }else {
        $("#" + id).parent().parent().append(errorElem);
    }
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

function addArticleErrors(errorList) {
    //For every non-empty path entry, if its value is in the list of error articles, 
    //add an error message below
    $(".path-entry[value!='']").each(function (index) {
        errorList.includes($(this).attr("value")) && addError($(this).attr("value") + " is not a valid article", $(this).attr("id"));
    })
}

function addPathErrors(errorList, otherErrorList) {
    let path_entries = $("#pathStart").add($(".path-entry[value!='']")).add($("#pathEnd"));

    path_entries.each(function (index) {
        errorList.includes($(this).attr("value")) && addError($(this).attr("value") + " does not link to " + path_entries.eq(index + 1).attr("value"), $(this).attr("id"));
    })
}

$("document").ready(function () {
    $("#revealPathFormSmall").on("click", revealPath);
    $("#removePathFormSmall").on("click", removePath);
    let articleList = $("#submitForm").data("path").split("|");
    addPreviousPaths(articleList);
    const articleErrorList = $("#submitForm").data("article-errors").split("|");
    const pathErrorList = $("#submitForm").data("path-errors").split("|");
    addArticleErrors(articleErrorList);
    addPathErrors(pathErrorList, articleErrorList);
})
