//Layout Selector
class LayoutSelector extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        let layoutOptions = this.props.layouts.map((layout, index) => (
                                <a href="#" onClick={() => this.props.onLayoutChanged(layout)}>{layout['name']}</a>
                            ));
        return (
            <div>
                <div className="menu-toggle">
                    <span>Layout</span>
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

    }
}

const layoutSelectorDispatchMap = (dispatch) => {
    return {
        onLayoutChanged: (layout) => {
            console.log('Changing Layout: ', layout)
            dispatch(changeLayout(layout))
        }
    }
}

const LayoutSelectorContainer = ReactRedux.connect(
    layoutSelectorStateMap,
    layoutSelectorDispatchMap
)(LayoutSelector)
