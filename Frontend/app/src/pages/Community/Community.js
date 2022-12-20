
import React,{useState,useEffect,useContext} from 'react'
import Sidebar from '../../components/Sidebar/Sidebar'
import "./Community.scss"
import Card from "../../components/Card/Card"
import BadgeSmall from "../../components/BadgeSmall/BadgeSmall"
import AuthContext from '../../context/AuthContext'
import axiosInstance from '../../axios'
import Module from '../../components/Module/Module';

function Community() {
  const [communityUsers,setCommunityUsers] = useState(null)
  const [modules,setModules] = useState(null)
  const [moduleModalToggle,setModuleModalToggle] = useState(false)


  // useEffect(()=>{
  //   if(modules && communityUsers){
  //     let tmpCommunityUsers = communityUsers
  //     tmpCommunityUsers.forEach(communityUser => {
        
  //       communityUser.badges.forEach(userBadge=>{
  //         userBadge.visible = false;
  //         if(modules.find(modEl => modEl.id === userBadge.badge.module && modEl.selected)){
  //           userBadge.visible = true;
  //         }
  //       })
  //     });
  //     setCommunityUsers([...tmpCommunityUsers])
  //   }
  // },[modules])

  useEffect(()=>{
    if(modules){
      let queryStr = ""
      modules.forEach(module => {
        if(module.selected){
          queryStr += `modules[]=${module.id}&`
        }
      });

      axiosInstance.get("/api/v1/users/minified/?"+queryStr).then(response=>{
        console.log(response.data)
        setCommunityUsers(response.data)
      })
    }
  },[modules])


  useEffect(()=>{
    axiosInstance.get("/api/v1/modules").then(response=>{
      response.data.forEach(data => {
        data.selected = data.active;
      });
      setModules(response.data)
    })
  },[])

  const moduleClickHandler = (id) => {
    let modulesTmp = modules
    let foundModule = modulesTmp.find(module => module.id === id)
    if(foundModule){
      foundModule.selected = !foundModule.selected
    }
    console.log(modulesTmp)
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
  
    <div className='communitypage def-page'>
        <Sidebar></Sidebar>
        <div className='content'>
            <div className='content-title'>Community</div>

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

            <Card notCollapsable={true} collapsed={false} noOverlay={true} className="community-card">
            <div className='table-wrapper'>
            {communityUsers?
            <table>
                <thead>
                  <tr>
                    <th>Benutzername</th>
                    <th>Badges</th>
                  </tr>

                </thead>
                <tbody>
                  
                  {communityUsers.map((user,userIndex)=>{
                    return <tr key={userIndex}>
                            <td>{user.username}</td>
                            <td className="user-badges">
                              <div className="small-badges">
                                {user.badges.filter(progressBadge=>progressBadge.earned).map((progressBadge,progressBadgeIndex)=>{

                                  return <BadgeSmall 
                                          key={progressBadgeIndex}
                                          name={progressBadge.name} 
                                          description={progressBadge.badge.description} 
                                          date={progressBadge.earned_at} 
                                          img={progressBadge.badge.img}
                                        ></BadgeSmall>
                                })}
                                {user.badges.length < user.total_badges?<div className='badge-more'>+{user.total_badges - user.badges.length > 99?"99":user.total_badges - user.badges.length}</div>:<></>}
                                
                              </div>
                            </td>
                          </tr>
                  })}
                  
                  
                </tbody>
                <tfoot>
                  <tr>
                    <th>Benutzername</th>
                    <th>Badges</th>
                  </tr>

                </tfoot>
              </table>
              :<div className='page-loader'>Wird geladen...</div>}
            </div>
            </Card>
        </div>
    </div>
    </>)
}

export default Community