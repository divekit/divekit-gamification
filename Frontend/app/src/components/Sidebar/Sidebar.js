import React, { useContext, useEffect, useState } from 'react'
import { useNavigate,NavLink } from "react-router-dom";

import AdminPanelSettingsRoundedIcon from '@mui/icons-material/AdminPanelSettingsRounded';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';
import PeopleRoundedIcon from '@mui/icons-material/PeopleRounded';
import HexagonRoundedIcon from '@mui/icons-material/HexagonRounded';
import DarkModeRoundedIcon from '@mui/icons-material/DarkModeRounded';
import LightModeRoundedIcon from '@mui/icons-material/LightModeRounded';
import ViewHeadlineRoundedIcon from '@mui/icons-material/ViewHeadlineRounded';
import ThemeContext from '../../context/ThemeContext';
import profileJson from "./profile.json";
import "./Sidebar.scss"
function Sidebar() {
    
    const {theme,toggleTheme} = useContext(ThemeContext)
    const [sidebarToggle,setSidebarToggle] = useState(true);

    
    let navigate = useNavigate(); 
    return (<>
            <div className={sidebarToggle?"sidebar collapsed":"sidebar"}>
                <div className='sidebar-top'>
                    <div className='sidebar-logo-wrapper'>
                        <div className='logo' onClick={()=>{navigate("/")}}>Archi<span>Badge</span></div>
                        <div className='sidebar-mobile' onClick={()=>{setSidebarToggle(!sidebarToggle)}}><ViewHeadlineRoundedIcon className='mobile-slider-toggler'/></div>
                    </div>

                    <div className='seperator'></div>
                    <div className='menu'>
                        <ul>
                            <li>
                                <NavLink to="/" className={({ isActive }) => isActive ? "selected" : undefined}>
                                    <HexagonRoundedIcon></HexagonRoundedIcon><div className='label'>Badges</div>
                                </NavLink>
                            </li>
                            <li>
                                <NavLink to="/community" className={({ isActive }) => isActive ? "selected" : undefined}>
                                <PeopleRoundedIcon></PeopleRoundedIcon><div className='label'>Community</div>
                                </NavLink>
                            </li>
                            <li>
                                <NavLink to="/settings" className={({ isActive }) => isActive ? "selected" : undefined}>
                                    <SettingsRoundedIcon></SettingsRoundedIcon><div className='label'>Einstellungen</div>
                                </NavLink>
                            </li>
                            {profileJson.isAdmin?<li>
                                <NavLink to="/admin" className={({ isActive }) => isActive ? "selected" : undefined}>
                                <AdminPanelSettingsRoundedIcon></AdminPanelSettingsRoundedIcon><div className='label'>Moderation</div>
                                </NavLink>
                            </li>:<></>}
                            

                        </ul>
                    
                    </div>
                    
                    
                
                </div>
                <div className='sidebar-bottom'>
                    <div className='seperator'></div>
                    <div className='profile'>
                        <div onClick={()=>{navigate("/profile/"+profileJson.id)}} className='profile-button'>{profileJson.username.charAt(0)}</div>
                        <div onClick={()=>{navigate("/profile/"+profileJson.id)}} className='profile-name'>{profileJson.username}</div>
                    </div>
                    <div onClick={()=>{navigate("/logout/")}} className='btn logout-button btn-rounded'>Abmelden</div>
                    {theme==="light"?<DarkModeRoundedIcon className='theme-icon dark' onClick={toggleTheme}></DarkModeRoundedIcon>:<LightModeRoundedIcon className='theme-icon light' onClick={toggleTheme}></LightModeRoundedIcon>}
                    <div className='footer'>© Copyright TH-Köln, 2022</div>
                </div>
            </div>
        
        </>
    )
}

export default Sidebar