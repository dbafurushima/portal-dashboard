$(function() {
    'use strict';

    $('.show-info').click(function(e) {
        let id = e.currentTarget.id;
        let company_name = e.currentTarget.getAttribute('data-company_name');
        let display_name = e.currentTarget.getAttribute('data-display_name');
        let cnpj = e.currentTarget.getAttribute('data-cnpj');
        let city = e.currentTarget.getAttribute('data-city');
        let state = e.currentTarget.getAttribute('data-state');
        let cep = e.currentTarget.getAttribute('data-cep');
        let state_registration = e.currentTarget.getAttribute('data-state_registration');
        let municipal_registration = e.currentTarget.getAttribute('data-municipal_registration');
        let created_at = e.currentTarget.getAttribute('data-created_at');

        $('#company_name').text('Company Name: '+company_name);
        $('#display_name').text(display_name);
        $('#cnpj').text(cnpj);
        $('#city').text(city);
        $('#state').text(state);
        $('#cep').text(cep);
        $('#state_registration').text(state_registration);
        $('#municipal_registration').text(municipal_registration);
        $('#created_at').text(created_at);

        $('#info-modal').modal('show');
    });

});