$('#user_registration').on("submit", function(event){
    userForm = $( this ).serializeArray();
    console.log("hello2")
    event.preventDefault();
    var userFormObject = {};
    $.each(userForm,
        function(i, v) {
            userFormObject[v.name] = v.value;
        });

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: 'post',
        headers: {'X-CSRFToken': csrftoken, 'Accept': 'application/json'},
        url: '/user-registration',
        data: userFormObject,
        success: function(response) {
            alert(response.message)
            document.location.reload(true);
        }
    })
})

$('.user_delete').on("click", function(){
    user_id = $(this).attr("id");
    user_id_split = user_id.split("_");
    console.log(user_id);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: 'delete',
        headers: {'X-CSRFToken': csrftoken, 'Accept': 'application/json'},
        url: `/user-crud/${user_id_split[1]}`,
        success: function(response) {
            alert(response.message)
            document.location.reload(true);
        }
    })
})

$('.user_login_allow').on("click", function(){
    user_id = $(this).attr("id");
    user_id_split = user_id.split("_");
    var userCrudObject = {'action': $(this).attr("action")};
    console.log(userCrudObject)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.ajax({
        type: 'put',
        headers: {'X-CSRFToken': csrftoken, 'Accept': 'application/json'},
        url: `/user-crud/${user_id_split[1]}`,
        data: userCrudObject,
        success: function(response) {
            alert(response.message)
            document.location.reload(true);
        }
    })
})