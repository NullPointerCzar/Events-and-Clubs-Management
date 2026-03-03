import api from "./axios";

export const getClubs = () => api.get("clubs/");

export const getClub = (id) => api.get(`clubs/${id}/`);

export const createClub = (data) => api.post("clubs/", data);

export const updateClub = (id, data) => api.put(`clubs/${id}/`, data);

export const deleteClub = (id) => api.delete(`clubs/${id}/`);

export const getClubMembers = (id) => api.get(`clubs/${id}/members/`);

export const joinClub = (id) => api.post(`clubs/${id}/join/`);
