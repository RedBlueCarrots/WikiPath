function revealPath(currentPath) {
    currentPath = currentPath.nextSibling.className.replace( /(?:^|\s)formPathHidden(?!\S)/g , '' );
    return currentPath;
}






currentpath = document.getElementsByClassName("formPathHidden")[0];
currentpath = document.getElementById("revealPathForm").addEventListener('click', revealPath(currentpath));