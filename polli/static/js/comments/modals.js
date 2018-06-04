class NewCommentModal{
    constructor(selector, bookID, pageID){
        var _this = this;
        this.bookID = bookID;
        this.pageID = pageID;

        this.$modal = $(selector);
        this.$typeLabel = this.$modal.find('.select-wrap label');
        this.$typeSelect = this.$modal.find('.select-wrap select');
        this.$typeSelect.change(function(){
            var commentType = $(this).val();
            _this.$typeLabel.text(commentType);
        });

        this.$typeSubject = this.$modal.find('.subject');
        this.$typeMessage = this.$modal.find('.message');
        this.$saveBtn = this.$modal.find('.save-btn');
        this.$saveBtn.click(function(){
            _this.saveComment();
        });

        this.template = _.template($('#new-comment-template').html());
    }

    saveComment(){
        var params = {
            book: this.bookID,
            page: this.pageID,
            type: this.$typeSelect.val(),
            subject: this.$typeSubject.val(),
            message: this.$typeMessage.val(),
        };

        var _this = this;
        $.post('/publisher/comment/', params, function(resp){
            console.log(resp);
            var newComment = _this.template(resp);
            $('.comment-list').prepend(newComment);
        }, 'json');

        this.close();
    }

    resetForm(){
        this.$typeSubject.val('');
        this.$typeMessage.val('');
    }

    open(){
        this.resetForm();
        this.$modal.modal();
    }

    close(){
        this.$modal.modal('hide');
    }
}

class CommentReplyModal{
    constructor(selector, bookID, pageID){
        var _this = this;
        this.bookID = bookID;
        this.pageID = pageID;

        this.$modal = $(selector);
        this.$typeMessage = this.$modal.find('.message');
        this.$saveBtn = this.$modal.find('.save-btn');
        this.$saveBtn.click(function(){
            _this.saveComment();
        });

        this.template = _.template($('#new-reply-template').html());
    }

    saveComment(){
        var params = {
            book: this.bookID,
            page: this.pageID,
            parent_comment: this.parentCommentID,
            message: this.$typeMessage.val(),
        };

        var _this = this;
        $.post('/publisher/comment/', params, function(resp){
            console.log(resp);
            var newComment = _this.template(resp);
            var selector = ".comment-item[data-id='"+_this.parentCommentID+"'] .msg-thread";

            console.log('new comment');
            console.log(selector);
            console.log(newComment);
            $(selector).prepend(newComment);
        }, 'json');

        this.close();
    }

    resetForm(){
        this.$typeMessage.val('');
    }

    open(parentCommentID){
        this.parentCommentID = parentCommentID;
        this.resetForm();
        this.$modal.modal();
    }

    close(){
        this.$modal.modal('hide');
    }
}