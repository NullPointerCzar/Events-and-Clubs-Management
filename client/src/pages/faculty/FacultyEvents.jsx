import { useState, useEffect } from "react";
import { getFacultyProposedEvents, reviewEvent } from "../../api/events";

const FacultyEvents = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");
  const [actionSuccess, setActionSuccess] = useState("");
  const [reviewingId, setReviewingId] = useState(null);
  const [remarks, setRemarks] = useState("");

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const res = await getFacultyProposedEvents();
      setEvents(res.data);
    } catch (err) {
      setError("Failed to load proposed events.");
    } finally {
      setLoading(false);
    }
  };

  const handleReview = async (eventId, decision) => {
    setActionError("");
    setActionSuccess("");
    try {
      await reviewEvent(eventId, { decision, remarks });
      setActionSuccess(`Event ${decision.toLowerCase()} successfully.`);
      setReviewingId(null);
      setRemarks("");
      // Refresh list (approved/rejected events will disappear from Proposed list)
      const res = await getFacultyProposedEvents();
      setEvents(res.data);
    } catch (err) {
      setActionError(err.response?.data?.detail || "Action failed.");
    }
  };

  if (loading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        Proposed Events — Pending Review
      </h2>

      {error && (
        <div className="bg-red-50 text-red-600 p-3 rounded text-sm mb-4">{error}</div>
      )}
      {actionSuccess && (
        <div className="bg-green-50 text-green-600 p-3 rounded text-sm mb-4">{actionSuccess}</div>
      )}
      {actionError && (
        <div className="bg-red-50 text-red-600 p-3 rounded text-sm mb-4">{actionError}</div>
      )}

      {events.length === 0 ? (
        <p className="text-gray-500 text-sm">No pending event proposals.</p>
      ) : (
        <div className="space-y-4">
          {events.map((ev) => (
            <div
              key={ev.id}
              className="border border-gray-200 rounded-lg p-4 hover:border-indigo-200 transition"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">{ev.title}</h3>
                  <p className="text-sm text-gray-500 mt-1">
                    <span className="font-medium">Club:</span> {ev.club_name} &nbsp;|&nbsp;
                    <span className="font-medium">Proposed by:</span> {ev.created_by_name} &nbsp;|&nbsp;
                    <span className="font-medium">Event Date:</span>{" "}
                    {new Date(ev.event_date).toLocaleDateString()}
                  </p>
                  {ev.description && (
                    <p className="text-sm text-gray-600 mt-2">{ev.description}</p>
                  )}
                </div>
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
                  {ev.status}
                </span>
              </div>

              {/* Review actions */}
              {reviewingId === ev.id ? (
                <div className="mt-4 space-y-3 border-t pt-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Remarks (optional)
                    </label>
                    <textarea
                      value={remarks}
                      onChange={(e) => setRemarks(e.target.value)}
                      rows={2}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Add remarks..."
                    />
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleReview(ev.id, "Approved")}
                      className="px-4 py-1.5 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 cursor-pointer"
                    >
                      Approve
                    </button>
                    <button
                      onClick={() => handleReview(ev.id, "Rejected")}
                      className="px-4 py-1.5 bg-red-600 text-white text-sm rounded-md hover:bg-red-700 cursor-pointer"
                    >
                      Reject
                    </button>
                    <button
                      onClick={() => {
                        setReviewingId(null);
                        setRemarks("");
                      }}
                      className="px-4 py-1.5 bg-gray-200 text-gray-700 text-sm rounded-md hover:bg-gray-300 cursor-pointer"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <div className="mt-3">
                  <button
                    onClick={() => setReviewingId(ev.id)}
                    className="px-4 py-1.5 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 cursor-pointer"
                  >
                    Review
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FacultyEvents;
