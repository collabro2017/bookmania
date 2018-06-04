class PageTextEditor{
    constructor(store){
        // Initialize TinyMCE
        var _this = this;
        tinymce.init({
            selector:'#tinymce',
            plugins: 'code, tagger',
            content_css : window.tinymceStyles,
            menubar: false,
            height: 350,
            toolbar: false,
            setup: function(editor){
                editor.on("click", function(e) {
                    var targetNode = this.selection.getNode();
                    if(targetNode.nodeName.toLowerCase()=='span'){
                        console.log('clicked a span');

                    }else{
                        console.log('did not click a node');
                    }
                });
            }
        }).then(function(editors) {
            _this.editor = editors[0];
            _this.editor.on('KeyUp', function (e) {
                _this.store.dispatch(updateText(_this.getContent('text'),  _this.getContent('html')));
            });
            _this.editor.on('Blur', function (e) {
                _this.store.dispatch(savePage());
            });
            _this.editor.store = _this.store;
            _this.editor.show();

            // Display Language Selector
            $('.tinymce-wrapper .language-selector').fadeIn();

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
        if(state.textSelectionTarget!=null && state.textSelectionTarget in state.text){
            var targetText = state.text[state.textSelectionTarget];
            if(typeof(targetText)=='object' && state.language in targetText){
                content = targetText[state.language]['tagged'];
            }
        }

        if(state.focusEditor==true){
            this.editor.focus();
            this.store.dispatch(editorFocusComplete());
        }
        this.setContent(content);
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