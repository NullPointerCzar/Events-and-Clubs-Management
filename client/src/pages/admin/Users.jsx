import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { getAllUsers } from "../../api/users"; // You'll need to create this export in api/users.js

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const location = useLocation();

  useEffect(() => {
    fetchUsers();
  }, [location.search]); // Re-fetch or re-filter when URL params change

  const fetchUsers = async () => {
    try {
      const response = await getAllUsers();
      setUsers(response.data);
    } catch (err) {
      console.error("Failed to fetch users:", err);
      setError("Failed to load users. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 p-4 rounded-md text-red-600 text-center">
        {error}
      </div>
    );
  }

  // Get filter from URL
  const queryParams = new URL(window.location.href).searchParams;
  const filterType = queryParams.get("type");

  // Create groups for each user type
  const allGroups = {
      Students: users.filter(u => u.user_type === 'Student'),
      Faculty: users.filter(u => u.user_type === 'Faculty'),
      Staff: users.filter(u => u.user_type === 'Staff'),
      Admins: users.filter(u => u.user_type === 'Admin'),
  };

  // Determine which groups to show
  let userGroups = allGroups;
  if (filterType === 'Student') userGroups = { Students: allGroups.Students };
  else if (filterType === 'Faculty') userGroups = { Faculty: allGroups.Faculty };
  else if (filterType === 'Staff') userGroups = { Staff: allGroups.Staff };
  else if (filterType === 'Admin') userGroups = { Admins: allGroups.Admins };

  return (
    <div className="space-y-8 p-4">
      <div className="flex justify-between items-center border-b pb-4">
        <h1 className="text-2xl font-bold text-gray-800">
           {filterType ? `${filterType} Management` : "User Management"}
        </h1>
        <Link
          to="/admin/users/create"
          className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition shadow-sm text-sm"
        >
          Add New User
        </Link>
      </div>

      {Object.entries(userGroups).map(([groupName, groupUsers]) => (
        <div key={groupName} className="mb-8">
            <h2 className="text-xl font-semibold mb-4 text-gray-700 border-l-4 border-indigo-500 pl-2">
                {groupName} <span className="text-sm font-normal text-gray-500">({groupUsers.length})</span>
            </h2>
            
            {groupUsers.length > 0 ? (
                <div className="overflow-x-auto border border-gray-200">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                        <tr>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r">
                                Name
                            </th>
                            {groupName === 'Students' && (
                              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r">
                                  Roll Number
                              </th>
                            )}
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-r">
                                Email
                            </th>
                            <th scope="col" className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider border-r">
                                Status
                            </th>
                            <th scope="col" className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                        {groupUsers.map((user) => (
                            <tr key={user.id} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 border-r">
                                    {user.full_name}
                                </td>
                                {groupName === 'Students' && (
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 border-r font-mono">
                                      {user.role_number || user.roll_number || "-"}
                                  </td>
                                )}
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 border-r">
                                    {user.email}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-center border-r">
                                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                    user.is_active ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                                    }`}>
                                    {user.is_active ? "Active" : "Inactive"}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                                    <button className="text-indigo-600 hover:text-indigo-900 mr-4">Edit</button>
                                    <button className="text-red-600 hover:text-red-900">Delete</button>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                <p className="text-gray-500 italic text-sm">No {groupName.toLowerCase()} found.</p>
            )}
        </div>
      ))}
    </div>
  );
};

export default Users;
