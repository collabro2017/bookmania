//Blend Selector
class BlendSelector extends React.Component {
    render() {
        return (
            <div>
                <div className="menu-toggle">
                    <span>Select Blend</span>
                    <i className="fa fa-angle-down"></i>
                </div>

                <div className="menu">
                    <a href="#" onClick={() => this.props.onBlendChanged(0)}>0%</a>
                    <a href="#" onClick={() => this.props.onBlendChanged(50)}>50%</a>
                    <a href="#" onClick={() => this.props.onBlendChanged(75)}>75%</a>
                    <a href="#" onClick={() => this.props.onBlendChanged(100)}>100%</a>
                </div>
            </div>
        );
    }
}

// Connect Layout Selector to Store
const blendSelectorStateMap = (state) => {
    return {
        blend: state.pageEditorReducer.blend
    }
}

const blendSelectorDispatchMap = (dispatch) => {
    return {
        onBlendChanged: (blend) => {
            dispatch(changeBlend(blend));
        }
    }
}

const BlendSelectorContainer = ReactRedux.connect(
    blendSelectorStateMap,
    blendSelectorDispatchMap
)(BlendSelector)

