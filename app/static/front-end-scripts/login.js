$("document").ready(function() {
	$("#loginForm").submit(function (e) {
		$("#loginErrorMsg").text("");
		e.preventDefault();
		let form = document.getElementById("loginForm");
		let formData = new FormData(form);
		let request = $.ajax({
			url: "/login",
			type: "POST",
			data: Object.fromEntries(formData),
			dataType: "text",
		}).done(function(msg) {
			location.reload(true)
		}).fail(function(msg) {
			if (msg.status >= 300) {
				$("#loginErrorMsg").text(JSON.parse(msg.responseText).reason);
			}
		});
	});
});
