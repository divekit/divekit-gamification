import React, { useState } from 'react'

import "./Card.scss"
import AddRoundedIcon from '@mui/icons-material/AddRounded';
import RemoveRoundedIcon from '@mui/icons-material/RemoveRounded';
function Card({children,collapsed,title,count,noOverlay,notCollapsable,className}) {

  const [cardCollapsed,setCardCollapsed] = useState(collapsed)



  return (
    <div className={cardCollapsed?`card collapsed ${className}`:`card ${className}`}>
            {noOverlay?<></>:<><div className='card-top'>
              <div className='card-title-wrapper'>
              <div className='card-title'>{title}</div>
              <div className='card-count'>{count}</div>
              </div>
              {notCollapsable?<></>:<div className='card-collapse-button'>
                {cardCollapsed?<AddRoundedIcon onClick={()=>{setCardCollapsed(false)}} className='extend-icon'></AddRoundedIcon>:<RemoveRoundedIcon onClick={()=>{setCardCollapsed(true)}} className='collapse-icon'></RemoveRoundedIcon>}
              </div>}
            </div>
            <div className='seperator card-seperator'></div></>}
            <div className='card-content'>
              {children}
            </div>
      </div>
  )
}

export default Card