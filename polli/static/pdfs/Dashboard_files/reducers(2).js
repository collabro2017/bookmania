const initialPageEditorReducer = {
        blend: 0,
        imageSelectionTarget: null,
        textSelectionTarget: 1,
        focusEditor: false,
        language: 'english',
        selectedFeature: null
    };

function pageEditorReducer(state=initialPageEditorReducer, action){

    var savePageToServer = (new_state) => {
        console.log('save page');
        var params = {
            page_id: new_state.pageID,
            content: {
                layout: new_state.layout,
                images: new_state.images,
                text: new_state.text,
            }
        };
        $.post('/publisher/update-page/', JSON.stringify(params), function(resp){
            console.log(resp);
        }, 'json');
    }

    switch (action.type) {
        case LOAD_PAGE_CONTENT:
            var new_state = Object.assign({}, state, action.content, {pageID: action.pageID})
            return new_state
        case SET_IMAGE_TARGET:
            return Object.assign({}, state, {
                imageSelectionTarget: action.targetID
            })
        case CHANGE_LAYOUT:
            var new_state = Object.assign({}, state, {
                layout: action.layout
            });
            savePageToServer(new_state);
            return new_state;
        case CHANGE_BLEND:
            return Object.assign({}, state, {
                blend: action.blend
            })
        case IMAGE_SELECTED:
            var imgTarget = state.imageSelectionTarget;
            if(imgTarget){
                var images = Object.assign({}, state.images, {});
                images[imgTarget] = {
                    url: action.imgUrl,
                    thumbnail_url: action.thumbnailUrl
                };
                new_state = Object.assign({}, state, {
                    images: images,
                    imageSelectionTarget: null
                });

                savePageToServer(new_state);
                return new_state;
            }else{
                return state;
            }
        case SELECT_TEXT:
            console.log('select text');
            return Object.assign({}, state, {
                textSelectionTarget: action.target_id,
                focusEditor: true
            })
        case UPDATE_TEXT:
            console.log('update text');

            var textTarget = state.textSelectionTarget;
            var text = Object.assign({}, state.text, {});

            if(typeof(text[textTarget]) != 'object'){
                text[textTarget] = {};
            }

            text[textTarget][state.language] = {
                                                    plain: action.plain,
                                                    tagged: action.tagged
                                                };

            return Object.assign({}, state, {
                text: text
            })
        case EDITOR_FOCUS_COMPLETE:
            return Object.assign({}, state, {
                focusEditor: false
            })
        case SAVE_PAGE:
            savePageToServer(state);
            return state
        case CHANGE_EDITOR_LANGUAGE:
            return Object.assign({}, state, {
                language: action.language
            })
        default:
          return state
    }
}