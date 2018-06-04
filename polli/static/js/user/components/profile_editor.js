class ProfileEditor extends React.Component {

    constructor(props){
        super(props);
        this.state = {
                        profile_pic: this.props.user.profile_pic,
                        first_name: this.props.user.first_name,
                        last_name: this.props.user.last_name,
                        email: this.props.user.email,
                        phone: this.props.user.phone,
                    };

        this.selectProfilePic = this.selectProfilePic.bind(this);
        this.updateProfilePic = this.updateProfilePic.bind(this);
        this.saveProfile = this.saveProfile.bind(this);
    }

    selectProfilePic(){
        this.picInput.click();
    }

    updateProfilePic(){
        var data = new FormData();
        data.append('image', this.picInput.files[0]);
        data.append('name', 'profile_pic_name');

        var _this = this;
        $.ajax({
            url: '/user/change-profile-pic/',
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
            success: function(data, textStatus, jqXHR)
            {
                data = JSON.parse(data);
                _this.setState({
                    profile_pic: data.thumbnail_url,
                    first_name: 'johnny'
                });
            }
        }, 'json');
    }

    saveProfile(){
        $.post('/user/update-profile/', this.state, function(resp){
            $('.save-complete-msg').animate({opacity:1});
            setTimeout(()=>{
                $('.save-complete-msg').animate({opacity:0});
            }, 2000);
        }, 'json');


    }

    render() {
        return (
            <div>
                <div className="col-md-4">
                    <div className="profile-pic-wrap" onClick={this.selectProfilePic}>
                        <div className="overlay">
                            <i className="fa fa-camera-retro"></i>
                        </div>
                        <img src={this.state.profile_pic}/>
                    </div>
                    <input type='file' ref={(input) => { this.picInput = input; }} onChange={this.updateProfilePic}/>
                </div>
                <div className="col-md-4">
                    <div>
                        <div className="form-group col-md-6 form-group-left">
                            <label>First Name</label>
                            <input type="text" className="form-control" placeholder="First Name"
                                value={this.state.first_name}
                                onChange={(e)=>{this.setState({first_name: e.target.value})}}
                                />
                        </div>
                        <div className="form-group col-md-6 form-group-right">
                            <label>Last Name</label>
                            <input type="text" className="form-control"  placeholder="Last Name"
                                value={this.state.last_name}
                                onChange={(e)=>{this.setState({last_name: e.target.value})}}
                                />
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Email</label>
                        <input type="text" className="form-control"  placeholder="Email"
                            value={this.state.email}
                            onChange={(e)=>{this.setState({email: e.target.value})}}
                            />
                    </div>

                    <div className="form-group">
                        <label>Phone</label>
                        <input type="text" className="form-control"  placeholder="xxx-xxx-xxxx"
                            value={this.state.phone}
                            onChange={(e)=>{this.setState({phone: e.target.value})}}
                            />
                    </div>

                    <div className="control-group">
                        <span className="save-complete-msg"><i className="fa fa-floppy-o"></i>Complete</span>

                        <div className="btn btn-info save-btn" onClick={this.saveProfile}>Save</div>
                    </div>
                </div>
            </div>
        );
    }
}