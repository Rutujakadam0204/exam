$('#login').on("submit", function(event){
    loginForm = $( this ).serializeArray();
    event.preventDefault();
    var loginFormObject = {};
    $.each(loginForm,
        function(i, v) {
            loginFormObject[v.name] = v.value;
        });

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: 'post',
        headers: {'X-CSRFToken': csrftoken, 'Accept': 'application/json'},
        url: '/login',
        data: loginFormObject,
        success: function(response) {
            if ("message" in response){
                alert(response.message)
            }
                location.href=response.redirect_url
        }
    })
})