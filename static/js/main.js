$(function() {
    $('#btnSignUp').click(function() {
        alert("add");
        var post= {'username':' ','password':' ','email':' ','group':''};
        post.username = $('#username').val();
        post.password = $('#password').val();
        post.email = $('#email').val();
        post.group = $('#group').val();

        $.ajax({
            url: '/signUp',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify(j),
            contentType: "application/json",
            success: function(response){
            }
        });
    });
});