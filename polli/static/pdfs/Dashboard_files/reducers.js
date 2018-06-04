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
                    book_id: state.id,
                    image_url: action.imgUrl
                };
                $.post('/publisher/update-book-cover/', params, function(resp){
                    console.log(resp);
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
                book_id: action.id,
                name:  action.name,
                description: action.description
            };
            $.post('/publisher/update-book-general-info/', params, function(resp){
                console.log(resp);
                $('.save-complete-msg').animate({ opacity: 1 }, 700).delay(1000).animate({ opacity: 0}, 700);
             }, 'json');

            var new_state = Object.assign({}, state, {name: action.name, description: action.description})
            return new_state
        default:
          return state
    }
}