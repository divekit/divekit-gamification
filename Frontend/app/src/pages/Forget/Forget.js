import { useNavigate } from "react-router-dom"
import React,{useState} from 'react'
import "./Forget.scss"
import axiosInstance from "../../axios";

function Forget() {
    const navigate = useNavigate();
    const [userInput,setUserInput] = useState({});

    const [errors,setErrors] = useState(null);
    const handleInput = (e) => {
        setUserInput({...userInput,[e.target.name]:e.target.value})
    }

    const handleSubmit = (e)=>{
        e.preventDefault();
        
        axiosInstance.put("/api/v1/users/refresh/",userInput).then(response=>{
            // let data = response.data;
            // localStorage.setItem('access', data["access"]);
            // localStorage.setItem('refresh', data["refresh"]);
            // let decodedToken = jwt(data["access"])
            // axiosInstance.defaults.headers['Authorization'] = "Bearer "+ data["access"];
            // setUser(decodedToken)        
            console.log("ASDAF",response)    
            // navigate("/login?flashMessage='Das neue Passwort wurde an '")
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

  return (
    <div className='forget-page'>
    <div className='content'>
    
      <div className='content-title'><h2>Passwort zurücksetzen</h2></div>
      {errors? errors.detail?<div className='error-detail'>{errors.detail}</div>:<></>:<></>}
    
        <div className='form-wrapper'>
          <form>
            <label htmlFor='emailInput'>Email
              <input onInput={handleInput} placeholder='Email' id='emailInput' type="email" name='email'></input>
            </label>
            
            {/* <label htmlFor='password'>Password {errors?<div className='error'> {errors.password?errors.password:""}</div>:""} */}
              {/* <input onInput={handleInput} placeholder='*********' id='password' type="password" name='password'></input> */}
            {/* </label> */}
            
            {/* <div className='password-forgot'><span className='link' onClick={()=>{navigate("/forget")}}>Passwort vergessen? </span></div> */}
            <button className='btn btn-rounded'  onClick={handleSubmit}>Anmelden</button>
          </form>
          

          
          {/* <div className='form-info'>(*) Required fields</div> */}
        </div>
        
        <div className='have-account'><span className='link' onClick={()=>{navigate("/login")}}>Zurück zum Login</span>.</div>
        
        
      
    </div>  
  </div>
  )
}

export default Forget