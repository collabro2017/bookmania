class BookCover extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        return (
            <div className="cover-image-wrapper">
                <div className="overlay">
                    <button className="btn edit-btn" onClick={()=>this.props.onClick()}>
                        <span>Change</span>
                    </button>
                </div>
                <img className="cover-image" src={this.props.cover_image_url}/>
            </div>
        );
    }
}

const bookCoverStateMap = (state) => {
    return {
        id: state.bookEditorReducer.id,
        name: state.bookEditorReducer.name,
        status: state.bookEditorReducer.status,
        cover_image_url: state.bookEditorReducer.cover_image_url,
        cover_thumbnail_url: state.bookEditorReducer.cover_thumbnail_url,
    }
}

const bookCoverDispatchMap = (dispatch) => {
    return {
        onClick: () => {
            dispatch(selectCoverImage());
            dispatch(openImageModal());
        }
    }
}

const BookCoverContainer = ReactRedux.connect(
    bookCoverStateMap,
    bookCoverDispatchMap
)(BookCover)


class SideMenuBookCover extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        return (
            <div>
                <div className="cover-image-wrapper">

                    <div className="status-wrap">
                        <div className="status green-status">{this.props.status}</div>
                    </div>

                    <div className="overlay">
                        <button className="btn edit-btn" onClick={()=>this.props.onClick()}>
                            <span>Change</span>
                        </button>
                    </div>
                    <img className="cover-image" src={this.props.cover_image_url}/>
                </div>
                <div className="name">{this.props.name}</div>
            </div>
        );
    }
}

const SideMenuBookCoverContainer = ReactRedux.connect(
    bookCoverStateMap,
    bookCoverDispatchMap
)(SideMenuBookCover)