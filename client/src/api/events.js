import api from "./axios";

export const getEvents = () => api.get("events/");

export const getEvent = (id) => api.get(`events/${id}/`);

export const createEvent = (data) => api.post("events/", data);

export const updateEvent = (id, data) => api.put(`events/${id}/`, data);

export const deleteEvent = (id) => api.delete(`events/${id}/`);

export const approveEvent = (id, data) =>
  api.post(`events/${id}/approve/`, data);

// ── Event proposal flow ──
export const proposeEvent = (data) => api.post("events/propose/", data);

export const getMyProposedEvents = () => api.get("events/my/");

export const getFacultyProposedEvents = () => api.get("events/review/");

export const reviewEvent = (id, data) =>
  api.post(`events/${id}/review/`, data);

export const getMyClubs = () => api.get("clubs/my/");
