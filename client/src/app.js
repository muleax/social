
class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            header: 'User 1',
            newUserData: null,
            newUser : {
                // TODO: auth
                id: 1,
                firstName: '',
                lastName: '',
                city: '',
                udata: {}
            },
            userListData: null,
            userList : {
                offset: 0,
                limit: 5
            },
            getUserData: null,
            getUser : {
                id: 0
            }
        };
    }

    updateUser = async () => {
        try {
            let response = await axios.post('/update_user', this.state.newUser);
            console.log(response);
            this.setState({newUserData: `${response.data}`});
        } catch (e) {
            this.setState({newUserData: 'FAIL'});
            throw e;
        }
    }

    userList = async () => {
        let response = await axios.get('/user_list', { params: this.state.userList });
        console.log(response);

        let data = JSON.stringify(response.data, null, 2);
        this.setState({ userListData: data });
    }

    getUser = async () => {
        let response = await axios.get('/user', { params: this.state.getUser });
        console.log(response);

        let data = JSON.stringify(response.data, null, 2);
        this.setState({ getUserData: data });
    }

    // TODO: move to separate components
    onNewUserChange = e => this.setState({ newUser: {...this.state.newUser, [e.target.name]:  e.target.value} });
    onUserListChange = e => this.setState({ userList: {...this.state.userList, [e.target.name]:  e.target.value} });
    onGetUserChange = e => this.setState({ getUser: {...this.state.getUser, [e.target.name]:  e.target.value} });

    renderUserList() {
        const userList = this.state.userList;
        return (
            <div>
                <input
                    placeholder = "Offset"
                    name = "offset"
                    value = {userList.offset}
                    onChange = {this.onUserListChange}
                />
                <input
                    placeholder = "Limit"
                    name = "limit"
                    value = {userList.limit}
                    onChange = {this.onUserListChange}
                />
                <button onClick={this.userList} type='button'>Get User List</button>
                <pre>{this.state.userListData}</pre>
            </div>
        );
    }

    renderUpdateUser() {
        const newUser = this.state.newUser;
        return (
            <form>
                <div>
                    <input
                        id="newFirstName"
                        placeholder="First name"
                        name="firstName"
                        value={newUser.firstName}
                        onChange={this.onNewUserChange}
                    />
                    <input
                        id="newLastName"
                        placeholder="Last name"
                        name="lastName"
                        value={newUser.lastName}
                        onChange={this.onNewUserChange}
                    />
                    <input
                        id="newCity"
                        placeholder="City"
                        name="city"
                        value={newUser.city}
                        onChange={this.onNewUserChange}
                    />
                    <button onClick={this.updateUser} type='button'>Update User</button>
                    <pre>{this.state.newUserData}</pre>
                </div>
            </form>
        );
    }

    renderGetUser() {
        const getUser = this.state.getUser;
        return (
            <div>
                <input
                    placeholder = "ID"
                    name = "id"
                    value = {getUser.id}
                    onChange = {this.onGetUserChange}
                />
                <button onClick = {this.getUser} type = 'button'>Get User</button>
                <pre>{this.state.getUserData}</pre>
            </div>
        );
    }

    render() {
        return (
            <div>
                <h3>{this.state.header}</h3>
                {this.renderUpdateUser()}
                {this.renderGetUser()}
                {this.renderUserList()}
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('root'))
