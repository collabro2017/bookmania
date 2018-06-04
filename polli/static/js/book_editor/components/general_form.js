class GeneralForm extends React.Component {
    constructor(props){
        super(props);
        this.state = Object.assign({}, this.props);
        this.saveForm = this.saveForm.bind(this);
    }

    saveForm(){
        this.props.onSaveForm(this.props.id, this.state.name, this.state.description, this.state.author);
    }

    render() {
        return (
            <div>
                <div className="form-group">
                    <label>Name</label>
                    <input type="text" className="form-control" placeholder="Name"
                        value={this.state.name} onChange={(e) => this.setState({name: e.target.value})}/>
                </div>
                <div className="form-group">
                    <label>Author</label>
                    <input type="text" className="form-control" placeholder="Author"
                        value={this.state.author} onChange={(e) => this.setState({author: e.target.value})}/>
                </div>
                <div className="form-group">
                    <label>Summary</label>
                    <textarea className="form-control" rows="3" placeholder="Summary"
                        value={this.state.description} onChange={(e) => this.setState({description: e.target.value})}></textarea>
                </div>
                <div className='controls'>
                    <span className='save-complete-msg'><i className="fa fa-floppy-o" aria-hidden="true"></i>Save Complete</span>
                    <button className='btn btn-info save-btn' onClick={()=>this.saveForm()}>Save</button>
                </div>
            </div>
        );
    }
}

const generalFormStateMap = (state) => {
    return {
        id: state.bookEditorReducer.id,
        name: state.bookEditorReducer.name,
        description: state.bookEditorReducer.description,
        author: state.bookEditorReducer.author
    }
}

const generalFormDispatchMap = (dispatch) => {
    return {
        onSaveForm: (id, name, description, author) => {
            dispatch(saveBook(id, name, description, author));
        }
    }
}

const GeneralFormContainer = ReactRedux.connect(
    generalFormStateMap,
    generalFormDispatchMap
)(GeneralForm)