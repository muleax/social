// @formatter:off
class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user_id: null,
            auth_token: null,

            auth : {
                login: 'nagibator2005',
                password: 'qwerty'
            },
            authResponse: null,

            user : {
                first_name: '',
                last_name: '',
                city: '',
                udata: {}
            },
            userConfirmed: {
                json: '',
                first_name: '',
                last_name: ''
            },
            updateUserResponse: null,

            getUserList : {
                offset: 0,
                limit: 5
            },
            getUserListResponse: null,

            getUser : {
                user_id: 0
            },
            getUserResponse: null
        };
    }

    getUserList = async () => {
        try {
            let response = await axios.get('/user_list', { params: this.state.getUserList });
            console.log(response);
            this.setState({ getUserListResponse: JSON.stringify(response.data, null, 2) });
        } catch (e) {
            this.setState({ getUserListResponse: e.message });
            throw e;
        }
    }

    // TODO: move to separate components
    onGetUserListChange = e => this.setState({ getUserList: {...this.state.getUserList, [e.target.name]:  e.target.value} });

    renderGetUserList() {
        const getUserList = this.state.getUserList;
        return (
            <div>
                <input
                    placeholder = "Offset"
                    name = "offset"
                    value = {getUserList.offset}
                    onChange = {this.onGetUserListChange}
                />
                <input
                    placeholder = "Limit"
                    name = "limit"
                    value = {getUserList.limit}
                    onChange = {this.onGetUserListChange}
                />
                <button onClick={this.getUserList} type='button'>Get User List</button>
                <pre>{this.state.getUserListResponse}</pre>
            </div>
        );
    }

    getUser = async () => {
        try {
            let response = await axios.get('/user', { params: this.state.getUser });
            console.log(response);
            this.setState({ getUserResponse: JSON.stringify(response.data, null, 2) });
        } catch (e) {
            this.setState({ getUserResponse: e.message });
            throw e;
        }
    }

    onGetUserChange = e => this.setState({ getUser: {...this.state.getUser, [e.target.name]:  e.target.value} });

    renderGetUser() {
        const getUser = this.state.getUser;
        return (
            <div>
                <input
                    placeholder = "ID"
                    name = "user_id"
                    value = {getUser.user_id}
                    onChange = {this.onGetUserChange}
                />
                <button onClick = {this.getUser} type = 'button'>Get User</button>
                <pre>{this.state.getUserResponse}</pre>
            </div>
        );
    }

    updateUser = async () => {
        try {
            let payload = {
                user_id: this.state.user_id,
                auth_token: this.state.auth_token,
                data: this.state.user
            }
            let response = await axios.post('/update_user', payload);
            console.log(response);

            let userConfirmed = {
                json: JSON.stringify(response.data, null, 2),
                first_name: response.data.first_name,
                last_name: response.data.last_name,
            }

            this.setState({
                userConfirmed,
                updateUserResponse: `${response.status}`
            });
        } catch (e) {
            this.setState({updateUserResponse: e.message})
            throw e;
        }
    }

    onUserChange = e => this.setState({ user: {...this.state.user, [e.target.name]:  e.target.value} });

    renderUpdateUser() {
        const user = this.state.user;
        return (
            <div>
                <input
                    id="newFirstName"
                    placeholder="First name"
                    name="first_name"
                    value={user.first_name}
                    onChange={this.onUserChange}
                />
                <input
                    id="newLastName"
                    placeholder="Last name"
                    name="last_name"
                    value={user.last_name}
                    onChange={this.onUserChange}
                />
                <input
                    id="newCity"
                    placeholder="City"
                    name="city"
                    value={user.city}
                    onChange={this.onUserChange}
                />
                <button onClick={this.updateUser} type='button'>Update User</button>
                <pre>{this.state.updateUserResponse}</pre>
            </div>
        );
    }

    renderHomePage() {
        let userConfirmed = this.state.userConfirmed;
        return (
            <div>
                <h3> {userConfirmed.first_name} {userConfirmed.last_name} </h3>
                <pre>{userConfirmed.json}</pre>
                {this.renderUpdateUser()}
                {this.renderGetUser()}
                {this.renderGetUserList()}
            </div>
        );
    }

    auth = async () => {
        try {
            let authResponse = await axios.get('/auth', { params: this.state.auth });
            console.log(authResponse);
            let user_id = authResponse.data.user_id;
            this.setState({
                user_id,
                auth_token: authResponse.data.auth_token,
                authResponse: `${authResponse.status}`
            });

            let response = await axios.get('/user', { params: {user_id} });
            console.log(response);

            let userConfirmed = {
                json: JSON.stringify(response.data, null, 2),
                first_name: response.data.first_name,
                last_name: response.data.last_name,
            }

            this.setState({
                userConfirmed,
                user: response.data,
            });
        } catch (e) {
            this.setState({authResponse: e.message})
            throw e;
        }
    }

    createAccount = async () => {
        try{
            let response = await axios.post('/create_account', this.state.auth);
            console.log(response);
            this.setState({authResponse: `${response.status}`});
        } catch (e) {
            this.setState({authResponse: e.message})
            throw e;
        }
    }

    onAuthChange = e => this.setState({ auth: {...this.state.auth, [e.target.name]:  e.target.value} });

    renderAuth() {
        const auth = this.state.auth;
        return (
            <div>
                <h3> Auth </h3>
                <input
                    placeholder = "Login"
                    name = "login"
                    value = {auth.login}
                    onChange = {this.onAuthChange}
                />
                <input
                    placeholder = "Password"
                    name = "password"
                    value = {auth.password}
                    onChange = {this.onAuthChange}
                />
                <button onClick = {this.auth} type = 'button'>Sign In</button>
                <button onClick = {this.createAccount} type = 'button'>Create Account</button>
                <pre>{this.state.authResponse}</pre>
            </div>
        );
    }

    render() {
        if (this.state.auth_token) {
            return this.renderHomePage();
        } else {
            return this.renderAuth();
        }
    }
}

ReactDOM.render(<App />, document.getElementById('root'))
// @formatter:on
