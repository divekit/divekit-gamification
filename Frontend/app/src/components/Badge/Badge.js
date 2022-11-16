import React from 'react'
import "./Badge.scss"
function Badge({name,description,total,current,badgeImg,earned}) {
  return (
    <div title={description} className={earned?"badge earned":"badge"}>
        <div className='badge-img'><img src={badgeImg} alt={name + " Bild"}></img></div>
        <div className='badge-name'>{name}</div>
        <div className='badge-progress-wrapper'>
            <div className='badge-progress-counter'>{total?(current+"/"+total):earned?"1/1":"0/1"}</div>
            {
            total?
                <div className='badge-progress-inner' style={{width:(100*current/total)+"%"}}></div>
                :
                earned?
                    <div className='badge-progress-inner' style={{width:"100%"}}></div>
                    :
                    <div className='badge-progress-inner' style={{width:"0%"}}></div>
            }
            
        </div>
        
    </div>
  )
}

export default Badge