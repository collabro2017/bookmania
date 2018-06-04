class FeatureSelector extends React.Component {
    render() {
        return (
            <div>
                <div className="menu-toggle">
                    <label>Select Feature</label>
                    <i className="fa fa-angle-down"></i>
                </div>

                <div className="menu">
                    <div className="item" onClick={()=>this.props.onLanguageChanged('english')}>English</div>
                    <div className="item" onClick={()=>this.props.onLanguageChanged('spanish')}>Spanish</div>
                    <div className="item" onClick={()=>this.props.onLanguageChanged('russian')}>Russian</div>
                </div>
            </div>
        );
    }
}

// Connect Layout Selector to Store
const featureSelectorStateMap = (state) => {
    return {
        selectedFeature: state.pageEditorReducer.selectedFeature
    }
}

const featureSelectorDispatchMap = (dispatch) => {
    return {
        /*
        onCloseTagSelector: () => {
            dispatch(closeTagSelector());
        }*/
    }
}

const FeatureSelectorContainer = ReactRedux.connect(
    featureSelectorStateMap,
    featureSelectorDispatchMap
)(FeatureSelector)

