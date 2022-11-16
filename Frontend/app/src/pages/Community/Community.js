
import React from 'react'
import Sidebar from '../../components/Sidebar/Sidebar'
import "./Community.scss"
import Card from "../../components/Card/Card"
import communityJson from "./community.json"
import BadgeSmall from "../../components/BadgeSmall/BadgeSmall"


function Community() {
 
  return (
    <div className='communitypage def-page'>
        <Sidebar></Sidebar>
        <div className='content'>
            <div className='content-title'>Community</div>
            <Card notCollapsable={true} collapsed={false} noOverlay={true} className="community-card">
            <div className='table-wrapper'>
              
            <table>
                <thead>
                  <tr>
                    <th>Benutzername</th>
                    <th>Badges</th>
                    <th>Kontakt</th>
                  </tr>

                </thead>
                <tbody>
                  {communityJson.users.map((user,userKey)=>{
                    return <tr>
                    <td>{user.username}</td>
                    <td className="user-badges">
                      <div className="small-badges">
                        {user.badges.map((badge,badgeKey)=>{
                          return <BadgeSmall name={badge.name} description={badge.description} date={badge.date} img={badge.img}></BadgeSmall>
                        })}
                        
                      </div>
                    </td>
                    <td>zhk</td>
                  </tr>
                  })}
                  
                </tbody>
                <tfoot>
                  <tr>
                    <th>Benutzername</th>
                    <th>Badges</th>
                    <th>Kontakt</th>
                  </tr>

                </tfoot>
              </table>
            </div>
            </Card>
        </div>
    </div>
  )
}

export default Community