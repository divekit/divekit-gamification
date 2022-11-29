
import React,{useState,useEffect,useContext} from 'react'
import Sidebar from '../../components/Sidebar/Sidebar'
import "./Community.scss"
import Card from "../../components/Card/Card"
import BadgeSmall from "../../components/BadgeSmall/BadgeSmall"
import AuthContext from '../../context/AuthContext'
import axiosInstance from '../../axios'


function Community() {
  const { user, setUser } = useContext(AuthContext)
  const [communityUsers,setCommunityUsers] = useState(null)

  useEffect(()=>{
    axiosInstance.get("/api/v1/users/minified/").then(response=>{
      console.log(response.data)
      setCommunityUsers(response.data)
    })
  },[])

  useEffect(()=>{
    console.log()

  },[communityUsers])

  return (
    <div className='communitypage def-page'>
        <Sidebar></Sidebar>
        <div className='content'>
            <div className='content-title'>Community</div>
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
  )
}

export default Community