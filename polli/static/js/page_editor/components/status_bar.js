class StatusBar extends React.Component {
    render() {
        return (
            <div>
                <i className="fa fa-cog"></i>
                <label>Status:</label>
                <span className="blue">Good%</span>
            </div>
        );
    }
}

const statusBarStateMap = (state) => {
    return {
        language: state.pageEditorReducer.language
    }
}

const statusBarDispatchMap = (dispatch) => {
    return {}
}

const StatusBarContainer = ReactRedux.connect(
    statusBarStateMap,
    statusBarDispatchMap
)(StatusBar)

