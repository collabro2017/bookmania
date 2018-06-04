class LayoutManager extends React.Component {

    render() {
        let SelectedLayout = this.props.layoutOptions[this.props.layout];

        return <SelectedLayout
                    onSelectImage={this.props.onSelectImage}
                    images={this.props.images}
                    onSelectText={this.props.onSelectText}
                    text={this.props.text}
                    textSelectionTarget={this.props.textSelectionTarget}
                    defaultImage={this.props.defaultImage}></SelectedLayout>;
    }
}

const layoutManagerStateMap = (state) => {
    return {
        layout: state.pageEditorReducer.layout,
        images: state.pageEditorReducer.images,
        text: state.pageEditorReducer.text,
        textSelectionTarget: state.pageEditorReducer.textSelectionTarget
    }
}

const layoutManagerDispatchMap = (dispatch) => {
    return {
        onSelectImage: (target_id) => {
            dispatch(openImageModal());
            dispatch(setImageTarget(target_id));
        },
        onSelectText: (target_id) => {
            dispatch(selectText(target_id));
        }
    }
}

const LayoutManagerContainer = ReactRedux.connect(
    layoutManagerStateMap,
    layoutManagerDispatchMap
)(LayoutManager)
