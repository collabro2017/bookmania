class LanguageSelector extends React.Component {
    render() {
        let languageOptions = this.props.languages.map(function(language){
            return <div className="item" onClick={()=>this.props.onLanguageChanged(language)}>{language}</div>;
        });

        return (
            <div>
                <div className="menu-toggle">
                    <label>{this.props.language}</label>
                    <i className="fa fa-angle-down"></i>
                </div>
                <div className="menu">
                    {languageOptions}
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

