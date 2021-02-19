import React from 'react'
import io from 'socket.io-client';
import classes from './chat.module.css'
import Sidebar from './sidebar/sidebar'
import Content from './content/content'
import Axios from 'axios';


let socket = io.connect(`http://localhost:5000`, {
    path: '/socket.io/item'
});

class Chat extends React.Component {

    state = {
        message: '',
        message_list: []
    }

    componentDidMount() {
        console.log(localStorage.getItem('idtoken'))

        let socket = io.connect(`http://localhost:5000`, {
            path: '/socket.io/item'
        });
        socket.on('connect', function () { console.log('connected') });
        socket.on('news', (data) => {
            let data1 = JSON.parse(data.items)
            console.log(typeof (data1))
            console.log(data1)
            this.setState({ message_list: data1 })
        });
    }

    send = (e) => {
        e.preventDefault()
        // socket.emit('push', { item: this.state.message })
        Axios.post('http://localhost:5000/item', { item: this.state.message },{withCredentials:true})
        .then(res=>{
            console.log(res.data)
        })
    }


    messgeHandler = (e) => {
        this.setState({ message: e.target.value })
    }


    render() {


        return (
            <div className={classes.main_div}>
                <input type="text" value={this.state.message} onChange={e => this.messgeHandler(e)} />
                <button onClick={this.send}>Send</button>
                {this.state.message_list.map((message, index) => <p key={index}>   {message.item}</p>)}
                {/* <div className={classes.sidebar}> 
                        <Sidebar />
                    </div>
                    <div className={classes.content}>
                        <Content />
                    </div> */}

            </div>
        )
    }
}

export default Chat