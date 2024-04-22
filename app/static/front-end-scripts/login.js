$("document").ready(function() {
	$("#loginForm").submit(function (e) {
		e.preventDefault();
		let form = document.getElementById("loginForm");
		let formData = new FormData(form);
		let request = $.ajax({
			url: "/login",
			type: "POST",
			data: Object.fromEntries(formData),
		});
		request.done(function(msg) {
			console.log(msg);
		});
	});
});
