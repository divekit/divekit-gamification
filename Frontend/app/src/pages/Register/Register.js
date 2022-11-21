import React,{useState} from 'react'
import axiosInstance from '../../axios';
import { useNavigate } from 'react-router-dom';
import "./Register.scss"

function Register() {


    const [userInput,setUserInput] = useState({});
    const [errors,setErrors] = useState(null);
    const navigate = useNavigate();
    const handleInput = (e) => {
        setUserInput({...userInput,[e.target.name]:e.target.value})
    }
    const handleSubmit = (e)=>{
        e.preventDefault();

        axiosInstance.post("/api/v1/token/create/",userInput).then(response=>{
            navigate("/login")
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


    return (<div className='register-page'>
    <div className='content'>
    <div className='register-page-content'>
      <div className='content-title'><h2>Register</h2></div>
      {errors? errors.detail?<div className='error-detail'>{errors.detail}</div>:<></>:<></>}
    
        <div className='form-wrapper'>
          <label htmlFor='email'>Email {errors?<div className='error'> {errors.email?errors.email:""}</div>:""}</label>
          <input onInput={handleInput} placeholder='Email' id='email' type="email" name='email'></input>

          <label htmlFor='username'>Username {errors?<div className='error'> {errors.username?errors.username:""}</div>:""}</label>
          <input onInput={handleInput} placeholder='Username' id='username' type="text" name='username'></input>

          <label htmlFor='discord-username'>Discord Username {errors?<div className='error'> {errors.discord_username?errors.discord_username:""}</div>:""}</label>
          <input onInput={handleInput} placeholder='Discord Username' id='discord-username' type="text" name='discord_username'></input>

          <label htmlFor='campus-id'>Campus ID {errors?<div className='error'> {errors.campus_id?errors.campus_id:""}</div>:""}</label>
          <input onInput={handleInput} placeholder='Campus ID' id='campus-id' type="text" name='campus_id'></input>

          <label htmlFor='password'>Password {errors?<div className='error'> {errors.password?errors.password:""}</div>:""}</label>
          <input onInput={handleInput} placeholder='Password' id='password' type="password" name='password'></input>
          
          <button type='submit' onClick={handleSubmit}>Register</button>

          
          {/* <div className='form-info'>(*) Required fields</div> */}
        </div>
        
        <div className='have-account'>Have an account? <span onClick={()=>{navigate("/login")}}>Login</span></div>
        
        
    </div>
  
    </div>  
  </div>
    
  )
}

export default Register