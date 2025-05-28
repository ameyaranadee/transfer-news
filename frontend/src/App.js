import React, { useEffect, useState } from 'react';

export default function App() {
  const [tweets, setTweets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null); // Add error state

  useEffect(() => {
    fetch('/api/tweets')
      .then((res) => {
        if (!res.ok) {
          throw new Error('Failed to fetch tweets');
        }
        return res.json();
      })
      .then((data) => {
        setTweets(data.tweets);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message); // Save error
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white p-6">
      <h1 className="text-3xl font-bold mb-4">⚽ Fabrizio Transfer Feed</h1>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p style={{ color: "red" }}>Error: {error}</p>
      ) : (
        tweets.map((tweet, idx) => (
          <div key={idx} className="mb-4 p-4 border rounded-xl shadow-sm bg-gray-100 dark:bg-gray-800">
            <p>{tweet.text}</p>
            <p className="text-sm text-gray-500 mt-2">{new Date(tweet.created_at).toLocaleString()}</p>
            <a
              href={`https://x.com/FabrizioRomano/status/${tweet.id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline text-sm"
            >
              View on Twitter
            </a>
          </div>
        ))
      )}
    </div>
  );
}
