import React from 'react'
import Sidebar from '../../components/Sidebar/Sidebar'
import "./Settings.scss"
import Card from "../../components/Card/Card"
function Settings() {
  return (
    <div className='settingspage def-page'>
        <Sidebar></Sidebar>
        
        <div className='content'>
            <div className='content-title'>Settings</div>
            
            <div className='settings'>
            <Card title="Generelle Einstellungen">
              <ul>
                <li><div className='input-wrapper'>
                  <label htmlFor='discord-notify'>Mich von Discord benachrichtigen 
                  vor <select>
                    <option>3 Stunden</option>
                    <option>6 Stunden</option>
                    <option>12 Stunden</option>
                    <option>1 Tag</option>
                    <option>2 Tage</option>
                    <option>3 Tage</option>
                    <option>5 Tage</option>
                    <option>1 Woche</option>
                    <option>2 Wochen</option>
                  </select> von dem Ablaufdatum
                  </label>
                </div></li>
              </ul>
            
            </Card>
                
            </div>
        </div>
    </div>
  )
}

export default Settings