class PageElement extends React.Component {
    constructor(props){
        super(props);
        this.editElement = this.editElement.bind(this);
        this.removeElement = this.removeElement.bind(this);
    }

    editElement(e){
        e.stopPropagation();
        this.props.onEditPageElement(this.props.index);
    }

    removeElement(e){
        e.stopPropagation();
        this.props.onRemove(this.props.index);
    }
}


class TextElement extends PageElement {
    render(){
        return (
            <div className="text-element page-element" onClick={(e)=>this.editElement(e)} style={this.props.element.style}>
                <div className="remove-btn" onClick={(e)=>this.removeElement(e)}>x</div>
                <div>{this.props.element.data[this.props.language]}</div>
            </div>
        );
    }
}


class ImageElement extends PageElement {
    render(){
        return (
            <div className="image-element page-element" onClick={(e)=>this.editElement(e)} style={this.props.element.containerStyle}>
                <div className="remove-btn" onClick={(e)=>this.removeElement(e)}>x</div>
                <div className="wrap">
                    <img src={this.props.element.data['url']} style={this.props.element.style}/>
                </div>
            </div>
        );
    }
}

class PageSettings extends React.Component {
    render(){
        return (
            <div className="form-section">
                <div className="form-field">
                    <label>Page Layout</label>
                    <select className="flex-direction" value={this.props.style.flexDirection} onChange={(e)=>this.props.onUpdatePageProperty('flexDirection', e.target.value)}>
                        <option>row</option>
                        <option>column</option>
                    </select>
                </div>
                <div className="form-field">
                    <label>Background Color</label>
                    <input type="color" value={this.props.style.backgroundColor} onChange={(e)=>this.props.onUpdatePageProperty('backgroundColor', e.target.value)}/>
                </div>
                <div className="form-field">
                    <label>Padding</label>
                    <input type="text" value={this.props.style.padding} onChange={(e)=>this.props.onUpdatePageProperty('padding', e.target.value)}/>
                </div>
            </div>
        );
    }
}

class TextSettings extends React.Component {
    constructor(props){
        super(props);
        this.updateText = this.updateText.bind(this);
        this.getLanguageText = this.getLanguageText.bind(this);
    }

    updateText(e){
        let text = e.target.value;
        this.props.onUpdateText(text);
    }

    getLanguageText(){
        let text = '';
        if(this.props.language in this.props.element.data){
            text = this.props.element.data[this.props.language];
        }
        console.log(text);
        return text
    }

    render(){
        let languages = this.props.languages.map(function(language){
            return <option>{language}</option>
        });
        return (
            <div className="form-section">

                <div className="form-field">
                    <label>Flex</label>
                    <input type='text' value={this.props.element.style.flex} onChange={(e)=>this.props.onUpdateElementProperty('flex', e.target.value)}/>
                </div>

                <div className="form-field">
                    <label>Font Size</label>
                    <input type='text' value={this.props.element.style.fontSize} onChange={(e)=>this.props.onUpdateElementProperty('fontSize', e.target.value)}/>
                </div>

                <div className="form-field">
                    <label>Color</label>
                    <input type='color' value={this.props.element.style.color} onChange={(e)=>this.props.onUpdateElementProperty('color', e.target.value)}/>
                </div>

                <div className="form-field">
                    <label>Font Family</label>
                    <select value={this.props.element.style.fontFamily} onChange={(e)=>this.props.onUpdateElementProperty('fontFamily', e.target.value)}>
                        <option>Roboto</option>
                        <option>Baloo</option>
                        <option>Eagle Lake</option>
                        <option>Open Sans</option>
                        <option>Lato</option>
                    </select>
                </div>

                <div className="form-field">
                    <label>Justify Content</label>
                    <select value={this.props.element.style.justifyContent} onChange={(e)=>this.props.onUpdateElementProperty('justifyContent', e.target.value)}>
                        <option>flex-start</option>
                        <option>center</option>
                        <option>flex-end</option>
                    </select>
                </div>

                <div className="form-field">
                    <label>Alignment</label>
                    <select value={this.props.element.style.alignItems} onChange={(e)=>this.props.onUpdateElementProperty('alignItems', e.target.value)}>
                        <option>flex-start</option>
                        <option>center</option>
                        <option>flex-end</option>
                    </select>
                </div>

                <div className="form-field language-select">
                    <label>Text</label>
                    <div className="select-wrap">
                        <select value={this.props.language} onChange={(e)=>this.props.onChangeLanguage(e.target.value)}>
                            {languages}
                        </select>
                    </div>
                    <textarea onChange={this.updateText} onBlur={this.props.onSavePage} value={this.getLanguageText()}></textarea>
                </div>

            </div>
        );
    }
}


class ImageSettings extends React.Component {
    render(){
        let alignment = null;
        if(this.props.pageStyle.flexDirection=='column'){
            alignment =  <select value={this.props.element.containerStyle.textAlign} onChange={(e)=>this.props.onUpdateContainerProperty('textAlign', e.target.value)}>
                                <option>left</option>
                                <option>center</option>
                                <option>right</option>
                             </select>;
        }else{
            alignment =  <select value={this.props.element.containerStyle.alignSelf} onChange={(e)=>this.props.onUpdateContainerProperty('alignSelf', e.target.value)}>
                            <option>flex-start</option>
                            <option>center</option>
                            <option>flex-end</option>
                         </select>;
        }

        return (
            <div className="form-section">
                <div className='form-btn' onClick={()=>this.props.onSelectImage(this.props.index)}>Change Image</div>
                <div className="form-field">
                    <label>Alignment</label>
                    {alignment}
                </div>
                <div className="form-field">
                    <label>Flex</label>
                    <input type="text" value={this.props.element.containerStyle.flex} onChange={(e)=>this.props.onUpdateContainerProperty('flex', e.target.value)}/>
                </div>
            </div>
        );
    }
}


class LayoutEditor extends React.Component {

    constructor(props){
        super(props);
        this.addText = this.addText.bind(this);
        this.addImage = this.addImage.bind(this);
        this.removeElement = this.removeElement.bind(this);
        this.editPageElement = this.editPageElement.bind(this);
        this.editPage = this.editPage.bind(this);
        this.updatePageProperty = this.updatePageProperty.bind(this);
        this.updateElementProperty = this.updateElementProperty.bind(this);
        this.updateContainerProperty = this.updateContainerProperty.bind(this);
        this.updateText = this.updateText.bind(this);
    }

    addText(){
        this.props.addText();
    }

    addImage(){
        this.props.addImage();
    }

    removeElement(elementIndex){
        this.props.removeElement(elementIndex);
    }

    editPageElement(elementIndex){
        this.props.editPageElement(elementIndex);
    }

    editPage(){
        this.props.editPage();
    }

    updatePageProperty(propName, value){
        this.props.updatePageProperty(propName, value);
    }

    updateElementProperty(propName, value){
        this.props.updateElementProperty(propName, value);
    }

    updateContainerProperty(propName, value){
        this.props.updateContainerProperty(propName, value);
    }

    updateText(newText){
        this.props.updateText(newText);
    }

    render() {
        let _this = this;
        let elements = this.props.elements.map(function(element, index){
            if(element['type']=='text'){
                return (
                    <TextElement language={_this.props.language} index={index} element={element} onRemove={_this.removeElement} onEditPageElement={_this.editPageElement}/>
                );
            }else{
                return (
                    <ImageElement index={index} element={element} onRemove={_this.removeElement} onEditPageElement={_this.editPageElement}/>
                );
            }
        });

        let settings = <PageSettings style={this.props.style} onUpdatePageProperty={this.updatePageProperty}/>
        if(this.props.activeElement && this.props.activeElement.type=='text'){
            settings = <TextSettings onSavePage={this.props.savePage} onUpdateText={this.updateText} onChangeLanguage={this.props.onChangeLanguage} language={this.props.language} element={this.props.activeElement} onUpdateElementProperty={this.updateElementProperty} languages={this.props.languages}/>
        }else if(this.props.activeElement && this.props.activeElement.type=='image'){
            settings = <ImageSettings index={this.props.activeElementIndex} onSelectImage={this.props.openImageSelectModal} element={this.props.activeElement} onUpdateContainerProperty={this.updateContainerProperty} pageStyle={this.props.style}/>
        }

        return (
            <div id="layout-editor">
                <div className="layout-section" style={this.props.style} onClick={this.editPage}>
                    {elements}
                </div>

                <div className="editor-section">
                    <div id="add-text-btn" className="btn" onClick={this.addText}>Add Text</div>
                    <div id="add-image-btn" className="btn" onClick={this.addImage}>Add Image</div>
                    {settings}
                </div>
            </div>
        );
    }
}

const layoutEditorStateMap = (state) => {
    return {
        style: state.pageEditorReducer.style,
        elements: state.pageEditorReducer.elements,
        language: state.pageEditorReducer.language,
        activeElement: state.pageEditorReducer.activeElement,
        activeElementIndex: state.pageEditorReducer.activeElementIndex
    }
}

const layoutEditorDispatchMap = (dispatch) => {
    return {

        addText: () => {
            dispatch(addText());
        },

        addImage: () => {
            dispatch(addImage());
        },

       removeElement: (elementIndex) => {
            dispatch(removeElement(elementIndex));
        },

        editPageElement: (elementIndex) => {
            dispatch(editPageElement(elementIndex));
        },

        editPage: () => {
            dispatch(editPage());
        },

        updatePageProperty: (propName, value) => {
            dispatch(updatePageProperty(propName, value));
        },

        updateElementProperty: (propName, value) => {
            dispatch(updateElementProperty(propName, value));
        },

        updateContainerProperty: (propName, value) => {
            dispatch(updateContainerProperty(propName, value));
        },

        updateText: (newText) => {
            dispatch(updateText(newText));
        },

        openImageSelectModal: () => {
            dispatch(openImageModal());
        },

        //
        onChangeLanguage: (language) => {
            dispatch(changeEditorLanguage(language));
        },

        savePage: () => {
            dispatch(savePage());
        }
    }
}

const LayoutEditorContainer = ReactRedux.connect(
    layoutEditorStateMap,
    layoutEditorDispatchMap
)(LayoutEditor)
