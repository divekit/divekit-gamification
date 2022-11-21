import { useEffect, useState } from 'react';
import ThemeContext from './context/ThemeContext';
import AuthContext from "./context/AuthContext";
import { BrowserRouter, Route,Routes, Navigate,useLocation } from 'react-router-dom';
import {Helmet} from "react-helmet";
import './styles/App.scss';
import jwt from 'jwt-decode'
import Home from './pages/Home/Home';
import Community from './pages/Community/Community';
import Admin from './pages/Admin/Admin';
import Settings from './pages/Settings/Settings';
import Profile from './pages/Profile/Profile';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';

function App() {
  const [user, setUser] = useState(localStorage.getItem("access") ? jwt(localStorage.getItem("access")) : null);
  const [theme,setTheme] = useState()
  
  useEffect(()=>{
    // console.log(user)
    if(!user){
      // console.log("LOGGED OUT")
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
    }

  },[user])

  useEffect(() => {
    if(theme){
      document.documentElement.setAttribute("data-theme", theme);
      localStorage.setItem("theme", theme);
    }else{
      let savedTheme = localStorage.getItem("theme")
      if(savedTheme){
        setTheme(savedTheme)
      }else{
        localStorage.setItem("theme", "light");
        setTheme("light")
      }
    }
  }, [theme])
  
  const toggleTheme = () => {
    if(theme === "light"){
        setTheme("dark");
    }
    else{
        setTheme("light");
    }
  }


  return (
<>
<AuthContext.Provider value={{user,setUser}}>
    <Helmet>
        <title>ArchiBadge</title>
        <meta name="theme-color" content={theme==="light"?"#fff":"#505050"} />
    </Helmet>
    <ThemeContext.Provider value={{theme,toggleTheme}}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<ProtectedRoute user={user}><Home/></ProtectedRoute>} />
          <Route path="/community" element={<ProtectedRoute user={user}><Community/></ProtectedRoute>} />
          <Route path="/settings" element={<ProtectedRoute user={user}><Settings/></ProtectedRoute>} />
          <Route path="/admin" element={<ProtectedRoute user={user} isStaff={true}><Admin/></ProtectedRoute>} />
          <Route path="/profile/:userId" element={<ProtectedRoute user={user}><Profile/></ProtectedRoute>} />
          <Route path="/login" element={<ProtectedRoute user={user} redirect="/"><Login/></ProtectedRoute>}></Route>
          <Route path="/register" element={<ProtectedRoute user={user} redirect="/"><Register/></ProtectedRoute>}></Route>
        </Routes>
      </BrowserRouter>
    </ThemeContext.Provider>
    </AuthContext.Provider>
</>

  );
}

function ProtectedRoute({user,redirect,children,isStaff=false}){
  const location = useLocation()

  if(!user){
    console.log('location.pathname', location.pathname)
    if(redirect){
      return children
    }
    return <Navigate to="/login" replace></Navigate>
  }
  else if (user && redirect){
    // if(isStaff && user.){

    // }
    console.log("user",user)
    return <Navigate to={redirect} replace></Navigate>
  }
  else{

  }
  return children;
}


export default App;
