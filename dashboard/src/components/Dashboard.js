import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSummary();
    const interval = setInterval(fetchSummary, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchSummary = async () => {
    try {
      const response = await axios.get(`${API_URL}/ceo/summary`);
      setSummary(response.data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8">Loading...</div>;
  if (error) return <div className="p-8 text-red-600">Error: {error}</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">Apex Intelligence CEO Dashboard</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Leads Card */}
          <div className="bg-blue-600 p-6 rounded-lg">
            <h2 className="text-lg font-semibold mb-2">Leads</h2>
            <p className="text-3xl font-bold">{summary?.lead_count || 0}</p>
            <p className="text-sm mt-2 opacity-80">In Pipeline</p>
          </div>

          {/* Deals Card */}
          <div className="bg-green-600 p-6 rounded-lg">
            <h2 className="text-lg font-semibold mb-2">Deals</h2>
            <p className="text-3xl font-bold">{summary?.deal_count || 0}</p>
            <p className="text-sm mt-2 opacity-80">Active Negotiations</p>
          </div>

          {/* Audits Card */}
          <div className="bg-purple-600 p-6 rounded-lg">
            <h2 className="text-lg font-semibold mb-2">Audits</h2>
            <p className="text-3xl font-bold">{summary?.audit_count || 0}</p>
            <p className="text-sm mt-2 opacity-80">In Progress</p>
          </div>

          {/* Support Tickets Card */}
          <div className="bg-orange-600 p-6 rounded-lg">
            <h2 className="text-lg font-semibold mb-2">Support</h2>
            <p className="text-3xl font-bold">{summary?.ticket_count || 0}</p>
            <p className="text-sm mt-2 opacity-80">Open Tickets</p>
          </div>
        </div>

        {/* Status Section */}
        <div className="bg-gray-800 p-6 rounded-lg mb-8">
          <h2 className="text-2xl font-bold mb-4">Company Status</h2>
          <p className="text-lg mb-2"><strong>Status:</strong> {summary?.company_status}</p>
          <p className="text-lg mb-4"><strong>Message:</strong> {summary?.status_message}</p>
          <p className="text-yellow-400 font-semibold">⚠️ Pending Approvals: {summary?.pending_approvals || 0}</p>
        </div>

        {/* Key Notes */}
        <div className="bg-gray-800 p-6 rounded-lg">
          <h2 className="text-2xl font-bold mb-4">Key Notes</h2>
          <ul className="space-y-2">
            {summary?.key_notes?.map((note, idx) => (
              <li key={idx} className="flex items-start">
                <span className="text-green-400 mr-3">✓</span>
                <span>{note}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
