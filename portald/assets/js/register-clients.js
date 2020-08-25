$(function() {
    'use strict';

    const div_list_users = $('#list-users');
    const input_users_json = $('#users-json');

    let input_modal_username = $('#username-user');
    let input_modal_email = $('#email-user');
    let input_modal_password = $('#password-user');

    function create_alert(msg, theme, prefix) {
        return `<div class="alert alert-${theme} alert-dismissible fade show" role="alert">
                 <strong>${prefix}</strong> ${msg}
                 <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                 </button>
                </div>`
    }

    function create_user_card_html(username, email) {
        /* <button class="close close-card-user" type="button" id="${username}" style="color: white" data-dismiss="modal" aria-label="Close"> */
        /* <span aria-hidden="true">×</span></button></h5> */
        return `<div class="col-sm-6 mb-3"><div class="card"><div class="card-body" style="padding: 15px;"><h5 class="card-title">${username}
                <h6 class="card-subtitle mb-0 text-muted">${email}</h6></div></div></div>`
    }

    $('#submit-form').click(function (e) {
        if (input_users_json.val() === "") {
            $('#add-user').modal('show');
        } else {
            let token = $('input[name="csrfmiddlewaretoken"]').val();
            let company_name = $('#company-name').val();
            let display_name = $('#display-name').val();
            let cnpj = $('#cnpj').val();
            let city = $('#city').val();
            let state = $('#state').val();
            let cep = $('#cep').val();
            let state_registration = $('#state-registration').val();
            let municipal_registration = $('#municipal-registration').val();
            let email = $('#email').val();
            let users_json = $('#users-json').val();
            let files = $('#logo')[0].files[0];

            let fd = new FormData();
            fd.append('file', files);
            fd.append('csrfmiddlewaretoken',token);
            fd.append('company-name', company_name);
            fd.append('display-name',display_name);
            fd.append('cnpj', cnpj);
            fd.append('city', city);
            fd.append('state', state);
            fd.append('cep', cep);
            fd.append('state-registration', state_registration);
            fd.append('municipal-registration', municipal_registration);
            fd.append('email', email);
            fd.append('users-json', users_json);

            $.ajax({
                url: "/register-client",
                method: 'post',
                data: fd,
                cache: false,
                contentType: false,
                processData: false,
                success: function(data) {
                    if (data.code === 200)
                        $('#alerts').append(create_alert(data.msg, 'success', ''))
                    else
                        $('#alerts').append(create_alert(data.msg, 'danger', 'Algo está errado!'))
                },
                error: function (data) {
                    $('#alerts').append(create_alert(data.msg, 'danger', 'Ocorreu um erro interno!'))
                }
            });
        }
    });

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
            input_modal_username.val(""); input_modal_email.val(""); input_modal_password.val("");
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