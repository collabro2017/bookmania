const initialImageSelectorState = {showImageSelector: false}

function imageSelectorReducer(state=initialImageSelectorState, action){
    switch (action.type) {
        case OPEN_IMAGE_MODAL:
            var newState = Object.assign({}, state, {
                showImageSelector: true
            });
            return newState;

        case CLOSE_IMAGE_MODAL:
            return Object.assign({}, state, {
                showImageSelector: false
            })
        case IMAGE_SELECTED:
            return Object.assign({}, state, {
                showImageSelector: false
            })
        default:
          return state
    }
}