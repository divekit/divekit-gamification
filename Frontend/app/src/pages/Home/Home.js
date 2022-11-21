import React, { useEffect,useState,useContext } from 'react'

import Sidebar from '../../components/Sidebar/Sidebar';


import "./Home.scss"

import Card from '../../components/Card/Card';
import Badge from '../../components/Badge/Badge';
import axiosInstance from '../../axios';
import AuthContext from '../../context/AuthContext';
function Home() {

  const { user, setUser } = useContext(AuthContext)
  const [totalBadges,setTotalBadges] = useState(null)
  const [myProfile,setMyProfile] = useState(null)
  const [earnedBadges,setEarnedBadges] = useState(null)
  const [progressedBadges, setProgressedBadges] = useState(null)
  const [availableBadges,setAvailableBadges] = useState(null)
  const [miscBadges,setMiscBadges] = useState(null)

  useEffect(()=>{
    if(user){
      axiosInstance.get("/api/v1/badges/").then(response=>{
        setTotalBadges(response.data)
      })
      axiosInstance.get("/api/v1/users/"+user.user_id).then(response=>{
        setMyProfile(response.data)
      })
    }

  },[user])

  useEffect(()=>{
    if(myProfile && totalBadges){

      console.log(myProfile)
      console.log(totalBadges)

      let progressedBadgesTmp = myProfile.badges.filter(progressBadge=>{
        return progressBadge.earned===false;
      })
      setProgressedBadges(progressedBadgesTmp)
      
      let earnedBadgesTmp = myProfile.badges.filter(progressBadge=>{
        return progressBadge.earned===true;
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
          return true
        }
        return false
      }))

      setMiscBadges(totalBadges.filter(badge=>{
        return badge.is_unique===false;
      }))

    }
  },[myProfile,totalBadges])


  useEffect(()=>{
    console.log("M",availableBadges)
  },[availableBadges])
  return (<>
  <div className='homepage def-page'>
        <Sidebar></Sidebar>
        <div className='content'>
          <div className='content-title'>
            Badges
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
              // console.log("")
              <div className='badges'>

                {availableBadges.map((badge,index)=>{
                  
                  return <Badge 
                          description={badge.description} 
                          key={index} 
                          name={badge.name}
                          total={badge.milestones} 
                          current={0} 
                          badgeImg={axiosInstance.defaults.baseURL + badge.img}
                          ></Badge>
                })}
              </div>
              :"Kein Badge gefunden"}
            </Card>
            <Card collapsed={false} title={"Misc"} count={miscBadges?miscBadges.length:"0"}>
            {miscBadges?
              // console.log("")
              <div className='badges'>

                {miscBadges.map((badge,index)=>{
                  
                  return <Badge 
                          description={badge.description}
                          key={index} 
                          name={badge.name}
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