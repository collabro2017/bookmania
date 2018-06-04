// Action Types
const SAVE_BOOK = 'SAVE_BOOK';
const LOAD_BOOK_INFO = 'LOAD_BOOK_INFO'
const SELECT_COVER_IMAGE = 'SELECT_COVER_IMAGE';


function saveBook(id, name, description){
    return {
        type: SAVE_BOOK,
        id: id,
        name: name,
        description: description
    };
}

function loadBookInfo(bookInfo){
    return {
        type: LOAD_BOOK_INFO,
        bookInfo: bookInfo
    };
}

function selectCoverImage(){
    return {
        type: SELECT_COVER_IMAGE,
    };
}