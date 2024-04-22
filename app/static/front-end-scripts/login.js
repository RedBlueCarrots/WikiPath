$("document").ready(function() {
	$("#loginForm").submit(function (e) {
		e.preventDefault();
		let form = document.getElementById("loginForm");
		let formData = new FormData(form);
		let request = $.ajax({
			url: "/login",
			type: "POST",
			data: Object.fromEntries(formData),
			dataType: "json",
		});
		request.done(function(msg) {
			
		});
		request.fail(function(msg) {
			if (msg.status >= 300) {
				$("#loginErrorMsg").text(JSON.parse(msg.responseText).reason);
			}
		});
	});
});
