import axios from "axios";

// Create an Axios instance with default settings
const api = axios.create({
    baseURL: "http://localhost:8000/api/",
    headers: {
        "Content-Type": "application/json",
    },
});

export default api;