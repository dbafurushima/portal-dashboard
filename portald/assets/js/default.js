$('#set-dark').click(function (e) {
     post_set_theme('dark');
});

$('#set-light').click(function (e) {
     post_set_theme('light');
});


function post_set_theme(theme) {
    let fd = new FormData();
    fd.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
    fd.append('theme', theme);

    $.ajax({
        url: '/set-theme',
        method: 'post',
        data: fd,
        cache: false,
        contentType: false,
        processData: false,
        beforeSend: function () {
        },
        success: function(data) {
            if ( data.code === 200 ) {
                location.reload();
            }
        },
        error: function (data) {
            alert('internal error!')
        }
    });
}
