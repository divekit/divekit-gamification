import React,{useContext, useEffect, useRef, useState} from 'react'
import Sidebar from '../../components/Sidebar/Sidebar'
import "./Profile.scss"
import {useNavigate, useParams} from "react-router-dom";
import AuthContext from '../../context/AuthContext';
import axiosInstance from '../../axios';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import Card from '../../components/Card/Card';
import jwt from 'jwt-decode';

function Profile() {
  const { user, setUser } = useContext(AuthContext);
  const imageButton = useRef()
  const [uploadedImg,setUploadedImg] = useState(null)
  const [profile,setProfile] = useState(null)
  const [password,setPassword] = useState(null)
  const [isEditing,setIsEditing] = useState(false)
  // const [isChanged,setIsChanged] = useState(false)
  const [responses,setResponses] = useState(null)

  const navigate = useNavigate();

  useEffect(()=>{
    if(user){
      console.log(user)
      axiosInstance.get("/api/v1/users/"+user.user_id).then(response=>{
        setProfile(response.data)
      })
    }

  },[user])
  
  const onImageChange = (e) =>{
    console.log("IMG CHANGE")
    setUploadedImg(URL.createObjectURL(e.target.files[0]))
  }

  const handleImageUpload = (e)=>{
    imageButton.current.click()
  }

  const handleInput = (e) => {
    
    if(e.target.type === "checkbox"){
      setProfile({...profile,[e.target.name]:e.target.checked})
    }
    else{
      setProfile({...profile,[e.target.name]:e.target.value})
    }
  }

  const handlePassword = (e)=>{
    // console.log(e.target.name)
    console.log(e.target.name,e.target.value)
    setPassword({...password,[e.target.name]:e.target.value})
  }

  const handleSaveProfile = (e)=>{
    console.log(profile)
    let tempProfile = Object.assign({}, profile);
    delete tempProfile.img
    let tmpResponses = []

    if(uploadedImg){
      let data = new FormData();
      // console.log('imageButton.current.files[0]', imageButton.current.files[0])
      data.append("img", imageButton.current.files[0])
      axiosInstance.put(
        "api/v1/users/"+profile.id+"/",
        data,
        {headers: {"Content-Type": "multipart/form-data",}})
      .then(response=>{
        // console.log(response.data)        
      })
    }

    if(password){
      axiosInstance.put("api/v1/users/password/",password).then(response=>{
        console.log(response.data.message)
        tmpResponses.push({"success":true,"message":response.data.message})
      }).catch(err=>{
        console.log(err.response.data.detail)
        tmpResponses.push({"success":false,"message":err.response.data.detail})
        
      })
    }

    axiosInstance.put("api/v1/users/"+profile.id+"/",tempProfile).then(response=>{
      console.log(response.data)
      setUser({...user})
      tmpResponses.push({"success":true,"message":"Profil wurde aktualisiert"})
    })
    setResponses(tmpResponses)
    toggleIsEditing();
  }

  useEffect(()=>{
    console.log('responses', responses)
  },[responses])
  
  const toggleIsEditing = ()=>{
    if(isEditing){
      setIsEditing(false)
      axiosInstance.get("/api/v1/users/"+user.user_id).then(response=>{
        setProfile(response.data)
      })
    }else{
      setIsEditing(true)
    }
  }

  const handleDeleteAccount = () => {
    axiosInstance.delete("/api/v1/users/"+user.user_id).then(response=>{
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
      setUser(null)
      navigate("/login")
    })
  }

  return (
    <div className='profilepage def-page'>
    <Sidebar></Sidebar>
    <div className='content'>
        {responses?<div className='responses'>
          <ul>
            {responses.map((response,index)=>{return <li key={index} className={response.success?"response success":"response fail"}>{response.message}</li>})}
          </ul>
          
        </div>:<></>}
        {profile?
        <>
          <div className='content-title'>Hallo {profile.username.charAt(0).toUpperCase() + profile.username.slice(1)}</div>
          <Card  noOverlay={true}>
          <div className='profile'>
          <div onClick={isEditing?handleImageUpload:()=>{}} className={isEditing?'profile-img-wrapper editing':'profile-img-wrapper'}>
            <img className='profile-img' alt={profile.username + "-profile"} src={uploadedImg?uploadedImg:axiosInstance.defaults.baseURL + profile.img}/>
            <div className='profile-img-upload'><AutorenewIcon></AutorenewIcon></div>
            {isEditing?<input style={{ display: "none" }} ref={imageButton} type="file" accept="image/*" onChange={onImageChange} />:<></>}
          </div>
          

          {isEditing?<div className='settings'>
            <div className='setting'>
              <label>Username:</label>
              <input type="text" name="username" onChange={handleInput} value={profile.username}/>
            </div>
            <div className='setting'>
              <label>Discord-Username:</label>
              <input type="text" name="discord_username" onChange={handleInput} value={profile.discord_username}/>
            </div>
            {/* <div className='setting'>
              <label>Campus-ID:</label>
              <input className='disabled' type="text" name="campus_id" onChange={handleInput} value={profile.campus_id} disabled/>
            </div> */}
            <div className='setting'>
              <label>Email:</label>
              <input className='disabled' type="text" name="email" onChange={handleInput} value={profile.email} disabled/>
            </div>
            <div className='setting'>
              <label>Altes Passwort:</label>
              <input type="password" name="old_password" onChange={handlePassword} placeholder="**********"/>
            </div>
            <div className='setting'>
              <label>Neues Passwort:</label>
              <input type="password" name="new_password" onChange={handlePassword} placeholder="**********"/>
            </div>
            {password?
            <div className='setting'>
            <label>Neues Passwort Bestätigung:</label>
            <input type="password" name="new_password_confirm" onChange={handlePassword} placeholder="**********"/>
          </div>
            :<></>}
            

          </div>
          :
          <div className='settings'>
            <div className='setting'>
              <label>Username:</label>
              <input type="text" name="username" disabled value={profile.username}/>
            </div>
            <div className='setting'>
              <label>Discord-Username:</label>
              <input type="text" name="discord_username" disabled value={profile.discord_username}/>
            </div>
            {/* <div className='setting'>
              <label>Campus-ID:</label>
              <input className='disabled' type="text" name="campus_id" disabled value={profile.campus_id}/>
            </div> */}
            <div className='setting'>
              <label>Email:</label>
              <input className='disabled' type="text" name="email" disabled value={profile.email}/>
            </div>
            <div className='setting'>
              <label>Passwort:</label>
              <input type="password" name="old_password" disabled placeholder="**********"/>
            </div>
            {/* <div className='setting'>
              <label>Neues Passwort:</label>
              <input type="password" name="new_password" disabled placeholder="**********"/>
            </div> */}
            

          </div>
          }
          

          
        </div>
          </Card>

          <Card collapsed={true} title="Einstellungen">
          {isEditing?<div className='settings'>
          <div className='setting'>
              <label>Mich auf der Community-Seite anzeigen</label>
              <input type="checkbox" name="visible_in_community" onChange={handleInput} checked={profile.visible_in_community}/>
            </div>
            <div className='setting'>
              <label>Discord Username auf der Community-Seite anzeigen</label>
              <input type="checkbox" name="show_discord_username" onChange={handleInput} checked={profile.show_discord_username}/>
            </div>
            <div className='setting'>
              <label>Mich von Discord benachrichtigen, wenn ich ein neues Badge erhalte</label>
              <input type="checkbox" name="notify_badge" onChange={handleInput} checked={profile.notify_badge}/>
            </div>
          </div>
          :
          <div className='settings'>
            <div className='setting'>
              <label>Mich auf der Community-Seite anzeigen</label>
              <input type="checkbox" name="visible_in_community" disabled checked={profile.visible_in_community}/>
            </div>
            <div className='setting'>
              <label>Discord Username auf der Community-Seite anzeigen</label>
              <input type="checkbox" name="show_discord_username" disabled checked={profile.show_discord_username}/>
            </div>
            <div className='setting'>
              <label>Mich von Discord benachrichtigen, wenn ich ein neues Badge erhalte</label>
              <input type="checkbox" name="notify_badge" disabled checked={profile.notify_badge}/>
            </div>
          </div>
          }
          </Card>
        
          <div className='button-row'>
            <div className='btn btn-rounded' onClick={toggleIsEditing}>{isEditing?"Abbrechen":"Bearbeiten"}</div>
            {isEditing?<div className='btn btn-rounded' onClick={handleSaveProfile}>Speichern</div>:<></>}
          </div>

          <div className='button-row'>
            
          <div className='btn btn-rounded danger' onClick={handleDeleteAccount}>Konto löschen</div>
          </div>
        
        </>

        :<div>Wird geladen...</div>}
    </div>
</div>
  )
}

export default Profile