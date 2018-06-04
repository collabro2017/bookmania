class ImageSelectorModal extends React.Component {
    constructor(props){
        super(props);
        this.imageSelected = this.imageSelected.bind(this);

        this.state = {
            images: this.props.images
        };

        this.uploadImage = this.uploadImage.bind(this);
        this.selectUploadImage = this.selectUploadImage.bind(this);
        this.deleteImage = this.deleteImage.bind(this);
    }

    imageSelected(event, imageUrl, thumbnailUrl){
        event.stopPropagation();
        this.props.onImageSelected(imageUrl, thumbnailUrl);
    }

    stopEventPropagation(event){
        console.log('stop event propagation');
        event.stopPropagation();
    }

    uploadImage(event){
        var data = new FormData();
        data.append('image', this.uploadInput.files[0]);
        data.append('thumbnail', this.uploadInput.files[0]);
        data.append('book', this.props.bookID);

        var _this = this;
        $.ajax({
            url: '/publisher/image/',
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
            success: function(data, textStatus, jqXHR)
            {
                //data = JSON.parse(data);
                console.log(data);
                var newImage = {
                    'id': data.id,
                    'url': data.image,
                    'thumbnail_url': data.thumbnail
                }
                _this.setState({
                    images: _this.state.images.concat([newImage])
                });

                console.log(data);
            }
        }, 'json');
    }

    selectUploadImage(event){
        event.stopPropagation();
        this.uploadInput.click();
    }

    deleteImage(event, imageID){
        event.stopPropagation();

        this.setState({
            images: this.state.images.filter(function(img){
                return img.id!=imageID;
            })
        });

        $.ajax({
            url: '/publisher/image/'+imageID+'/',
            type: 'DELETE',
            success: function(data, textStatus, jqXHR)
            {
                console.log('Image Delete');
            }
        }, 'json');

    }

    render() {
        if(this.props.showImageSelector){
            let images = this.state.images.map((image, index) => (
                                <div className="img-wrap col-md-3">
                                    <i className="fa fa-times" onClick={(event) => this.deleteImage(event, image.id)}></i>
                                    <img src={image.thumbnail_url} onClick={(event) => this.imageSelected(event, image.url, image.thumbnail_url)} />
                                </div>
                            ));

            return (
                <div>
                    <div className="modal show" id="image-select-modal" role="dialog"  tabindex="-1" onClick={()=>this.props.onModalClosed()}>
                        <div className="modal-dialog" role="document">
                            <div className="modal-content">

                                <div className="modal-header">
                                    <h4 className="modal-title" id="myModalLabel">
                                        <i className="fa fa-camera"></i>
                                        <span>Image Select</span>
                                    </h4>
                                    <button className="close-btn"><i className="fa fa-times" aria-hidden="true"></i></button>
                                </div>

                                <div className="modal-body">
                                    <div className="container-fluid">
                                        <div className="row">
                                            {images}
                                        </div>
                                    </div>
                                </div>
                                <div className="modal-footer">
                                    <button className="btn btn-info upload-btn" onClick={(e)=>this.selectUploadImage(e)}>Upload Image</button>
                                </div>
                                <input type='file' ref={(input) => { this.uploadInput = input; }} onClick={(e)=>this.stopEventPropagation(e)} onChange={(e)=>this.uploadImage()}/>
                            </div>
                        </div>
                    </div>
                    <div className="modal-backdrop" ></div>
                </div>
            );
        }else{
            return null;
        }
    }
}

const imageSelectorStateMap = (state) => {
    return {
        showImageSelector: state.imageSelectorReducer.showImageSelector,
        bookID: state.bookEditorReducer.id
    }
}

const imageSelectorDispatchMap = (dispatch) => {
    return {
        onModalClosed: () => {
            dispatch(closeImageModal())
        },
        onImageSelected: (imgUrl, thumbnailUrl) => {
            dispatch(imageSelected(imgUrl, thumbnailUrl))
        },
    }
}

const ImageSelectorModalContainer = ReactRedux.connect(
    imageSelectorStateMap,
    imageSelectorDispatchMap
)(ImageSelectorModal)