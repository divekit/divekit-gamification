import React,{useContext, useState} from 'react'
import axiosInstance from '../../axios';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../../context/AuthContext';
import jwt from 'jwt-decode';
import "./Login.scss"
import { ThemeContext } from '@emotion/react';

function Login() {
    const { user, setUser } = useContext(AuthContext)
    const {theme,toggleTheme} = useContext(ThemeContext)
    const [userInput,setUserInput] = useState({});
    const [errors,setErrors] = useState(null);
    const navigate = useNavigate();
    const handleInput = (e) => {
        setUserInput({...userInput,[e.target.name]:e.target.value})
    }
    const handleSubmit = (e)=>{
        e.preventDefault();

        axiosInstance.post("/api/v1/token/obtain/",userInput).then(response=>{
            let data = response.data;
            localStorage.setItem('access', data["access"]);
            localStorage.setItem('refresh', data["refresh"]);
            let decodedToken = jwt(data["access"])
            axiosInstance.defaults.headers['Authorization'] = "Bearer "+ data["access"];
            setUser(decodedToken)            
            navigate("/")
        }).catch(error=>{
            console.log("ERROR",error);
            if(error.response){
              if(error.response.status === 400 || error.response.status === 401){
                console.log(error.response.data);
                setErrors(error.response.data);
              }

            }
          })
    }





    return (<div className='login-page'>
    <div className='content'>
    
      <div className='content-title'><h2>Login</h2></div>
      {errors? errors.detail?<div className='error-detail'>{errors.detail}</div>:<></>:<></>}
    
        <div className='form-wrapper'>
          <form>
            <label htmlFor='username'>Username {errors?<div className='error'> {errors.username?errors.username:""}</div>:""}
              <input onInput={handleInput} placeholder='Username' id='username' type="text" name='username'></input>
            </label>
            
            <label htmlFor='password'>Password {errors?<div className='error'> {errors.password?errors.password:""}</div>:""}
              <input onInput={handleInput} placeholder='*********' id='password' type="password" name='password'></input>
            </label>
            
            <div className='password-forgot'><span className='link' onClick={()=>{navigate("/forget")}}>Passwort vergessen? </span></div>
            <button className='btn btn-rounded'  onClick={handleSubmit}>Anmelden</button>
          </form>
          

          
          {/* <div className='form-info'>(*) Required fields</div> */}
        </div>
        
        <div className='have-account'>Falls Sie noch kein Konto haben, können Sie sich <span className='link' onClick={()=>{navigate("/register")}}>hier registrieren</span>.</div>
        
        
      
    </div>  
  </div>
    
  )
}

export default Login