$(document).ready(function(){

    // New Book Modal
    $('.upload-book-btn').click(function(){
        //$('input[name=book_pdf]').click();

        //Clear Form
        $("#new-book-modal input").val('');
        $("#new-book-modal .file-selector label").text('Select PDF');
        $('#new-book-modal').fadeIn();
    });

    $('#new-book-modal .close-btn').click(function(){
        $('#new-book-modal').fadeOut();
    });

    $('#new-book-modal .file-selector').click(function(){
        console.log('upload the book pdf');
        $("#new-book-modal .book-pdf-input").click();
    });

    $('#new-book-modal .book-pdf-input').on('change', function(event){
        console.log('you change the book pdf');
        var pdf_filename = $('#new-book-modal .book-pdf-input')[0].files[0].name;
        $("#new-book-modal .file-selector label").text(pdf_filename);
    });

    $('#new-book-modal .save-btn').click(function(){
        console.log('save the new book');

        // Close New Book Modal
        $('#new-book-modal').fadeOut(400, function(){
            // Show Progress Modal
            $('.progress-modal .progress-bar').css('width', '0%');
            $('.progress-modal').fadeIn();
        });

        // Upload Book
        var data = new FormData();
        data.append('book_pdf', $('#new-book-modal .book-pdf-input')[0].files[0], 'book.pdf');
        data.append('name', $("#new-book-modal .book-name").val());
        data.append('template', $("#new-book-modal .layout-select").val());

        data.append('author', $("#new-book-modal .author").val());
        data.append('description', $("#new-book-modal .description").val());
        data.append('translation', $("#new-book-modal .translation-select").val());

        $.ajax({
            url: '/publisher/book/',
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
            success: function(data, textStatus, jqXHR)
            {
                console.log(data);

                // Begin Polling for the Book's Processing Status
                var processingStatusUrl = '/publisher/book/'+data.id+'/get_book_processing_status/';
                var statusInterval = setInterval(function(){
                    $.post(processingStatusUrl, {}, function(resp){
                        console.log('Processing Completed: ', resp.processing_completed);
                        $('.progress-modal .progress-bar').css('width', resp.processing_completed + '%');
                    }, 'json');
                }, 1000);

                // Start Processing the Book
                var processBookUrl = '/publisher/book/'+data.id+'/process_book/';
                $.post(processBookUrl, {}, function(data){

                    //Hide Progress Modal
                    $('.progress-modal').fadeOut();

                    // Add New Book to View
                    var template = _.template($('#book-template').html());
                    var $book = $(template(data));
                    $('.book-grid').append($book);
                    $book.fadeIn();

                    // Clear Progress Polling Interval
                    clearInterval(statusInterval);

                }, 'json');

            }
        }, 'json');
    });

    // Book Deletion
    var deleteBookID = null;
    $('#delete-modal .delete-btn').click(function(){
        console.log('confirm delete');
        $('#delete-modal').fadeOut();
        var deleteBookUrl = '/publisher/book/'+deleteBookID+'/';
        $.ajax({
            url: deleteBookUrl,
            type: 'DELETE',
            success: function(data, textStatus, jqXHR)
            {
                console.log('Delete Complete');
                $(".book[data-id='"+deleteBookID+"']").remove();
            }
        }, 'json');
    });

    $('#delete-modal .cancel-btn').click(function(){
        console.log('cancel delete');
        $('#delete-modal').fadeOut();
    });

    $('body').on('click', '.book .delete-btn', function(){
        var $book = $(this).closest('.book');
        deleteBookID = $book.data('id');
        console.log('delete id: ', deleteBookID);
        $('#delete-modal').fadeIn();
    });
});