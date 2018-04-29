function signup(){
//alert("add");
	var post= {'username':' ','password':' ','email':' ','group':''};
	post.username = $('#username').val();
	post.password = $('#password').val();
	post.email = $('#email').val();
    post.group = $('#group').val();

	$.ajax({
		url: '/signup',
		type: 'POST',
		dataType: 'json',
		data: JSON.stringify(j),
		contentType: "application/json",
		success: function(response){
		}
	})
}
function login(){
	var post= {'username':' ','password':' '};
	post.username = $('#login_name').val();
	post.password = $('#login_pass').val();
	$.ajax({
		url: '/login',
		type: 'POST',
		dataType: 'json',
		data: JSON.stringify(j),
		contentType: "application/json",
		success: function(response){
			if(response.status === "OK"){
			    alert("SUCCESS")
			}
			else if(response.status === "ERROR"){
				alert("Invalid login information")
			}
			else{
				alert(resonse.status)
			}
		}
	})
}