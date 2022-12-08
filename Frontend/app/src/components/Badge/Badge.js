import React from 'react'
import axiosInstance from '../../axios'
import "./Badge.scss"
import QuestionMarkIcon from '@mui/icons-material/QuestionMark';
function Badge({name,description,total,current,badgeImg,progress,hidden}) {
  return (
    <div className={progress?"badge earned":"badge"}>
      {hidden?<>
        <div className='badge-img'><div className='hidden-badge'><QuestionMarkIcon></QuestionMarkIcon></div></div>
        <div className='badge-name'>???</div>
        <div className='badge-progress-wrapper'>
            <div className='badge-progress-counter'>?</div>
            <div className='badge-progress-inner' style={{width:"0%"}}></div>            
        </div>
        </>:<>
        <div className='badge-img' title={description}><img src={badgeImg} alt={name + " Bild"}></img></div>
        <div className='badge-name' title={name}>{name}</div>
        <div className='badge-progress-wrapper'>
            <div className='badge-progress-counter'>{total?(current+"/"+total):"99+"}</div>
            {
            total?
                <div className='badge-progress-inner' style={{width:(100*current/total)+"%"}}></div>
                :
                progress?
                    <div className='badge-progress-inner' style={{width:"100%"}}></div>
                    :
                    <div className='badge-progress-inner' style={{width:"0%"}}></div>
            }
        </div></>}
        
        
    </div>
  )
}

export default Badge