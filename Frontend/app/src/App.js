import { useEffect, useState } from 'react';
import ThemeContext from './context/ThemeContext';
import { BrowserRouter, Route,Routes } from 'react-router-dom';
import {Helmet} from "react-helmet";
import './styles/App.scss';
import Home from './pages/Home/Home';
import Community from './pages/Community/Community';
import Admin from './pages/Admin/Admin';
import Settings from './pages/Settings/Settings';
import Profile from './pages/Profile/Profile';

function App() {
  const [theme,setTheme] = useState()
  
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
    <Helmet>
        <title>ArchiBadge</title>
        <meta name="theme-color" content={theme==="light"?"#fff":"#505050"} />
    </Helmet>
    <ThemeContext.Provider value={{theme,toggleTheme}}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/community" element={<Community />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/profile/:userId" element={<Profile />} />
        </Routes>
      </BrowserRouter>
    </ThemeContext.Provider>
</>

  );
}

export default App;
