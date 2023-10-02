$('#college_registration').on("submit", function(event){
    console.log("this")
    collegeRegistrationForm = $( this ).serializeArray();
    event.preventDefault();
    var collegeRegistrationFormObject = {};
    $.each(collegeRegistrationForm,
        function(i, v) {
            collegeRegistrationFormObject[v.name] = v.value;
        });

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: 'post',
        headers: {'X-CSRFToken': csrftoken, 'Accept': 'application/json'},
        url: '/college-registration',
        data: collegeRegistrationFormObject,
        success: function(response) {
            if (response.message === 'success'){
                location.href=response.redirect_url
            }else{
                $.each(response.error, function(index,jsonObject){
                    $.each(jsonObject, function(key,val){
                        alert(index+" : "+val);
                    });
                });
            }

        }
    })
})