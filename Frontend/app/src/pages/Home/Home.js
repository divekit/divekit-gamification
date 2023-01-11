import React, { useEffect,useState,useContext } from 'react'

import Sidebar from '../../components/Sidebar/Sidebar';


import "./Home.scss"

import Card from '../../components/Card/Card';
import Badge from '../../components/Badge/Badge';
import axiosInstance from '../../axios';
import AuthContext from '../../context/AuthContext';
import Module from '../../components/Module/Module';
function Home() {

  const { user, setUser } = useContext(AuthContext)
  const [totalBadges,setTotalBadges] = useState(null)
  const [myBadges,setMyBadges] = useState(null)
  const [earnedBadges,setEarnedBadges] = useState(null)
  const [modules,setModules] = useState(null)
  const [progressedBadges, setProgressedBadges] = useState(null)
  const [availableBadges,setAvailableBadges] = useState(null)
  const [miscBadges,setMiscBadges] = useState(null)

  const [moduleModalToggle,setModuleModalToggle] = useState(false)
  useEffect(()=>{
    if(user){
      axiosInstance.get("/api/v1/badges/").then(response=>{
        setTotalBadges(response.data)
      })
      axiosInstance.get("/api/v1/users/"+user.user_id+"/badges/").then(response=>{
        setMyBadges(response.data)
      })
      axiosInstance.get("/api/v1/modules").then(response=>{
        response.data.forEach(data => {
          data.selected = data.active;
        });
        setModules(response.data)
      })
    }

  },[user])

  useEffect(()=>{
    if(myBadges && totalBadges && modules){

      let progressedBadgesTmp = myBadges.filter(progressBadge=>{
        return progressBadge.earned===false && modules.find(modEl => modEl.id === progressBadge.badge.module && modEl.selected);
      })
      setProgressedBadges(progressedBadgesTmp)
      
      let earnedBadgesTmp = myBadges.filter(progressBadge=>{
        return progressBadge.earned===true && modules.find(modEl => modEl.id === progressBadge.badge.module && modEl.selected);
      })
      setEarnedBadges(earnedBadgesTmp)
      
      setAvailableBadges(totalBadges.filter(badge=>{
        if(badge.is_unique){
          let found = false;
          progressedBadgesTmp.forEach(element => {
            if(element.badge.id === badge.id){
              found = true;
            }
          });
          if(found){
            return false;
          }
          earnedBadgesTmp.forEach(element=>{
            if(element.badge.id === badge.id){
              found = true;
            }
          });
          if(found){
            return false;
          }
          if(!modules.find(modEl => modEl.id === badge.module && modEl.selected)){
            return false;
          }
          return true;
        }
        return false;
      }))

      setMiscBadges(totalBadges.filter(badge=>{
        return badge.is_unique===false && modules.find(modEl => modEl.id === badge.module && modEl.selected);
      }))

    }
  },[modules,myBadges,totalBadges],[modules])

  const moduleClickHandler = (id) => {
    let modulesTmp = modules
    let foundModule = modulesTmp.find(module => module.id === id)
    if(foundModule){
      foundModule.selected = !foundModule.selected
    }
    setModules([...modulesTmp])
  }

  return (<>
  {moduleModalToggle?<div className='modal' id="module-modal" onClick={()=>{setModuleModalToggle(false)}}>
    <div className='modal-box' onClick={(e)=>{e.stopPropagation()}}>
      <div className='modal-header'>
        <div className='modal-title'>Sonstige</div>
        <div className='modal-close btn btn-rounded' onClick={()=>{setModuleModalToggle(false)}}>X</div>
        
      </div>
      <div className='modal-content'>
        {modules.map((modEl,index)=>{
                  if(!modEl.active && !modEl.selected){
                    return <Module id={modEl.id} key={index} moduleClickHandler={moduleClickHandler} moduleName={modEl.name} moduleAcronym={modEl.acronym} isSelected={modEl.selected}></Module>
                  }
                  return null
                })
              }
      </div>
    </div>
    </div>:<></>
  }
  <div className='homepage def-page'>
        <Sidebar></Sidebar>
        <div className='content'>
          <div className='content-title'>
            Badges
          </div>



          {modules?
            <div className='modules'>
              {modules.map((modEl,index)=>{
                  if(modEl.active){
                    return <Module id={modEl.id} key={index} moduleClickHandler={moduleClickHandler} moduleName={modEl.name} moduleAcronym={modEl.acronym} isSelected={modEl.selected}></Module>
                  }
                  return null
                  
                })
              }
              {modules.map((modEl,index)=>{
                  if(!modEl.active && modEl.selected){
                    return <Module id={modEl.id} key={index} moduleClickHandler={moduleClickHandler} moduleName={modEl.name} moduleAcronym={modEl.acronym} isSelected={modEl.selected}></Module>
                  }
                  return null
                  
                })
              }
              <div className='module modules-modal-toggler' onClick={()=>{setModuleModalToggle(true)}}>Sonstige</div>
            </div>
            :
            <div className='modules modules-loading'>
              <div className='module-loading'></div>
              <div className='module-loading'></div>
              <div className='module-loading'></div>
              <div className='module-loading'></div>
              <div className='module-loading'></div>
            </div>
          }
          <div >

          </div>
          

          <div className='cards'>
            
            <Card collapsed={false} title={"Erworben"} count={earnedBadges?earnedBadges.length:"0"}>
            {earnedBadges?
              
              <div className='badges'>
                {earnedBadges.map((badge,index)=>{
                  
                  return <Badge 
                          description={badge.badge.description} 
                          key={index} 
                          name={badge.badge.name}
                          total={badge.badge.milestones} 
                          current={badge.progress}
                          progress={true}
                          badgeImg={axiosInstance.defaults.baseURL + badge.badge.img}
                          ></Badge>
                })}
              </div>
              :"Kein Badge gefunden"}
              
            </Card>
            <Card collapsed={false} title={"Vorangegangen"} count={progressedBadges?progressedBadges.length:"0"}>
              {progressedBadges?
              <div className='badges'>

                {progressedBadges.map((badge,index)=>{
                  
                  return <Badge 
                          description={badge.badge.description} 
                          key={index} 
                          name={badge.badge.name}
                          total={badge.badge.milestones} 
                          current={badge.progress} 
                          progress={true}
                          badgeImg={axiosInstance.defaults.baseURL + badge.badge.img}
                          ></Badge>
                })}
              </div>
              :"Kein Badge gefunden"}
              
            </Card>
            <Card collapsed={false} title={"Erhältlich"} count={availableBadges?availableBadges.length:"0"}>
            {availableBadges?
              <div className='badges'>

                {availableBadges.map((badge,index)=>{
                  
                  return <Badge 
                          description={badge.description} 
                          key={index} 
                          name={badge.name}
                          total={badge.milestones} 
                          current={0} 
                          hidden={badge.is_hidden}
                          badgeImg={axiosInstance.defaults.baseURL + badge.img}
                          ></Badge>
                })}
              </div>
              :"Kein Badge gefunden"}
            </Card>
            <Card collapsed={true} title={"Misc"} count={miscBadges?miscBadges.length:"0"}>
            {miscBadges?
              <div className='badges'>

                {miscBadges.map((badge,index)=>{
                  
                  return <Badge 
                          description={badge.description}
                          key={index} 
                          name={badge.name}
                          hidden={badge.is_hidden}
                          // total={badge.milestones} 
                          // current={0} 
                          badgeImg={axiosInstance.defaults.baseURL + badge.img}
                          ></Badge>
                })}
              </div>
              :"Kein Badge gefunden"}
            </Card>
          </div>
        </div>
    </div>
  </>
    
  )
}

export default Home