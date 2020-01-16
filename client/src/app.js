// @formatter:off
class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user_id: localStorage.getItem('user_id'),
            auth_token: localStorage.getItem('auth_token'),

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

    async componentDidMount() {
        // TODO: refactore
        if (this.state.user_id) {
            await this.updateUserView();
        }
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
            <div class="border">
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
            <div class="border">
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

    updateUserView = async (data) => {
        if (!data) {
            let response = await axios.get('/user', { params: {user_id: this.state.user_id} });
            console.log(response);
            data = response.data;
        }

        let userConfirmed = {
            json: JSON.stringify(data, null, 2),
            first_name: data.first_name,
            last_name: data.last_name,
        }

        this.setState({
            userConfirmed,
            user: data,
        });
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

            this.setState({
                updateUserResponse: `${response.status}`
            });

            this.updateUserView(response.data);
        } catch (e) {
            this.setState({updateUserResponse: e.message})
            throw e;
        }
    }

    onUserChange = e => this.setState({ user: {...this.state.user, [e.target.name]:  e.target.value} });

    renderUpdateUser() {
        const user = this.state.user;
        const userConfirmed = this.state.userConfirmed;
        return (
            <div class="border">
                <h3> {userConfirmed.first_name} {userConfirmed.last_name} </h3>
                <pre>{userConfirmed.json}</pre>
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
            </div>
        );
    }

    renderHomePage() {
        return (
            <div>
                <button onClick = {this.logout} type = 'button'>Sign Out</button>
                {this.renderUpdateUser()}
                {this.renderGetUser()}
                {this.renderGetUserList()}
            </div>
        );
    }

    logout = async () => {
        this.setState({
            user_id: null,
            auth_token: null
        });

        localStorage.removeItem('user_id');
        localStorage.removeItem('auth_token');
    }

    login = async () => {
        try {
            let authResponse = await axios.get('/auth', { params: this.state.auth });
            console.log(authResponse);
            let user_id = authResponse.data.user_id;
            let auth_token = authResponse.data.auth_token;
            this.setState({
                user_id,
                auth_token,
                authResponse: `${authResponse.status}`
            });

            localStorage.setItem('user_id', user_id);
            localStorage.setItem('auth_token', auth_token);

            this.updateUserView();
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
            <div class="border">
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
                <button onClick = {this.login} type = 'button'>Sign In</button>
                <button onClick = {this.createAccount} type = 'button'>Create Account</button>
                <pre>{this.state.authResponse}</pre>
            </div>
        );
    }

    render() {
        if (this.state.auth_token && this.state.user_id) {
            return this.renderHomePage();
        } else {
            return this.renderAuth();
        }
    }
}

ReactDOM.render(<App />, document.getElementById('root'))
// @formatter:on
