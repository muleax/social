// @formatter:off
class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user_id: localStorage.getItem('user_id'),
            auth_token: localStorage.getItem('auth_token'),

            auth : {
                login: 'kotik_kotik',
                password: 'kotik'
            },
            authResponse: null,

            createAccount : {
                login: '',
                password: ''
            },
            createAccountResponse: null,

            user : {
                first_name: '',
                last_name: '',
                city: '',
                birth_date: '',
                udata: {}
            },
            userConfirmed: {
                json: '',
                first_name: '',
                last_name: ''
            },
            updateUserResponse: null,

            getUserList : {
                limit: 20,
                offset: 0
            },
            getUserListResponse: null,

            getUser : {
                user_id: 0
            },
            getUserResponse: null,

            findUsers : {
                first_name: '',
                last_name: '',
                city: '',
                age_from: 14,
                age_to: 35,
                limit: 10,
                offset: 0
            },
            findUsersResponse: null
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
            <div className="border">
                <input
                    placeholder = "Limit"
                    name = "limit"
                    value = {getUserList.limit}
                    onChange = {this.onGetUserListChange}
                />
                <input
                    placeholder = "Offset"
                    name = "offset"
                    value = {getUserList.offset}
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
            <div className="border">
                <input
                    placeholder = "ID"
                    name = "user_id"
                    value = {getUser.user_id}
                    onChange = {this.onGetUserChange}
                />
                <button onClick = {this.getUser} type = 'button'>Get User By ID</button>
                <pre>{this.state.getUserResponse}</pre>
            </div>
        );
    }

    updateUserView = async () => {
        let response = await axios.get('/user', { params: {user_id: this.state.user_id} });
        console.log(response);
        let data = response.data;

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
                ...this.state.user,
                user_id: this.state.user_id,
                auth_token: this.state.auth_token,
            }
            let response = await axios.post('/update_user', payload);
            console.log(response);

            this.setState({
                updateUserResponse: `${response.status}`
            });

            await this.updateUserView();
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
            <div className="border">
                <h3> {userConfirmed.first_name} {userConfirmed.last_name} </h3>
                <pre>{userConfirmed.json}</pre>
                <div>
                    <input
                        placeholder="First Name"
                        name="first_name"
                        value={user.first_name}
                        onChange={this.onUserChange}
                    />
                    <input
                        placeholder="Last Name"
                        name="last_name"
                        value={user.last_name}
                        onChange={this.onUserChange}
                    />
                    <input
                        placeholder="City"
                        name="city"
                        value={user.city}
                        onChange={this.onUserChange}
                    />
                    <input
                        placeholder="Birth Date"
                        name="birth_date"
                        value={user.birth_date}
                        onChange={this.onUserChange}
                    />
                    <button onClick={this.updateUser} type='button'>Update User</button>
                    <pre>{this.state.updateUserResponse}</pre>
                </div>
            </div>
        );
    }

    findUsers = async () => {
        try {
            let params = {
                user_id: this.state.user_id,
                auth_token: this.state.auth_token,
            };

            // filter out empty strings
            for (const [key, value] of Object.entries(this.state.findUsers)) {
                if (value !== "") {
                    params[key] = value;
                }
            }

            let response = await axios.get('/find_users', { params });
            console.log(response);
            this.setState({ findUsersResponse: JSON.stringify(response.data, null, 2) });

            this.setState({
                updateUserResponse: `${response.status}`
            });
        } catch (e) {
            this.setState({findUsersResponse: e.message})
            throw e;
        }
    }

    onFindUsersChange = e => this.setState({ findUsers: {...this.state.findUsers, [e.target.name]:  e.target.value} });

    renderFindUsers() {
        const findUsers = this.state.findUsers;
        return (
            <div className="border">
                <div>
                    <input
                        placeholder="First name"
                        name="first_name"
                        value={findUsers.first_name}
                        onChange={this.onFindUsersChange}
                    />
                    <input
                        placeholder="Last name"
                        name="last_name"
                        value={findUsers.last_name}
                        onChange={this.onFindUsersChange}
                    />
                    <input
                        placeholder="City"
                        name="city"
                        value={findUsers.city}
                        onChange={this.onFindUsersChange}
                    />
                    <input
                        placeholder="Age From"
                        name="age_from"
                        value={findUsers.age_from}
                        onChange={this.onFindUsersChange}
                    />
                    <input
                        placeholder="Age To"
                        name="age_to"
                        value={findUsers.age_to}
                        onChange={this.onFindUsersChange}
                    />
                    <input
                        placeholder = "Limit"
                        name = "limit"
                        value = {findUsers.limit}
                        onChange = {this.onFindUsersChange}
                    />
                    <input
                        placeholder = "Offset"
                        name = "offset"
                        value = {findUsers.offset}
                        onChange = {this.onFindUsersChange}
                    />
                    <button onClick={this.findUsers} type='button'>Find Users</button>
                    <pre>{this.state.findUsersResponse}</pre>
                </div>
            </div>
        );
    }

    renderHomePage() {
        return (
            <div>
                <button onClick = {this.logout} type = 'button'>Sign Out</button>
                {this.renderUpdateUser()}
                {this.renderFindUsers()}
                {this.renderGetUser()}
                {this.renderGetUserList()}
            </div>
        );
    }

    createAccount = async () => {
        try{
            let response = await axios.post('/create_account', this.state.createAccount);
            console.log(response);
            this.setState({
                createAccountResponse: `${response.status}`,
                auth: Object.assign({}, this.state.createAccount)
            });
        } catch (e) {
            this.setState({createAccountResponse: e.message})
            throw e;
        }
    }

    onCreateAccountChange = e => this.setState({ createAccount: {...this.state.createAccount, [e.target.name]:  e.target.value} });

    renderCreateAccount() {
        return (
            <div className="border">
                <h3> Create Account </h3>
                <input
                    placeholder = "Login"
                    name = "login"
                    value = {this.state.createAccount.login}
                    onChange = {this.onCreateAccountChange}
                />
                <input
                    placeholder = "Password"
                    name = "password"
                    value = {this.state.createAccount.password}
                    onChange = {this.onCreateAccountChange}
                />
                <button onClick = {this.createAccount} type = 'button'>Create Account</button>
                <pre>{this.state.createAccountResponse}</pre>
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

    auth = async () => {
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

            await this.updateUserView();
        } catch (e) {
            this.setState({authResponse: e.message})
            throw e;
        }
    }

    onAuthChange = e => this.setState({ auth: {...this.state.auth, [e.target.name]:  e.target.value} });

    renderAuth() {
        const auth = this.state.auth;
        return (
            <div className="border">
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
                <pre>{this.state.authResponse}</pre>
            </div>
        );
    }

    renderAuthPage() {
        return (
            <div>
                {this.renderAuth()}
                {this.renderCreateAccount()}
            </div>
        );
    }

    render() {
        if (this.state.auth_token && this.state.user_id) {
            return this.renderHomePage();
        } else {
            return this.renderAuthPage();
        }
    }
}

ReactDOM.render(<App />, document.getElementById('root'))
// @formatter:on
