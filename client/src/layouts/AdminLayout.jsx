import { useState } from "react";
import { Outlet, Link, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

const AdminLayout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isUsersMenuOpen, setIsUsersMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-indigo-700 text-white shadow-md relative z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-6">
              <Link to="/admin" className="text-xl font-bold">
                ECM Admin
              </Link>
              <Link to="/admin" className="text-indigo-200 hover:text-white">
                Dashboard
              </Link>
              
              {/* Users Dropdown */}
              <div 
                className="relative"
                onMouseEnter={() => setIsUsersMenuOpen(true)}
                onMouseLeave={() => setIsUsersMenuOpen(false)}
              >
                <button 
                  className="text-indigo-200 hover:text-white flex items-center gap-1 focus:outline-none py-4"
                >
                  Users
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                
                {isUsersMenuOpen && (
                  <div className="absolute top-14 left-0 w-48 bg-white rounded-md shadow-lg py-1 border border-indigo-100 animate-fadeIn">
                    <Link
                      to="/admin/users" 
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700"
                    >
                      All Users
                    </Link>
                    <Link
                      to="/admin/users?type=Student"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700"
                    >
                      Students
                    </Link>
                    <Link
                      to="/admin/users?type=Faculty"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700"
                    >
                      Faculty
                    </Link>
                    <Link
                      to="/admin/users?type=Staff"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700"
                    >
                      Staff
                    </Link>
                    <Link
                      to="/admin/users?type=Admin"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-700"
                    >
                      Admins
                    </Link>
                  </div>
                )}
              </div>

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
