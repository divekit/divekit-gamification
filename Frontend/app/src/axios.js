import axios from 'axios'


const baseURL = 'http://localhost:8000/'

const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 5000,
    headers: {
        'Authorization': localStorage.getItem('access') ? "Bearer " + localStorage.getItem('access') : null,
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
})


axiosInstance.interceptors.response.use(
    response =>  response,
    error => {
        const originalRequest = error.config;
        if(error.response.status === 401){
            
            const refreshToken = localStorage.getItem("refresh");
            if(refreshToken && !originalRequest._retry){
                originalRequest._retry = true
                return new Promise((resolve,reject) => {
                    axiosInstance.post("/api/v1/token/refresh/",{refresh:refreshToken}).then((response)=>{
                        localStorage.setItem("access",response.data.access);
                        localStorage.setItem("refresh",response.data.refresh);
                        axiosInstance.defaults.headers = {...axios.defaults.headers, Authorization: `Bearer ${response.data.access}`}
                        originalRequest.headers = {...originalRequest.headers, Authorization: `Bearer ${response.data.access}`}
                        resolve(axiosInstance(originalRequest))
                        
                    }).catch(err=>{
                        console.log('err', err)
                        reject(err)
                    })
                });
                
            }
        }
        return Promise.reject(error)
        
    }
)



export default axiosInstance;