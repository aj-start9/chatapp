import React from 'react'
import Layout from './../../hoc/Layout/Layout'
import GoogleLogin from 'react-google-login';
import io from 'socket.io-client';
import Axios from 'axios'
import classes from './auth.module.css'
import { LinkedIn } from 'react-linkedin-login-oauth2';



class Auth extends React.Component {

    responseGoogle = (response) => {
        console.log(response)
        Axios.post('http://localhost:5000/register?authType=google', { token: response.tokenId },{withCredentials:true})
            .then(res => {
                console.log(res.data)
                // document.cookie = `access_token_cookie=${res.data.access_token}`;
                // localStorage.setItem('idtoken', res.data.access_token)
                // this.props.history.push('/chat')
                // // document.cookie = 'access_token_cookie=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
            })

    }

    handleSuccess = (data) => {
        console.log(data)
    }


    handleFailure = (error) => {
        console.log(error)
    }

    render() {
        return (
            <Layout>
                <div className={classes.main_div}>
                    <GoogleLogin
                        clientId="245937553496-jj986qcag03f80buncc0grjq5mos2vun.apps.googleusercontent.com"
                        buttonText="GOOGLE SIGNIN"
                        onSuccess={this.responseGoogle}
                        // onFailure={this.responseGoogle }
                        cookiePolicy={'single_host_origin'}
                        uxMode="popup"
                    />
                    <LinkedIn
                        clientId="78f2x3kppicuu0"
                        onFailure={this.handleFailure}
                        onSuccess={this.handleSuccess}
                        redirectUri="http://localhost:3000"
                        scope="r_emailaddress"
                    >
                    </LinkedIn>
                </div>
            </Layout>
        )
    }
}


export default Auth