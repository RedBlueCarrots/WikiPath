$("document").ready(function () {
	let currentPage = $("#pagination").data("page");
	let totalPage = $("#pagination").data("totalpages");
	for (let i = 3; i > totalPage; i--) {
		$(".page-item-"+i).addClass("d-none");
	}
	URLvars =  location.search.split("?");
	newPath = location.pathname+"?"
	if (URLvars.length === 2) {
		URLvars = URLvars[1].split("&");
		for (let i = 0; i < URLvars.length; i++) {
			if (URLvars[i].indexOf("page=") === -1){
				newPath += URLvars[i] + "&";
			}
	}
	}
	if (currentPage === 1) {
		$(".page-item-1>.page-link").text("1");
		$(".page-item-1").addClass("active");
		$(".page-item-2>.page-link").text("2");
		$(".page-item-3>.page-link").text("3");
	} else if (currentPage === totalPage && currentPage !== 2) {
		$(".page-item-1>.page-link").text(totalPage-2);
		$(".page-item-3").addClass("active");
		$(".page-item-2>.page-link").text(totalPage-1);
		$(".page-item-3>.page-link").text(totalPage);
	} else {
		$(".page-item-1>.page-link").text(currentPage-1);
		$(".page-item-2").addClass("active");
		$(".page-item-2>.page-link").text(currentPage);
		$(".page-item-3>.page-link").text(currentPage+1);
	}
	for (let i = 1; i <= 3; i++) {
		$(".page-item-"+i + ">.page-link").attr("href", newPath + "page=" + $(".page-item-"+i + ">.page-link").text());
	}
	$(".page-link-start").attr("href", newPath + "page=1");
	$(".page-link-end").attr("href", newPath + "page="+totalPage);
});