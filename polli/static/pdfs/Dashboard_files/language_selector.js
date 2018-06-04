class LanguageSelector extends React.Component {
    render() {
        return (
            <div>
                <div className="menu-toggle">
                    <label>{this.props.language}</label>
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
const languageSelectorStateMap = (state) => {
    return {
        language: state.pageEditorReducer.language
    }
}

const languageSelectorDispatchMap = (dispatch) => {
    return {
        onLanguageChanged: (language) => {
            console.log('language changed');
            dispatch(changeEditorLanguage(language));
        }
    }
}

const LanguageSelectorContainer = ReactRedux.connect(
    languageSelectorStateMap,
    languageSelectorDispatchMap
)(LanguageSelector)

