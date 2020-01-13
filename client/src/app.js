
class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            header: 'Social',
            users: null,
            newUser : {
                firstName: '',
                lastName: '',
                city: ''
            }
        };
    }

    async createUser() {
        let response = await axios.post('/create_user', this.state.newUser);
        console.log(response);
    }

    async updateUsers() {
        let response = await axios.get('/users');
        console.log(response);
        this.setState({users: JSON.stringify(response.data, null, 2)});
    }

    onNewUserChange = e => {
        let newUser = Object.assign({}, this.state.newUser);
        newUser[e.target.name] = e.target.value;
        this.setState({ newUser })
    }

    renderUsers() {
        return (
            <div>
                <button onClick={async () => await this.updateUsers()} type='button'>Update Users</button>
                <pre>{this.state.users}</pre>
            </div>
        );
    }

    renderCreateUser() {
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
                    <button onClick={async () => await this.createUser()} type='button'>Create User</button>
                </div>
            </form>
        );
    }

    render() {
        return (
            <div>
                <h3>{this.state.header}</h3>
                {this.renderCreateUser()}
                {this.renderUsers()}
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('root'))
