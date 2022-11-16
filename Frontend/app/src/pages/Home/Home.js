import React, { useEffect } from 'react'

import Sidebar from '../../components/Sidebar/Sidebar';


import "./Home.scss"
import dummy from "./dummy.json";
import Card from '../../components/Card/Card';
import Badge from '../../components/Badge/Badge';
function Home() {

  useEffect(()=>{
    console.log(dummy)
  },[])
  return (<>
  <div className='homepage def-page'>
        <Sidebar></Sidebar>
        <div className='content'>
          <div className='content-title'>
            Badges
          </div>
          <div className='cards'>
            
            <Card collapsed={false} title={"Erworben"} count={4}>
              <div className='badges'>
                <Badge name="Hurra!" 
                total={5} 
                current={5}
                description="Du hast alle Aufgaben von Meilenstein 1 erfolgreich bestanden."
                earned={true}
                // badgeImg="https://www.w3schools.com/images/img_mylearning_120.png"
                badgeImg="https://www.gravatar.com/avatar/7e721e8fb7dc69b5068dc98f2daf74bc?s=64&d=identicon&r=PG&f=1"
                ></Badge>
                <Badge name="Hurra!" 
                // total={5} 
                earned={true}
                // current={3} 
                // badgeImg="https://www.w3schools.com/images/img_mylearning_120.png"
                badgeImg="https://www.gravatar.com/avatar/7e721e8fb7dc69b5068dc98f2daf74bc?s=64&d=identicon&r=PG&f=1"
                ></Badge>
                
              </div>
              
            </Card>
            <Card collapsed={false} title={"Gesperrt"} count={32}>
              <div className='badges'>
              <Badge name="Hurra!" 
                // total={5} 
                // current={3} 
                // badgeImg="https://www.w3schools.com/images/img_mylearning_120.png"
                badgeImg="https://www.gravatar.com/avatar/7e721e8fb7dc69b5068dc98f2daf74bc?s=64&d=identicon&r=PG&f=1"
                ></Badge>
                <Badge name="Hurra!" 
                total={5} 
                current={3} 
                // badgeImg="https://www.w3schools.com/images/img_mylearning_120.png"
                badgeImg="https://www.gravatar.com/avatar/7e721e8fb7dc69b5068dc98f2daf74bc?s=64&d=identicon&r=PG&f=1"
                ></Badge>
                <Badge name="Hurra!" 
                total={5} 
                current={3} 
                // badgeImg="https://www.w3schools.com/images/img_mylearning_120.png"
                badgeImg="https://www.gravatar.com/avatar/7e721e8fb7dc69b5068dc98f2daf74bc?s=64&d=identicon&r=PG&f=1"
                ></Badge>
                <Badge name="Hurra!" 
                total={5} 
                current={3} 
                // badgeImg="https://www.w3schools.com/images/img_mylearning_120.png"
                badgeImg="https://www.gravatar.com/avatar/7e721e8fb7dc69b5068dc98f2daf74bc?s=64&d=identicon&r=PG&f=1"
                ></Badge>
                <Badge name="Hurra!" 
                total={5} 
                current={3} 
                // badgeImg="https://www.w3schools.com/images/img_mylearning_120.png"
                badgeImg="https://www.gravatar.com/avatar/7e721e8fb7dc69b5068dc98f2daf74bc?s=64&d=identicon&r=PG&f=1"
                ></Badge>
              </div>
            </Card>
            <Card collapsed={true} title={"Misc"} count={144}></Card>
          </div>
        </div>
    </div>
  </>
    
  )
}

export default Home