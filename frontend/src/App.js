import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [currentEmail, setCurrentEmail] = useState(null);
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [emailInfo, setEmailInfo] = useState(null);

  // Create new temporary email
  const createTempEmail = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post(`${API}/email/create`, {
        expiration_minutes: 60
      });
      
      setCurrentEmail(response.data);
      setTimeRemaining(response.data.remaining_time);
      setEmails([]);
      setSelectedEmail(null);
      
      // Start checking for emails
      startEmailPolling(response.data.email);
      
    } catch (err) {
      setError(`Failed to create email: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Fetch emails for current account
  const fetchEmails = async (emailAddress) => {
    try {
      const response = await axios.get(`${API}/email/${emailAddress}/messages`);
      setEmails(response.data);
    } catch (err) {
      if (err.response?.status === 404) {
        setError('Email account not found or expired');
        setCurrentEmail(null);
      } else if (err.response?.status === 410) {
        setError('Email account has expired');
        setCurrentEmail(null);
      } else {
        console.error('Error fetching emails:', err);
      }
    }
  };

  // Get email account info
  const getEmailInfo = async (emailAddress) => {
    try {
      const response = await axios.get(`${API}/email/${emailAddress}/info`);
      setEmailInfo(response.data);
      setTimeRemaining(response.data.remaining_time);
    } catch (err) {
      if (err.response?.status === 404 || err.response?.status === 410) {
        setCurrentEmail(null);
        setEmailInfo(null);
      }
    }
  };

  // Start polling for emails
  const startEmailPolling = (emailAddress) => {
    // Initial fetch
    fetchEmails(emailAddress);
    getEmailInfo(emailAddress);
    
    // Set up polling interval
    const interval = setInterval(() => {
      fetchEmails(emailAddress);
      getEmailInfo(emailAddress);
    }, 10000); // Poll every 10 seconds

    // Cleanup on unmount
    return () => clearInterval(interval);
  };

  // Delete email account
  const deleteEmailAccount = async () => {
    if (!currentEmail) return;
    
    setLoading(true);
    try {
      await axios.delete(`${API}/email/${currentEmail.email}`);
      setCurrentEmail(null);
      setEmails([]);
      setSelectedEmail(null);
      setEmailInfo(null);
      setTimeRemaining(0);
    } catch (err) {
      setError(`Failed to delete email: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Format time remaining
  const formatTimeRemaining = (seconds) => {
    if (seconds <= 0) return 'Expired';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${secs}s`;
    } else {
      return `${secs}s`;
    }
  };

  // Update countdown timer
  useEffect(() => {
    if (timeRemaining > 0) {
      const timer = setInterval(() => {
        setTimeRemaining(prev => prev - 1);
      }, 1000);
      
      return () => clearInterval(timer);
    }
  }, [timeRemaining]);

  // Copy email to clipboard
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    // You could add a toast notification here
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            Temporary Email Service
          </h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Generate temporary email addresses to protect your privacy. Perfect for testing, 
            avoiding spam, or temporary registrations.
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 max-w-2xl mx-auto">
            <p>{error}</p>
          </div>
        )}

        {/* Email Generation Section */}
        <div className="max-w-4xl mx-auto">
          {!currentEmail ? (
            <div className="text-center">
              <button
                onClick={createTempEmail}
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-semibold py-3 px-8 rounded-lg shadow-lg transition-all duration-200 transform hover:scale-105"
              >
                {loading ? 'Creating...' : 'Generate Temporary Email'}
              </button>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-4">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">
                    Your Temporary Email
                  </h3>
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="text-lg font-mono bg-gray-100 px-3 py-1 rounded">
                      {currentEmail.email}
                    </span>
                    <button
                      onClick={() => copyToClipboard(currentEmail.email)}
                      className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-3 py-1 rounded text-sm"
                    >
                      Copy
                    </button>
                  </div>
                  <p className="text-sm text-gray-600">
                    Expires in: <span className="font-semibold text-red-600">
                      {formatTimeRemaining(timeRemaining)}
                    </span>
                  </p>
                </div>
                <div className="flex space-x-2 mt-4 md:mt-0">
                  <button
                    onClick={() => fetchEmails(currentEmail.email)}
                    disabled={loading}
                    className="bg-green-600 hover:bg-green-700 disabled:bg-green-300 text-white px-4 py-2 rounded"
                  >
                    Refresh
                  </button>
                  <button
                    onClick={deleteEmailAccount}
                    disabled={loading}
                    className="bg-red-600 hover:bg-red-700 disabled:bg-red-300 text-white px-4 py-2 rounded"
                  >
                    Delete
                  </button>
                  <button
                    onClick={createTempEmail}
                    disabled={loading}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white px-4 py-2 rounded"
                  >
                    New Email
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Email List */}
          {currentEmail && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Email List Panel */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">
                  Inbox ({emails.length})
                </h3>
                
                {emails.length === 0 ? (
                  <div className="text-center py-8">
                    <div className="text-gray-400 text-6xl mb-4">📧</div>
                    <p className="text-gray-500">No emails yet</p>
                    <p className="text-sm text-gray-400 mt-2">
                      Emails will appear here automatically
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {emails.map((email, index) => (
                      <div
                        key={index}
                        onClick={() => setSelectedEmail(email)}
                        className={`p-4 border rounded-lg cursor-pointer transition-all duration-200 hover:shadow-md ${
                          selectedEmail?.id === email.id
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="font-semibold text-gray-800 text-sm truncate">
                            {email.subject || 'No Subject'}
                          </h4>
                          <span className="text-xs text-gray-500 ml-2">
                            {new Date(email.date).toLocaleTimeString()}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mb-1">
                          From: {email.sender}
                        </p>
                        <p className="text-xs text-gray-500 line-clamp-2">
                          {email.body_text.substring(0, 100)}...
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Email Content Panel */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">
                  Email Content
                </h3>
                
                {selectedEmail ? (
                  <div className="space-y-4">
                    <div className="border-b pb-4">
                      <h4 className="font-semibold text-lg text-gray-800">
                        {selectedEmail.subject || 'No Subject'}
                      </h4>
                      <p className="text-sm text-gray-600 mt-1">
                        From: {selectedEmail.sender}
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(selectedEmail.date).toLocaleString()}
                      </p>
                    </div>
                    
                    <div className="max-h-96 overflow-y-auto">
                      {selectedEmail.body_html ? (
                        <div
                          className="prose max-w-none"
                          dangerouslySetInnerHTML={{ __html: selectedEmail.body_html }}
                        />
                      ) : (
                        <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono">
                          {selectedEmail.body_text}
                        </pre>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <div className="text-gray-400 text-6xl mb-4">📄</div>
                    <p className="text-gray-500">Select an email to view its content</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <p>
            Temporary emails are automatically deleted after expiration. 
            Never use for important communications.
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;