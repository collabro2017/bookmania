class BaseLayout extends React.Component {
    getImage(imgId){
        if(imgId in this.props.images){
            let image = this.props.images[imgId];
            return <img src={image.url} onClick={() => this.props.onSelectImage(imgId)}/>
        }else{
            return <img src={this.props.defaultImage} onClick={() => this.props.onSelectImage(imgId)}/>
        }
    }

    getText(textId){
        let text = '[Click to Edit Text]';
        if(textId in this.props.text && this.props.text[textId]){
            //Default to only english for now
            if(typeof(this.props.text[textId])=='object' && 'english' in this.props.text[textId]){
                text = this.props.text[textId]['english']['plain'];
            }
        }

        if(textId==this.props.textSelectionTarget){
            return <p onClick={() => this.props.onSelectText(textId)} className='active-editing'>{text}</p>
        }else{
            return <p onClick={() => this.props.onSelectText(textId)}>{text}</p>
        }
    }
}

class ThreeColumnLayout extends BaseLayout {

    render() {
        let image1 = this.getImage(1);
        let image2 = this.getImage(2);
        let image3 = this.getImage(3);

        let text1 = this.getText(1);
        let text2 = this.getText(2);
        let text3 = this.getText(3);

        return (
            <div className="layout-3-col layout">

                <div className="col">
                    {image1}
                    {text1}
                </div>

                <div className="col">
                    {image2}
                    {text2}
                </div>

                <div className="col">
                    {image3}
                    {text3}
                </div>

            </div>
        );
    }
}

class ThreeRowLayout extends BaseLayout {
    render() {
        let image1 = this.getImage(1);
        let image2 = this.getImage(2);
        let image3 = this.getImage(3);

        let text1 = this.getText(1);
        let text2 = this.getText(2);
        let text3 = this.getText(3);

        return (
            <div className="layout-3-row layout">

                <div className="row">
                    {image1}
                    {text1}
                </div>

                <div className="row">
                    {image2}
                    {text2}
                </div>

                <div className="row">
                    {image3}
                    {text3}
                </div>

            </div>
        );
    }
}

class TopImageLayout extends BaseLayout {
    render() {
        let image1 = this.getImage(1);
        let text1 = this.getText(1);
        return (
            <div className="layout-top-image layout">
                {image1}
                {text1}
            </div>
        );
    }
}

// Layout Types Map
const LAYOUT_TYPES = {
    'top_image': TopImageLayout,
    'three_row': ThreeRowLayout,
    'three_column': ThreeColumnLayout,
}