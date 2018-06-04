// Action Types
const OPEN_IMAGE_MODAL = 'OPEN_IMAGE_MODAL';
const CLOSE_IMAGE_MODAL = 'CLOSE_IMAGE_MODAL';
const IMAGE_SELECTED = 'IMAGE_SELECTED';

// Action Creators
function openImageModal(){
    return {
        type: OPEN_IMAGE_MODAL
    };
}

function closeImageModal(){
    return {
        type: CLOSE_IMAGE_MODAL
    };
}

function imageSelected(imgUrl, thumbnailUrl){
    return {
        type: IMAGE_SELECTED,
        imgUrl: imgUrl,
        thumbnailUrl: thumbnailUrl
    };
}