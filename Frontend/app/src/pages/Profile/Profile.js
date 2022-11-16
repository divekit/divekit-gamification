import React from 'react'
import Sidebar from '../../components/Sidebar/Sidebar'
import "./Profile.scss"
import {useParams} from "react-router-dom";

function Profile() {
  let { userId } = useParams();

  return (
    <div className='profilepage def-page'>
    <Sidebar></Sidebar>
    <div className='content'>
        <div className='content-title'>Hallo {userId}</div>
        
    </div>
</div>
  )
}

export default Profile