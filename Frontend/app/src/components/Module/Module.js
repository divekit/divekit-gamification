import React from 'react'
import "./Module.scss";

function Module({id,moduleClickHandler,moduleColor,moduleName,moduleAcronym,isActive,isSelected}) {
  return (
    <div onClick={()=>{moduleClickHandler(id)}} title={moduleName} className={isSelected?"module selected":"module"} >
        {moduleAcronym}
    </div>
  )
}

export default Module