$(function() {
    'use strict';

    const div_list_users = $('#list-users');

    const input_users_json = $('#users-json');

    let input_modal_username = $('#username-user');
    let input_modal_email = $('#email-user');
    let input_modal_password = $('#password-user');

    var users = [];

    function create_user_card_html(username, email) {
        return `<div class="col-sm-6 mb-3"><div class="card"><div class="card-body" style="padding: 15px;"><h5 class="card-title">${username}
                <button class="close close-card-user" type="button" id="${username}" style="color: white" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">×</span></button></h5>
                <h6 class="card-subtitle mb-0 text-muted">${email}</h6></div></div></div>`
    }

    $('#btn-add-user-modal').click(function (e) {
        if ( (input_modal_username.val() === "") && (input_modal_email.val() === "") ) {
            input_modal_email.focus();
        } else {
            let card_user_html = create_user_card_html(input_modal_username.val(), input_modal_email.val());

            let user_json = JSON.stringify([{
                "username": input_modal_username.val(),
                "email": input_modal_email.val(),
                "password": input_modal_password.val()
            }]);

            if (input_users_json.val() === "") {
                input_users_json.val(user_json);
                div_list_users.append(card_user_html);
            } else {
                if (user_exists(input_modal_username.val())) {
                    alert('usuário já cadastrado');
                } else {
                    let all_users_json = JSON.parse(input_users_json.val());
                    all_users_json.push({
                        "username": input_modal_username.val(),
                        "email": input_modal_email.val(),
                        "password": input_modal_password.val()
                    });
                    input_users_json.val(JSON.stringify(all_users_json));
                    div_list_users.append(card_user_html);
                }
            }

            input_modal_username.val("");
            input_modal_email.val("");
            input_modal_password.val("");

            $('#add-user').modal('hide');
        }
    });

    function user_exists(username) {
        let users_json = JSON.parse(input_users_json.val());
        for (let i=0; i < users_json.length; i++) {
            if ( users_json[i].username === username )
                return true;
        }
        return false;
    }

});