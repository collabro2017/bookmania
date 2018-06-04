// Action Types
const CHANGE_LAYOUT = 'CHANGE_LAYOUT';
const CHANGE_BLEND = 'CHANGE_BLEND';
const SELECT_TEXT = 'SELECT_TEXT';
const UPDATE_TEXT = 'UPDATE_TEXT';
const EDITOR_FOCUS_COMPLETE = 'EDITOR_FOCUS_COMPLETE';
const SAVE_PAGE = 'SAVE_PAGE';
const LOAD_PAGE_CONTENT = 'LOAD_PAGE_CONTENT';
const SET_IMAGE_TARGET = 'SET_IMAGE_TARGET';
const CHANGE_EDITOR_LANGUAGE = 'CHANGE_EDITOR_LANGUAGE';


// Action Creators
function changeLayout(layout){
    return {
        type: CHANGE_LAYOUT,
        layout: layout
    };
}

function changeBlend(blend){
    return {
        type: CHANGE_BLEND,
        blend: blend
    };
}

function selectText(target_id){
    return {
        type: SELECT_TEXT,
        target_id: target_id
    };
}

function updateText(plain, tagged){
    return {
        type: UPDATE_TEXT,
        plain: plain,
        tagged: tagged
    };
}

function editorFocusComplete(){
    return {
        type: EDITOR_FOCUS_COMPLETE
    };
}

function savePage(){
    return {
        type: SAVE_PAGE
    };
}

function loadPageContent(pageID, content){
    return {
        type: LOAD_PAGE_CONTENT,
        pageID: pageID,
        content: content
    };
}

function setImageTarget(targetID){
    return {
        type: SET_IMAGE_TARGET,
        targetID: targetID,
    };
}

function changeEditorLanguage(language){
    return {
        type: CHANGE_EDITOR_LANGUAGE,
        language: language,
    };
}