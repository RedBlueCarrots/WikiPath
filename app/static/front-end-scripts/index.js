$("document").ready(function () {
	let currentPage = $("#pagination").data("page");
	let totalPage = $("#pagination").data("totalpages");
	for (let i = 3; i > totalPage; i--) {
		$(".page-item-"+i).addClass("d-none");
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
		$(".page-item-1>.page-link").text(totalPage-1);
		$(".page-item-2").addClass("active");
		$(".page-item-2>.page-link").text(totalPage);
		$(".page-item-3>.page-link").text(totalPage+1);
	}
	for (let i = 1; i <= 3; i++) {
		$(".page-item-"+i + ">.page-link").attr("href", "/?page=" + $(".page-item-"+i + ">.page-link").text());
	}
	$(".page-link-start").attr("href", "/?page=1");
	$(".page-link-end").attr("href", "/?page="+totalPage);
});