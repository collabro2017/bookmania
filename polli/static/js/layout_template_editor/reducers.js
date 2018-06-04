const DEFAULT_IMAGE = 'https://polli-static.s3.amazonaws.com/images/samples/grey_square_image_placeholder.jpg';

const initialLayoutEditorReducer = {
        language: 'english',
        activeElement: null,
        activeElementIndex: null
    };

var stateStack = [];

function LayoutTemplateEditorReducer(state=initialLayoutEditorReducer, action){

    var savePage = (new_state, addToStack=true) => {
        console.log('[Save Page]');

        // Store Previous State in Stack
        if(addToStack){
            stateStack.push(state);
            console.log('[Push Previous State to Stack]');
        }

        var params = {
            layout: {
                style: new_state.style,
                elements: new_state.elements,
            },
        };

        jQuery.ajax ({
            url: '/publisher/layout-template/'+new_state.templateID+'/',
            type: "PUT",
            data: JSON.stringify(params),
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(resp){
                console.log(resp);
            }
        });

    }

    switch (action.type) {

        case LOAD_LAYOUT_TEMPLATE:
            var new_state = Object.assign({}, state, action.layout, {templateID: action.templateID});
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
                var height = action.value=='row' ? 'auto' : '100%';
                var width = action.value=='row' ? '100%' : 'auto';

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

        case SAVE_PAGE:
            savePage(state);
            return state

        default:
          return state
    }
}