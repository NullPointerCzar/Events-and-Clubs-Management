import { useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { getClubs, getClubMembers } from "../../api/clubs";

const REQUIRED_CLUBS = [
  "NCE IT Club",
  "NCE Robotics Club",
  "CESS",
  "Electrical Club",
];

const Clubs = () => {
  const [clubs, setClubs] = useState([]);
  const [members, setMembers] = useState([]);
  const [selectedClubId, setSelectedClubId] = useState("");
  const [membersLoading, setMembersLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const location = useLocation();

  useEffect(() => {
    const fetchClubs = async () => {
      setLoading(true);
      setError("");
      try {
        const response = await getClubs();
        const filtered = response.data.filter((club) => REQUIRED_CLUBS.includes(club.club_name));
        setClubs(filtered);

        const queryParams = new URLSearchParams(location.search);
        const selectedName = queryParams.get("name");
        if (selectedName) {
          const matchedClub = filtered.find((club) => club.club_name === selectedName);
          if (matchedClub) setSelectedClubId(String(matchedClub.id));
        }
      } catch (err) {
        setError("Failed to load clubs.");
      } finally {
        setLoading(false);
      }
    };

    fetchClubs();
  }, [location.search]);

  useEffect(() => {
    const fetchMembers = async () => {
      if (!selectedClubId) {
        setMembers([]);
        return;
      }

      setMembersLoading(true);
      try {
        const response = await getClubMembers(selectedClubId);
        setMembers(response.data);
      } catch (err) {
        setError("Failed to load club members.");
      } finally {
        setMembersLoading(false);
      }
    };

    fetchMembers();
  }, [selectedClubId]);

  const selectedClub = useMemo(() => {
    return clubs.find((club) => String(club.id) === String(selectedClubId)) || null;
  }, [clubs, selectedClubId]);

  if (loading) return <div className="p-4">Loading clubs...</div>;
  if (error) return <div className="p-4 text-red-600">{error}</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Club Management</h1>

      <div className="bg-white border border-gray-200 p-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">Select Club</label>
        <select
          value={selectedClubId}
          onChange={(e) => setSelectedClubId(e.target.value)}
          className="w-full md:w-96 border border-gray-300 px-3 py-2"
        >
          <option value="">-- Choose a club --</option>
          {clubs.map((club) => (
            <option key={club.id} value={club.id}>
              {club.club_name}
            </option>
          ))}
        </select>
      </div>

      <div className="overflow-x-auto border border-gray-200 bg-white">
        <div className="px-4 py-3 border-b bg-gray-50 font-semibold text-gray-700">
          {selectedClub ? `${selectedClub.club_name} Members` : "Club Members"}
        </div>
        <table className="min-w-full divide-y divide-gray-200 text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-2 text-left border-r">Full Name</th>
              <th className="px-4 py-2 text-left border-r">Email</th>
              <th className="px-4 py-2 text-left border-r">Roll Number</th>
              <th className="px-4 py-2 text-left border-r">Designated Role</th>
              <th className="px-4 py-2 text-left">Joined At</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {!selectedClubId && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-gray-500">
                  Select a club to view members.
                </td>
              </tr>
            )}

            {selectedClubId && membersLoading && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-gray-500">
                  Loading members...
                </td>
              </tr>
            )}

            {selectedClubId && !membersLoading && members.map((member) => (
              <tr key={member.id}>
                <td className="px-4 py-2 border-r">{member.full_name}</td>
                <td className="px-4 py-2 border-r">{member.email}</td>
                <td className="px-4 py-2 border-r">{member.roll_number || "-"}</td>
                <td className="px-4 py-2 border-r">{member.position}</td>
                <td className="px-4 py-2">{member.joined_at}</td>
              </tr>
            ))}

            {selectedClubId && !membersLoading && members.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-gray-500">
                  No members found for this club.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Clubs;