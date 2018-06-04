function bookEditorReducer(state={changingCover: false}, action){
    switch (action.type) {
        case LOAD_BOOK_INFO:
            var new_state = Object.assign({}, state, action.bookInfo)
            return new_state

        case SELECT_COVER_IMAGE:
            var new_state = Object.assign({}, state, {changingCover: true})
            return new_state

        case CLOSE_IMAGE_MODAL:
            var new_state = Object.assign({}, state, {changingCover: false})
            return new_state

        case IMAGE_SELECTED:
            if(state.changingCover){
                var params = {
                    image_url: action.imgUrl
                };
                var updateCoverUrl = '/publisher/book/'+state.id+'/update_book_cover/';
                $.post(updateCoverUrl, params, function(resp){
                    console.log('Cover Updated');
                }, 'json');

                var new_state = Object.assign({}, state, {
                    showImageSelector: false,
                    cover_image_url: action.imgUrl,
                    cover_thumbnail_url: action.thumbnailUrl,
                    changingCover: false
                });

                return new_state
            }else{
                return state;
            }
        case SAVE_BOOK:
            console.log('save book');
            var params = {
                name:  action.name,
                description: action.description,
                author: action.author
            };
            var new_state = Object.assign({}, state, {name: action.name, description: action.description, author: action.author})

            var updateBookUrl = '/publisher/book/'+state.id+'/';
            $.ajax({
                url: updateBookUrl,
                type: 'PUT',
                data: JSON.stringify(params),
                processData: false,
                contentType: 'application/json',
                success: function(data, textStatus, jqXHR)
                {
                    console.log('Book Updated');
                    $('.save-complete-msg').animate({ opacity: 1 }, 700).delay(1000).animate({ opacity: 0}, 700);
                }
            }, 'json');

            return new_state
        default:
          return state
    }
}