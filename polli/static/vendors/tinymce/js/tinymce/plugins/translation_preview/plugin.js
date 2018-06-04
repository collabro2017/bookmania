tinymce.PluginManager.add('translation_preview', function(editor, url) {

    editor.addButton('translation_preview', {
        text: 'Preview',
        icon: false,
        onclick: function() {
            console.log('preview the translation');
            var content = editor.getContent();
            $('#previewModal .modal-body').html(content);
            $('#previewModal').modal();
        }
    });

});
