
class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            header: 'Social',
            users: null
        };
    }

    async addUser() {

    }

    async showUsers() {
        let response = await axios.get('/users');
        let users = JSON.stringify(response.data);
        this.setState({users});
    }

    renderUsers() {
        if (!this.state.users) {
            return null;
        }

        return (
            <div>
                {this.state.users}
            </div>
        );
    }

    render() {
        return (
            <div>
                <h3>{this.state.header}</h3>
                <button onClick={async () => await this.showUsers()}>Show Users</button>
                {this.renderUsers()}
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('root'))
