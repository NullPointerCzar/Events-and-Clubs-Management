import api from "./axios";

export const getAllUsers = () => api.get("users/");

export const createUser = (data) => api.post("users/", data);

