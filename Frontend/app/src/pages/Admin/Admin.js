import React from 'react'
import Sidebar from '../../components/Sidebar/Sidebar'
import "./Admin.scss"
function Admin() {
  return (
    <div className='adminpage def-page'>
        <Sidebar></Sidebar>
        <div className='content'>
            <div className='content-title'>Admin</div>
            <div className='modal-buttons'>
              <div className='big-button'>Badge erstellen</div>
              <div className='big-button'>Rollen & Zugriffe</div>
              <div className='big-button'>Bot verwalten</div>
              <div className='big-button'>Log </div>
            </div>
        </div>
    </div>
  )
}

export default Admin