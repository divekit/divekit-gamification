import React,{useContext} from 'react'
import Sidebar from '../../components/Sidebar/Sidebar'
import "./Profile.scss"
import {useParams} from "react-router-dom";
import AuthContext from '../../context/AuthContext';

function Profile() {
  const { user, setUser } = useContext(AuthContext)
  let { userId } = useParams();


  return (
    <div className='profilepage def-page'>
    <Sidebar></Sidebar>
    <div className='content'>
        <div className='content-title'>Hallo {user.username.charAt(0).toUpperCase() + user.username.slice(1)}</div>
        
    </div>
</div>
  )
}

export default Profile