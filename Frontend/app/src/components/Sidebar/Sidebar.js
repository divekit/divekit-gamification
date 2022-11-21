import React, { useContext, useEffect, useState } from 'react'
import { useNavigate,NavLink } from "react-router-dom";
import axiosInstance from '../../axios';
import AuthContext from '../../context/AuthContext';
import AdminPanelSettingsRoundedIcon from '@mui/icons-material/AdminPanelSettingsRounded';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';
import PeopleRoundedIcon from '@mui/icons-material/PeopleRounded';
import HexagonRoundedIcon from '@mui/icons-material/HexagonRounded';
import DarkModeRoundedIcon from '@mui/icons-material/DarkModeRounded';
import LightModeRoundedIcon from '@mui/icons-material/LightModeRounded';
import ViewHeadlineRoundedIcon from '@mui/icons-material/ViewHeadlineRounded';
import ThemeContext from '../../context/ThemeContext';

import "./Sidebar.scss"
function Sidebar() {
    const { user, setUser } = useContext(AuthContext)
    const {theme,toggleTheme} = useContext(ThemeContext)
    const [sidebarToggle,setSidebarToggle] = useState(true);
    const [profileImageHigherWidth,setProfileImageHigherWidth] = useState(false);
    // const [profileImg,setProfileImg] = useState("http://127.0.0.1:8000/"+user.img);


    useEffect(()=>{
        console.log(user)
        let img = new Image();
        img.src = axiosInstance.defaults.baseURL+user.img;
        img.onload = () => {
            // console.log(img.height);
            // console.log(img.width);
            if(img.height > img.width){
                setProfileImageHigherWidth(true)
            }
            else{
                setProfileImageHigherWidth(false)
            }

        }
    },[user])


    const handleLogout = () =>{
        console.log("LOGOUT CLICKED")
        setUser(null)
    }
    
    let navigate = useNavigate(); 
    return (<>
            <div className={sidebarToggle?"sidebar collapsed":"sidebar"}>
                <div className='sidebar-top'>
                    <div className='sidebar-logo-wrapper'>
                        <div className='logo' onClick={()=>{navigate("/")}}>Divekit<span>Badge</span></div>
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
                            {user.is_staff?<li>
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
                        <div onClick={()=>{navigate("/profile/"+user.user_id)}} className='profile-button'><div className="profile-letter">{user.username.charAt(0).toUpperCase()}</div><img className={profileImageHigherWidth?'profile-img higher-width':'profile-img'} alt="Profil Bild" src={axiosInstance.defaults.baseURL+user.img}/></div>
                        {/* <div onClick={()=>{navigate("/profile/"+user.user_id)}} className='profile-button'><div className="profile-letter">{user.username.charAt(0).toUpperCase()}</div><img className='profile-img' src={"https://images.pexels.com/photos/5800782/pexels-photo-5800782.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"}/></div> */}
                        <div onClick={()=>{navigate("/profile/"+user.user_id)}} className='profile-name'>{user.username.charAt(0).toUpperCase() + user.username.slice(1)}</div>
                    </div>
                    <div onClick={handleLogout} className='btn logout-button btn-rounded'>Abmelden</div>
                    {theme==="light"?<DarkModeRoundedIcon className='theme-icon dark' onClick={toggleTheme}></DarkModeRoundedIcon>:<LightModeRoundedIcon className='theme-icon light' onClick={toggleTheme}></LightModeRoundedIcon>}
                    <div className='footer'>© Copyright TH-Köln, 2022</div>
                </div>
            </div>
        
        </>
    )
}

export default Sidebar