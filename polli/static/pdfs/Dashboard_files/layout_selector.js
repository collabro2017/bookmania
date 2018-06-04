//Layout Selector
class LayoutSelector extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        let layoutOptions = this.props.layouts.map((layout, index) => (
                                <a href="#" onClick={() => this.props.onLayoutChanged(layout)}>{layout.replace('_', ' ')}</a>
                            ));
        return (
            <div>
                <div className="menu-toggle">
                    <span>Select Layout</span>
                    <i className="fa fa-angle-down"></i>
                </div>

                <div className="menu">
                    {layoutOptions}
                </div>
            </div>
        );
    }
}

// Connect Layout Selector to Store
const layoutSelectorStateMap = (state) => {
    return {
        layout: state.pageEditorReducer.layout
    }
}

const layoutSelectorDispatchMap = (dispatch) => {
    return {
        onLayoutChanged: (layout) => {
            dispatch(changeLayout(layout))
        }
    }
}

const LayoutSelectorContainer = ReactRedux.connect(
    layoutSelectorStateMap,
    layoutSelectorDispatchMap
)(LayoutSelector)
