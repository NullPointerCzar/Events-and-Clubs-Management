import { Outlet, Link, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

const AdminLayout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-indigo-700 text-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-6">
              <Link to="/admin" className="text-xl font-bold">
                ECM Admin
              </Link>
              <Link to="/admin" className="text-indigo-200 hover:text-white">
                Dashboard
              </Link>
              <Link
                to="/admin/users"
                className="text-indigo-200 hover:text-white"
              >
                Users
              </Link>
              <Link
                to="/admin/clubs"
                className="text-indigo-200 hover:text-white"
              >
                Clubs
              </Link>
              <Link
                to="/admin/events"
                className="text-indigo-200 hover:text-white"
              >
                Events
              </Link>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-indigo-200">
                {user?.name} (Admin)
              </span>
              <button
                onClick={handleLogout}
                className="px-3 py-1.5 text-sm bg-indigo-800 text-white rounded-md hover:bg-indigo-900 transition cursor-pointer"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
};

export default AdminLayout;
