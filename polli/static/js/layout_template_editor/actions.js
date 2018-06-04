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
const LOAD_LAYOUT_TEMPLATE = 'LOAD_LAYOUT_TEMPLATE';
const UPDATE_TEXT = 'UPDATE_TEXT';
const SAVE_PAGE = 'SAVE_PAGE';

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

function savePage(){
    return {
        type: SAVE_PAGE
    };
}

function loadLayoutTemplate(templateID, layout){
    return {
        type: LOAD_LAYOUT_TEMPLATE,
        templateID: templateID,
        layout: layout
    };
}
