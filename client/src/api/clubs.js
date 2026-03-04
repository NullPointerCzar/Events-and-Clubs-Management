import api from "./axios";

export const getClubs = () => api.get("clubs/");

export const getClubMembers = (id) => api.get(`clubs/${id}/members/`);
