let buttonClicked = "";

$("document").ready(function () {
	$("#loginForm").submit(function (e) {
		$("#loginErrorMsg").text("");
		e.preventDefault();
		let form = document.getElementById("loginForm");
		//gets data entered in the form and converts it to json
		let formData = Object.fromEntries(new FormData(form));
		let request = $.ajax({
			//The id of the submit buttons is the route
			url: buttonClicked,
			type: "POST",
			data: formData,
			dataType: "text",
		}).done(function (msg) {
			location.reload(true)
		}).fail(function (msg) {
			if (msg.status >= 300) {
				$("#loginErrorMsg").text(JSON.parse(msg.responseText).reason);
			}
		});
	});

	$(".loginFormButton").click(function () {
		buttonClicked = $(this).data("link");
	})

	$("#loginPopup").on("show.bs.modal", () => {
		$("#loginErrorMsg").text("");
	});

});

function logout(url) {
	window.location = url;
}
