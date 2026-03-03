import { Routes, Route, Navigate } from "react-router-dom";
import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";
import Unauthorized from "../pages/Unauthorized";
import ProtectedRoute from "./ProtectedRoute";
import MainLayout from "../layouts/MainLayout";
import AdminLayout from "../layouts/AdminLayout";

// Placeholder page components — replace with real pages as you build them
const AdminDashboard = () => (
  <h1 className="text-2xl font-bold">Admin Dashboard</h1>
);
const AdminUsers = () => (
  <h1 className="text-2xl font-bold">Manage Users</h1>
);
const AdminClubs = () => (
  <h1 className="text-2xl font-bold">Manage Clubs</h1>
);
const AdminEvents = () => (
  <h1 className="text-2xl font-bold">Manage Events</h1>
);
const StudentHome = () => (
  <h1 className="text-2xl font-bold">Dashboard — Events & Clubs</h1>
);
const FacultyPortal = () => (
  <h1 className="text-2xl font-bold">Faculty Portal — Approvals</h1>
);

const AppRoutes = () => {
  return (
    <Routes>
      {/* ── Public routes ── */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/unauthorized" element={<Unauthorized />} />

      {/* ── Admin routes (with AdminLayout) ── */}
      <Route
        element={
          <ProtectedRoute allowedRoles={["Admin"]}>
            <AdminLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/users" element={<AdminUsers />} />
        <Route path="/admin/clubs" element={<AdminClubs />} />
        <Route path="/admin/events" element={<AdminEvents />} />
      </Route>

      {/* ── Main app routes (with MainLayout) ── */}
      <Route
        element={
          <ProtectedRoute allowedRoles={["Student", "Faculty", "Admin"]}>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<StudentHome />} />
        <Route
          path="/faculty"
          element={
            <ProtectedRoute allowedRoles={["Faculty", "Admin"]}>
              <FacultyPortal />
            </ProtectedRoute>
          }
        />
      </Route>

      {/* ── Redirects ── */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
};

export default AppRoutes;
