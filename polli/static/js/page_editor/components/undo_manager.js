class UndoManager extends React.Component {
    render() {
        return (
            <div onClick={this.props.onUndoAction}>
                <i className="fa fa-undo"></i>
                <span>Undo Action</span>
            </div>
        );
    }
}

const undoStateMap = (state) => {
    return {

    }
}

const undoDispatchMap = (dispatch) => {
    return {
        onUndoAction: () => {
            dispatch(undoAction())
        }
    }
}

const UndoManagerContainer = ReactRedux.connect(
    undoStateMap,
    undoDispatchMap
)(UndoManager)
