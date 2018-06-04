const DEFAULT_IMAGE = 'https://polli-static.s3.amazonaws.com/images/samples/grey_square_image_placeholder.jpg';

const initialPageEditorReducer = {
        blend: 0,
        language: 'english',
        activeElement: null,
        activeElementIndex: null
    };

var stateStack = [];

function pageEditorReducer(state=initialPageEditorReducer, action){

    var savePage = (new_state, addToStack=true) => {
        console.log('[Save Page]');

        // Store Previous State in Stack
        if(addToStack){
            stateStack.push(state);
            console.log('[Push Previous State to Stack]');
        }

        var params = {
            content: {
                style: new_state.style,
                elements: new_state.elements,
            },
        };

        var updatePageUrl = '/publisher/page/'+new_state.pageID+'/';
        $.ajax({
            url: updatePageUrl,
            type: 'PATCH',
            data: JSON.stringify(params),
            processData: false,
            contentType: 'application/json',
            success: function(data, textStatus, jqXHR)
            {
                console.log(data);
            }
        }, 'json');

    }

    switch (action.type) {

        case LOAD_PAGE_CONTENT:
            var new_state = Object.assign({}, state, action.content, {pageID: action.pageID});
            return new_state;

        case UNDO_ACTION:
            console.log('[Action] - Undo Action');
            if(stateStack.length>0){
                var new_state = stateStack.pop()
                savePage(new_state, false);
                return new_state
            }else{
                return state;
            }

        case ADD_TEXT:
            console.log('[Action] - Add Text');
            var textElement = {
                'type': 'text',
                'data': {
                    'english': 'Default Text'
                },
                'containerStyle': {},
                'style': {
                    'display': 'flex',
                    'flex': 1,
                }
            };

            var elements = state.elements.slice(0);
            elements.push(textElement);

            var new_state = Object.assign({}, state, {
                elements: elements
            });
            savePage(new_state);
            return new_state;

        case ADD_IMAGE:
            console.log('[Action] - Add Image');
            var flexDir = state.style.flexDirection;
            var height = flexDir=='row' ? 'auto' : '100%';
            var width = flexDir=='row' ? '100%' : 'auto';

            var imageElement = {
                'type': 'image',
                'data': {
                    'url': DEFAULT_IMAGE,
                    'thumbnail_url': DEFAULT_IMAGE
                },
                'containerStyle': {
                    'flex': 1
                },
                'style': {
                    'height': height,
                    'width': width
                }
            }
            var elements = state.elements.slice(0);
            elements.push(imageElement);

            var new_state = Object.assign({}, state, {
                elements: elements
            });
            savePage(new_state);
            return new_state

        case REMOVE_ELEMENT:
            console.log('[Action] - Remove Element');
            var elements = state.elements.slice(0);
            elements.splice(action.elementIndex, 1);
            var new_state = Object.assign({}, state, {
                elements: elements
            });
            savePage(new_state);
            return new_state

        case EDIT_PAGE_ELEMENT:
            console.log('[Action] - Edit Page Element');
            var elements = state.elements.slice(0);
            var activeElement = elements[action.elementIndex];
            var new_state = Object.assign({}, state, {
                activeElement: activeElement,
                activeElementIndex: action.elementIndex
            })
            return new_state

        case EDIT_PAGE:
            console.log('[Action] - Edit Page');
            var new_state = Object.assign({}, state, {
                activeElement: null,
                activeElementIndex: null
            })
            return new_state

        case UPDATE_PAGE_PROPERTY:
            console.log('[Action] - Update Page Property');
            var style = Object.assign({}, state.style);
            var elements = state.elements.slice(0);

            if(action.propName=='flexDirection'){
                var height = value=='row' ? 'auto' : '100%';
                var width = value=='row' ? '100%' : 'auto';

                elements = elements.map(function(element){
                    if(element.type=='image'){
                        element.style['height'] = height;
                        element.style['width'] = width;

                        // Clear Alignment Styling
                        delete element.containerStyle['alignSelf'];
                        delete element.containerStyle['textAlign'];
                    }
                    return element;
                });
            }
            style[action.propName] = action.value;

            var new_state = Object.assign({}, state, {
                style: style,
                elements: elements
            })
            savePage(new_state);
            return new_state

        case UPDATE_ELEMENT_PROPERTY:
            console.log('[Action] - Update Element Property');
            var new_state = $.extend(true, {}, state);
            new_state.elements[new_state.activeElementIndex].style[action.propName] = action.value;
            savePage(new_state);
            return new_state

        case UPDATE_CONTAINER_PROPERTY:
            console.log('[Action] - Update Container Property');
            var new_state = $.extend(true, {}, state);
            new_state.elements[new_state.activeElementIndex].containerStyle[action.propName] = action.value;
            savePage(new_state);
            return new_state

        case UPDATE_TEXT:
            console.log('[Action] - Update Text');
            var elements = state.elements.slice(0);
            elements[state.activeElementIndex].data[state.language] = action.newText;
            var new_state = Object.assign({}, state, {
                elements: elements,
                activeElement: elements[state.activeElementIndex]
            })
            return new_state

        case CHANGE_EDITOR_LANGUAGE:
            var new_state = Object.assign({}, state, {
                language: action.language
            })
            return new_state

        case IMAGE_SELECTED:
            console.log('[Action] - Image Selected');
            if(state.activeElementIndex!=null){
                var new_state = $.extend(true, {}, state);
                new_state.elements[state.activeElementIndex].data = {
                    url: action.imgUrl,
                    thumbnail_url: action.thumbnailUrl
                };
                new_state.imageSelectionTarget = null;
                savePage(new_state);
                return new_state;
            }else{
                return state;
            }

        case SAVE_PAGE:
            savePage(state);
            return state

         case CHANGE_LAYOUT:
            var new_state = $.extend(true, {}, state);
            let currentElements = new_state.elements.slice(0);
            let updatedElements = action.layout.layout.elements;

            // Get Current Text and Image Data
            let textData = '';
            let imageData = null;
            for(var i=0; i<currentElements.length; i++){
                if(currentElements[i]['type']=='image' && imageData==null){
                    imageData = currentElements[i]['data'];
                }else if(currentElements[i]['type']=='text' && textData==null){
                    textData = currentElements[i]['data']['english'];
                }else if(currentElements[i]['type']=='text'){
                    textData += ' ' + currentElements[i]['data']['english'];
                }
            }

            // Assign Text and Image Data
            let textSet = false;
            let imageSet = false;
            for(var j=0; j<updatedElements.length; j++){
                if(textData!='' && textSet==false && updatedElements[j]['type']=='text'){
                    updatedElements[j]['data']['english'] = textData;
                    textSet = true;
                }else if(imageData && imageSet==false && updatedElements[j]['type']=='image'){
                    updatedElements[j]['data'] = imageData;
                    imageSet = true;
                }
            }

            new_state.style = action.layout.layout.style;
            new_state.elements = updatedElements;
            savePage(new_state);
            return new_state;

        case CHANGE_BLEND:
            var new_state = Object.assign({}, state, {
                blend: action.blend
            })
            return new_state

        default:
          return state
    }
}