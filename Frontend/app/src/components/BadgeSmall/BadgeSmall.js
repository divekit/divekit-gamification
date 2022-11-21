import React from 'react'
import axiosInstance from '../../axios'
import "./BadgeSmall.scss"
function BadgeSmall({name,description,date,img}) {
  
  const showModal = () => {
    console.log("SHOWING MODAL")
  }

  return (
    <div className='badge-small' title={description} onClick={showModal}>
        <img className='badge-small-img' alt={name} src={axiosInstance.defaults.baseURL + img}></img>
    </div>
  )
}

export default BadgeSmall