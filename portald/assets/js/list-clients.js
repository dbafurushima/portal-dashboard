$(function() {
    'use strict';

    $('.disable-client').click(function(e) {
        let id = e.currentTarget.id;
        let swalDisableClient = Swal.mixin({
            customClass: {
                confirmButton: 'btn btn-success',
                cancelButton: 'btn btn-danger'
            },
            buttonsStyling: false,
        })
        Swal.fire({
            title: '<strong>Desabilitar <u>colaborador</u></strong>',
            icon: 'info',
            html:
                'Caso seja <b>desabilitado</b>, o colaborador não será ' +
                'mais exibido em toda e qualquer página da aplicação.',
            confirmButtonClass: 'ml-2',
            confirmButtonText: 'Sim, Desabilitar',
            cancelButtonText: 'Não, Cancelar!',
            showCloseButton: true,
            showCancelButton: true,
            focusConfirm: false,
        }).then((result) => {
            if (result.value) {
                let fd = new FormData();
                fd.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
                fd.append('client', id);

                $.ajax({
                    url: '/clientes',
                    method: 'post',
                    data: fd,
                    cache: false,
                    contentType: false,
                    processData: false,
                    beforeSend: function () {
                    },
                    success: function(data) {
                        if ( data.code === 200 ) {
                            swalDisableClient.fire(
                                'Desabilitado!',
                                'Colaborador desabilitado com sucesso.',
                                'success')
                        } else {
                            swalDisableClient.fire(
                                'Ops...',
                                data.msg,
                                'info')
                        }
                    },
                    error: function (data) {
                        console.log(data);
                        alert('internal error!');
                    }
                });
            } else if (
                // Read more about handling dismissals
                result.dismiss === Swal.DismissReason.cancel
            ) {
                console.log('cancelado...');
            }
        });
    });

    $('.card-client').click(function(e) {
        console.log($(this).parent());
        let id = e.currentTarget.id;
        let company_name = $(this).parent().attr('data-company_name');
        let display_name = $(this).parent().attr('data-display_name');
        let cnpj = $(this).parent().attr('data-cnpj');
        let cnpj_s = $(this).parent().attr('data-cnpj_s');
        let city = $(this).parent().attr('data-city');
        let state = $(this).parent().attr('data-state');
        let cep = $(this).parent().attr('data-cep');
        let address = $(this).parent().attr('data-address');
        let district = $(this).parent().attr('data-district');
        let state_registration = $(this).parent().attr('data-state_registration');
        let municipal_registration = $(this).parent().attr('data-municipal_registration');
        let created_at = $(this).parent().attr('data-created_at');
        let description = $(this).parent().attr('data-description');

        $('#company_name').text(company_name);
        $('#display_name').text(display_name);
        $('#cnpj').text(cnpj);
        $('#cnpj_s').text(cnpj_s);
        $('#city').text(city);
        $('#state').text(state);
        $('#cep').text(cep);
        $('#address').text(address);
        $('#district').text(district);
        $('#state_registration').text(state_registration);
        $('#municipal_registration').text(municipal_registration);
        $('#created_at').text(created_at);
        $('#description').text(description);

        $('#info-modal').modal('show');
    });

    function editModeEnable() {
        $('#text-edit-mode').html('Desabilitar Modo Edição');
    }
    function editModeDisable() {
        $('#text-edit-mode').html('Habilitar Modo Edição');
    }

    $('#edit-mode').click(function(e) {
        let id = e.currentTarget.id;
        $('.div-editing-mode').each(function(index, element) {
            let classList = element.className.split(/\s+/);

            for (let i = 0; i < classList.length; i++){
                if ( classList[i] === 'd-none' ) {
                    element.classList.remove('d-none');
                    editModeEnable();
                } else {
                    element.classList.add('d-none');
                    editModeDisable();
                }
            }

        });
    });

});