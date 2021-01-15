$(function() {
    'use strict';

    $('.show-info').click(function(e) {
        let id = e.currentTarget.id;
        let company_name = e.currentTarget.getAttribute('data-company_name');
        let display_name = e.currentTarget.getAttribute('data-display_name');
        let cnpj = e.currentTarget.getAttribute('data-cnpj');
        let cnpj_s = e.currentTarget.getAttribute('data-cnpj_s');
        let city = e.currentTarget.getAttribute('data-city');
        let state = e.currentTarget.getAttribute('data-state');
        let cep = e.currentTarget.getAttribute('data-cep');
        let address = e.currentTarget.getAttribute('data-address');
        let district = e.currentTarget.getAttribute('data-district');
        let state_registration = e.currentTarget.getAttribute('data-state_registration');
        let municipal_registration = e.currentTarget.getAttribute('data-municipal_registration');
        let created_at = e.currentTarget.getAttribute('data-created_at');
        let description = e.currentTarget.getAttribute('data-description');

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

});