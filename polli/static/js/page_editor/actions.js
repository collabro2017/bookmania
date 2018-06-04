// Action Types
const UNDO_ACTION = 'UNDO_ACTION';
const ADD_TEXT = 'ADD_TEXT';
const ADD_IMAGE = 'ADD_IMAGE';
const REMOVE_ELEMENT = 'REMOVE_ELEMENT';
const EDIT_PAGE_ELEMENT = 'EDIT_PAGE_ELEMENT';
const EDIT_PAGE = 'EDIT_PAGE';
const UPDATE_PAGE_PROPERTY = 'UPDATE_PAGE_PROPERTY';
const UPDATE_ELEMENT_PROPERTY = 'UPDATE_ELEMENT_PROPERTY';
const UPDATE_CONTAINER_PROPERTY = 'UPDATE_CONTAINER_PROPERTY';
const UPDATE_TEXT = 'UPDATE_TEXT';
const CHANGE_LAYOUT = 'CHANGE_LAYOUT';

const CHANGE_BLEND = 'CHANGE_BLEND';
const SAVE_PAGE = 'SAVE_PAGE';
const LOAD_PAGE_CONTENT = 'LOAD_PAGE_CONTENT';
const CHANGE_EDITOR_LANGUAGE = 'CHANGE_EDITOR_LANGUAGE';

// Action Creators
function undoAction(){
    return {
        type: UNDO_ACTION
    };
}

function addText(){
    return {
        type: ADD_TEXT
    };
}

function addImage(){
    return {
        type: ADD_IMAGE
    };
}

function removeElement(elementIndex){
    return {
        type: REMOVE_ELEMENT,
        elementIndex: elementIndex
    };
}

function editPageElement(elementIndex){
    return {
        type: EDIT_PAGE_ELEMENT,
        elementIndex: elementIndex
    };
}

function editPage(){
    return {
        type: EDIT_PAGE
    };
}

function updatePageProperty(propName, value){
    return {
        type: UPDATE_PAGE_PROPERTY,
        propName: propName,
        value: value
    };
}

function updateElementProperty(propName, value){
    return {
        type: UPDATE_ELEMENT_PROPERTY,
        propName: propName,
        value: value
    };
}

function updateContainerProperty(propName, value){
    return {
        type: UPDATE_CONTAINER_PROPERTY,
        propName: propName,
        value: value
    };
}

function updateText(newText){
    return {
        type: UPDATE_TEXT,
        newText: newText
    };
}

//
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

function changeEditorLanguage(language){
    return {
        type: CHANGE_EDITOR_LANGUAGE,
        language: language,
    };
}