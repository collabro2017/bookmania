class FeatureTaggingAnalytics extends React.Component {
    render() {
        let percent = this.props.analytics.percent;
        return (
            <div className="tag-progress">
                <label>{this.props.analytics.name}</label>
                <div className="progress pull-right">
                    <div className="progress-bar progress-bar-info" style={{width: percent + '%'}}></div>
                    <div className="percent">{percent}%</div>
                </div>
            </div>
        );
    }
}

class LanguageTaggingAnalytics extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            'collapsibleOpened': false
        }
        this.toggleCollapsible = this.toggleCollapsible.bind(this);
    }

    toggleCollapsible(){
        this.setState({
            collapsibleOpened: !this.state.collapsibleOpened
        });
    }

    render() {
        let featureAnalytics = []
        let features = this.props.analytics.features;
        for(var i=0; i<features.length; i++){
            featureAnalytics.push(<FeatureTaggingAnalytics analytics={features[i]}></FeatureTaggingAnalytics>);
        }

        let percent = this.props.analytics.percent;
        return (
            <div className="analytics-sub-panel">
                <div className="title-bar" onClick={this.toggleCollapsible}>
                    <label>{this.props.analytics.name}</label>

                    <div className="pull-right">
                        <div className="progress">
                            <div className="progress-bar progress-bar-info" style={{width: percent + '%'}}></div>
                            <div className="percent">{percent}%</div>
                        </div>
                        <i className="expand-btn fa fa-angle-down"></i>
                    </div>
                </div>

                {this.state.collapsibleOpened &&
                    <div className="collapsible">
                        {featureAnalytics}
                    </div>
                }

            </div>
        );
    }
}

class BookTaggingAnalytics extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            'collapsibleOpened': false
        }
        this.toggleCollapsible = this.toggleCollapsible.bind(this);
    }

    toggleCollapsible(){
        this.setState({
            collapsibleOpened: !this.state.collapsibleOpened
        });
    }

    render() {

        let languageAnalytics = [];
        let languages = this.props.analytics.languages;
        for(var i=0; i<languages.length; i++){
            languageAnalytics.push(<LanguageTaggingAnalytics analytics={languages[i]}></LanguageTaggingAnalytics>);
        }

        let percent = this.props.analytics.percent;
        return (
            <div className="analytics-panel">
                <div className="title-bar" onClick={this.toggleCollapsible}>
                    <label>Tagging</label>

                    <div className="pull-right">
                        <div className="progress">
                            <div className="progress-bar progress-bar-info" style={{width: percent + '%'}}></div>
                            <div className="percent">{percent}%</div>
                        </div>
                        <i className="expand-btn fa fa-angle-down"></i>
                    </div>
                </div>

                {this.state.collapsibleOpened &&
                    <div className="collapsible">
                        {languageAnalytics}
                    </div>
                }

            </div>
        );
    }
}