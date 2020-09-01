$(function() {
    'use strict';

    $('#n-add').click(function (e) {
        let token = $('input[name="csrfmiddlewaretoken"]').val();

        let username = $('#n-username');
        let password = $('#n-passwd');
        let enterprise = $('#n-enterprise');

        if (username.val() === '')
            username.focus();
        else if (password.val() === '')
            password.focus();
        else if (enterprise.val() === '')
            enterprise.focus()
        else {
            let nfd = new FormData();

            nfd.append('username', username.val());
            nfd.append('passwd', password.val());
            nfd.append('enterprise', enterprise.val());
            nfd.append('csrfmiddlewaretoken', token);

            $.ajax({
                url: '/passwords-safe',
                method: 'post',
                data: nfd,
                cache: false,
                contentType: false,
                processData: false,
                beforeSend: function () {
                },
                success: function(data) {
                    if ( data.code === 200 ) {
                        Swal.mixin({
                            toast: true,
                            position: 'top-end',
                            showConfirmButton: false,
                            timer: 1113000
                        }).fire({
                                icon: 'success',
                                title: 'Usuário adicionado!'
                            });
                        $('#mnpass').modal('hide');

                        username.val("");
                        password.val("");
                    }
                },
                error: function (data) {
                    alert('internal error!')
                }
            });
        }

    });

    $('.show-passwd').click(function (e) {
        let username = e.currentTarget.id;
        let token = $('input[name="csrfmiddlewaretoken"]').val();

        let click = e.currentTarget.getAttribute('data-click');
        alert(click)
        let _id = '#passwd-'+username;
        let _icon_id = '#icon-v-'+username;

        if ( click === "1" ) {
            let fd = new FormData();
            fd.append('username', username.replace('-', '.'));
            fd.append('csrfmiddlewaretoken', token);

            $.ajax({
                url: '/passwords-safe',
                method: 'post',
                data: fd,
                cache: false,
                contentType: false,
                processData: false,
                beforeSend: function () {
                    $(_icon_id).html('<div class="spinner-border spinner-border-sm" role="status"><span class="sr-only">Loading...</span></div>')
                },
                success: function(data) {
                    if ( data.code === 200 ) {
                        $(_id).text(data.msg);
                        e.currentTarget.setAttribute('data-click', '2');
                        $(_icon_id).html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-eye-off"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>')
                    }
                },
                error: function (data) {
                    alert('internal error!')
                }
            });
        } else {
            $(_id).text('**********');
            e.currentTarget.setAttribute('data-click', '1');
            $(_icon_id).html('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-eye"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>')
        }
    });

});