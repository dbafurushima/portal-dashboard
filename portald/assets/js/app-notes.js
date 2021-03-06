$(document).ready(function() {

    function deleteNote() {
        $(".delete-note").off('click').on('click', function(event) {
            event.stopPropagation();

            var item = $(this).parents('.note-item'); // .remove();

            let token = $('input[name="csrfmiddlewaretoken"]').val();
            let titleNote = $(this).parents('.note-item')[0].attributes["data-title"].nodeValue;

            $.post("/delete-note", {title: titleNote, csrfmiddlewaretoken: token}, function(data)  {
                console.log(data);
                if ( data.code === 500 )
                    Swal.fire({icon: 'error', title: 'Oops...', text: data.msg})
                else
                    item.remove();
            })
            .done(function() {})
            .fail(function() {})
            .always(function() {});
        })
    }

    function editNote() {
        $(".edit-note").off('click').on('click', function(event) {
            event.stopPropagation();
            $('#editNoteModal').modal('show');
            $('#edit-btn-n-save').show();
            $('#edit-btn-n-add').hide();

            let idNote = $(this).parents('.note-item')[0].attributes["data-id"].nodeValue;
            let titleNote = $(this).parents('.note-item')[0].attributes["data-title"].nodeValue;
            let textNote = $(this).parents('.note-item')[0].attributes["data-text"].nodeValue;
            let topicNote = $(this).parents('.note-item')[0].attributes["data-topic"].nodeValue;

            $('#edit-id-note').val(idNote);
            $('#edit-n-title').val(titleNote);
            $('#edit-n-description').val(textNote);
            $('#edit-n-topic').val(topicNote);
        })
    }

    $('#cancel-edit-note').on('click', function(event) {
        $('#editNoteModal').modal('hide');
    });

    $('#edit-btn-n-save').on('click', function(event) {

        let token = $('input[name="csrfmiddlewaretoken"]').val();

        let idNote = document.getElementById('edit-id-note').value;
        let titleNote = document.getElementById('edit-n-title').value;
        let topicNote = document.getElementById('edit-n-topic').value;
        let textNote = document.getElementById('edit-n-description').value;

        let divNoteId = '#note-'+idNote;
        let titleNoteId = '#title-note-'+idNote;
        let textNoteId = '#text-note-'+idNote;

        console.log('id: ', idNote);
        console.log('titleNote: ', titleNote);
        console.log('topicNote: ', topicNote);
        console.log('textNote: ', textNote);

        $.post("/edit-note", {
                id: idNote, title: titleNote, topic: topicNote, text: textNote, csrfmiddlewaretoken: token
        }, function(data)  {
            console.log(data);
            if ( data.code === 500 ) {
                $('#editNoteModal').modal('hide');
                $('#edit-btn-n-save').hide();
                $('#edit-btn-n-add').show();
                Swal.fire({icon: 'error', title: 'Oops...', text: data.msg});
            }
            else {
                let pTitle = $(titleNoteId)[0];
                let pText = $(textNoteId)[0];
                let divNote = $(divNoteId)[0];

                let classDiv = divNote.classList;
                classDiv.remove(classDiv[2]);
                classDiv.add('note-'+topicNote);

                divNote.attributes['data-title'].nodeValue = titleNote;
                divNote.attributes['data-text'].nodeValue = textNote;
                divNote.attributes['data-topic'].nodeValue = topicNote;

                console.log(divNote);
                console.log(pTitle);

                pTitle.textContent = titleNote;
                pTitle.attributes['data-notetitle'].nodeValue = titleNote;

                pText.textContent = textNote;
                pText.attributes['data-noteDescription'].nodeValue = textNote;

                $('#editNoteModal').modal('hide');
            }
        })
        .done(function() {})
        .fail(function() {})
        .always(function() {});
    });

    function favNote() {
        $(".fav-note").off('click').on('click', function(event) {
        event.stopPropagation();

            let token = $('input[name="csrfmiddlewaretoken"]').val();
            let titleNote = $(this).parents('.note-item')[0].attributes["data-title"].nodeValue;
            let isFav = $(this).parents('.note-item')[0].classList.contains("note-fav");
            $(this).parents('.note-item').toggleClass('note-fav');

            console.log('anc');
            console.log($(this).parents('.note-item')[0]);

            $.post("/fav-note", {name: titleNote, act: !isFav, csrfmiddlewaretoken: token}, function(data)  {
                console.log(data);

                if ( data.code === 500 ) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: data.msg
                    })
                } else {
                }
            })
            .done(function() {})
            .fail(function() {})
            .always(function() {});
        })
    }

    function addLabelGroups() {
        $('.tags-selector .label-group-item').off('click').on('click', function(event) {
          event.preventDefault();
          /* Act on the event */
          var getclass = this.className;
          console.log(getclass);
          var getSplitclass = getclass.split(' ')[0];
          console.log(getSplitclass);
          if ($(this).hasClass('label-personal')) {
            $(this).parents('.note-item').removeClass('note-social');
            $(this).parents('.note-item').removeClass('note-work');
            $(this).parents('.note-item').removeClass('note-important');
            $(this).parents('.note-item').toggleClass(getSplitclass);
          } else if ($(this).hasClass('label-work')) {
            $(this).parents('.note-item').removeClass('note-personal');
            $(this).parents('.note-item').removeClass('note-social');
            $(this).parents('.note-item').removeClass('note-important');
            $(this).parents('.note-item').toggleClass(getSplitclass);
          } else if ($(this).hasClass('label-social')) {
            $(this).parents('.note-item').removeClass('note-personal');
            $(this).parents('.note-item').removeClass('note-work');
            $(this).parents('.note-item').removeClass('note-important');
            $(this).parents('.note-item').toggleClass(getSplitclass);
          } else if ($(this).hasClass('label-important')) {
            $(this).parents('.note-item').removeClass('note-personal');
            $(this).parents('.note-item').removeClass('note-social');
            $(this).parents('.note-item').removeClass('note-work');
            $(this).parents('.note-item').toggleClass(getSplitclass);
          }
        });
    }

    $('.hamburger').on('click', function(event) {
        $('.app-note-container').find('.tab-title').toggleClass('note-menu-show')
        $('.app-note-container').find('.app-note-overlay').toggleClass('app-note-overlay-show')
    })
    $('.app-note-overlay').on('click', function(e){
        $(this).parents('.app-note-container').children('.tab-title').removeClass('note-menu-show')
        $(this).removeClass('app-note-overlay-show')
    })
    $('.tab-title .nav-pills a.nav-link').on('click', function(event) {
        $(this).parents('.app-note-container').find('.tab-title').removeClass('note-menu-show')
        $(this).parents('.app-note-container').find('.app-note-overlay').removeClass('app-note-overlay-show')
    })

    var $btns = $('.list-actions').click(function() {
        if (this.id == 'all-notes') {
          var $el = $('.' + this.id).fadeIn();
          $('#ct > div').not($el).hide();
        } if (this.id == 'important') {
          var $el = $('.' + this.id).fadeIn();
          $('#ct > div').not($el).hide();
        } else {
          var $el = $('.' + this.id).fadeIn();
          $('#ct > div').not($el).hide();
        }
        $btns.removeClass('active');
        $(this).addClass('active');
    });

    $('#btn-topic-cancel').on('click', function(event) {
        $('#topicModal').modal('hide');
    });

    $('#btn-add-notes').on('click', function(event) {
        $('#notesMailModal').modal('show');
        $('#btn-n-save').hide();
        $('#btn-n-add').show();
    })

    $('#btn-add-topic').on('click', function(event) {
        $('#topicModal').modal('show');
        $('#btn-n-save').hide();
        $('#btn-n-add').show();
    })

    $('#btn-topic-save').on('click', function (event) {
        event.preventDefault();

        let titleTopic = document.getElementById('topic-title').value;
        let topicColor = document.getElementById('color-picker').value;

        let htmlTopic = '<li class="nav-item">' +
            '<a class="nav-link list-actions g-dot-primary" id="note-'+titleTopic+'" style="color: '+topicColor+'">' +
            titleTopic+'</a></li>';

        let token = $('input[name="csrfmiddlewaretoken"]').val();

        let jqxhr = $.post("/create-topic", {name: titleTopic, color: topicColor, csrfmiddlewaretoken: token}, function(data)  {
            console.log(data);
            if ( data.code === 500 ) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: data.msg,
                    footer: '<a href>Why do I have this issue?</a>'
                })

            } else {
                $('#pills-tab').append(htmlTopic);
                $('#topicModal').modal('hide');
                let Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 1113000
                });

                Toast.fire({
                    icon: 'success',
                    title: 'Tópico criado com sucesso!'
                })
            }
        })
        .done(function() {})
        .fail(function() {})
        .always(function() {});

        // Perform other work here ...

        // Set another completion function for the request above
        jqxhr.always(function() {});
    });

    $('#topicModal').on('hidden.bs.modal', function (event) {
        event.preventDefault();
        document.getElementById('topic-title').value = '';
    })

    // Button add
    $("#btn-n-add").on('click', function(event) {
        event.preventDefault();
        /* Act on the event */
        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();
        var today = mm + '/' + dd + '/' + yyyy;

        var $_noteTitle = document.getElementById('n-title').value;
        var $_noteTopic = document.getElementById('n-topic').value;
        var $_noteDescription = document.getElementById('n-description').value;

        let token = $('input[name="csrfmiddlewaretoken"]').val();

        $html = '<div class="note-item all-notes note-'+$_noteTopic+'">' +
                    '<div class="note-inner-content">' +
                        '<div class="note-content">' +
                            '<p class="note-title" data-noteTitle="'+$_noteTitle+'">'+$_noteTitle+'</p>' +
                            '<p class="meta-time">'+today+'</p>' +
                            '<div class="note-description-content">' +
                                '<p class="note-description" data-noteDescription="'+$_noteDescription+'">'+$_noteDescription+'</p>' +
                            '</div>' +
                        '</div>' +
                        '<div class="note-action">' +
                            '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-star fav-note"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg> ' +
                            '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2 delete-note"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>' +
                            '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit edit-note"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>' +
                        '</div>' +
                        '<div class="note-footer">' +
                            '<div class="tags-selector btn-group">' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div> ';

        let jqxhr = $.post("/create-note", {
                title: $_noteTitle, text: $_noteDescription, csrfmiddlewaretoken: token, topic: $_noteTopic
            }, function(data)  {
            console.log(data);
            if ( data.code === 500 ) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: data.msg,
                    footer: '<a href="https://github.com/dbafurushima/portal-dashboard/issues">Why do I have this issue?</a>'
                })

            } else {
                $('#topicModal').modal('hide');
                let Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 1113000
                });

                Toast.fire({
                    icon: 'success',
                    title: 'Tópico criado com sucesso!'
                });

                $("#ct").prepend($html);
                $('#notesMailModal').modal('hide');
            }
        })
        .done(function() {})
        .fail(function() {})
        .always(function() {});

        deleteNote();
        favNote();
        // addLabelGroups();
    });

    $('#notesMailModal').on('hidden.bs.modal', function (event) {
        event.preventDefault();
        document.getElementById('n-title').value = '';
        document.getElementById('n-description').value = '';
    });

    deleteNote();
    favNote();
    editNote();
    // addLabelGroups();
})

// Validation Process

var $_getValidationField = document.getElementsByClassName('validation-text');

getNoteTitleInput = document.getElementById('n-title');

getNoteTitleInput.addEventListener('input', function() {

    getNoteTitleInputValue = this.value;

    if (getNoteTitleInputValue == "") {
      $_getValidationField[0].innerHTML = 'Title Required';
      $_getValidationField[0].style.display = 'block';
    } else {
      $_getValidationField[0].style.display = 'none';
    }
})

getNoteDescriptionInput = document.getElementById('n-description');

getNoteDescriptionInput.addEventListener('input', function() {

  getNoteDescriptionInputValue = this.value;

  if (getNoteDescriptionInputValue == "") {
    $_getValidationField[1].innerHTML = 'Description Required';
    $_getValidationField[1].style.display = 'block';
  } else {
    $_getValidationField[1].style.display = 'none';
  }

})