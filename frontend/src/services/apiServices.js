import axios from "axios";

const BASE_URL = "https://2ed74eecdcfc.ngrok-free.app/api/";

const api = axios.create({
    baseURL: BASE_URL,
    timeout: 10000,
    headers: { 'Content-Type': 'application/json' }
})

 export const getDestinations  = async()=>{
    try {
        const response = await api.get("destinations/");
        console.log(response.data,"This Is destinations:" );
        return response.data;
    } catch (error) {
        console.error("Error fetching destinations:", error);
        return [];
    }

}
export const getTours = async ()=>{
    try {
        const response = await api.get("tours/")
        console.log(response.data,"This Is tours:" );
        return response.data;
    } catch (error) {
        console.error("Error fetching tours:", error);
        return [];
    }
}
export default api