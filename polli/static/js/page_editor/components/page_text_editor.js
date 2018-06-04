class PageTextEditor{
    constructor(store){
        // Initialize TinyMCE
        var _this = this;
        tinymce.init({
            selector:'#tinymce',
            plugins: 'code',
            content_css : window.tinymceStyles,
            menubar: false,
            height: 200,
            toolbar: false,
            setup: function(editor){

            }
        }).then(function(editors) {
            _this.editor = editors[0];
            _this.editor.on('KeyUp', function (e) {
                console.log('Update Text - temporarily suspended');
                //_this.updateText();
            });
            _this.editor.on('Blur', function (e) {
                console.log('Save Page - temporarily suspended');
                //_this.store.dispatch(savePage());
            });
            _this.editor.store = _this.store;
            _this.editor.show();

            // Display Editor Controls
            $('.tinymce-wrapper .editor-controls').fadeIn();

            // Display Status Bar
            $('.tinymce-wrapper .status-bar').fadeIn();

            // Get Initial Content
            _this.handleStateChange();
        });

        // Setup Store Event Handlers
        this.store = store;
        this.handleStateChange = this.handleStateChange.bind(this);
        this.store.subscribe(this.handleStateChange);
    }

    handleStateChange(){
        let state = this.store.getState().pageEditorReducer;
        let content = '';

        // Get Content
        if(state.textSelectionTarget!=null && state.textSelectionTarget in state.elements){
            var targetText = state.elements[state.textSelectionTarget];
            if(state.language in targetText){
                content = targetText['data'][state.language];
            }
        }

        // Handle Focus Request
        if(state.focusEditor == true){
            this.editor.focus();
            this.store.dispatch(editorFocusComplete());
        }

        // Set Content
        this.setContent(content);
    }

    updateText(){
        let text = this.getContent('text');
        this.store.dispatch(updateText(text));
    }

    getContent(format){
        return this.editor.getContent({format : format});
    }

    setContent(content){
        this.editor.setContent(content);
        this.editor.selection.select(this.editor.getBody(), true);
        this.editor.selection.collapse(false);
    }
}