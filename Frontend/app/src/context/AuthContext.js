import React from "react"

const AuthContext = React.createContext(
    {
        user: {},
        setUser: () => {}
    }
)


export default AuthContext;