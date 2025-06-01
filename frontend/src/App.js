import React, { useEffect, useState } from 'react';

function cleanText(text) {
  let cleaned = text.replace(/https?:\/\/\S+/g, "");
  cleaned = cleaned.replace(/\s+/g, " ").trim();
  return cleaned;
}

export default function App() {
  const [tweets, setTweets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/tweets")
      .then((res) => res.json())
      .then((data) => {
        let tweetsArray = [];
        if (Array.isArray(data)) {
          tweetsArray = data;
        } else if (Array.isArray(data.tweets)) {
          tweetsArray = data.tweets;
        }
        setTweets(tweetsArray);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching tweets:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white p-6">
      <h1 className="text-3xl font-bold mb-4">⚽ Fabrizio Transfer Feed</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul className="space-y-4">
          {tweets.map((tweet, idx) => (
            <li key={idx} className="p-4 border rounded-xl shadow-sm bg-gray-100 dark:bg-gray-800">
              <p>{cleanText(tweet.text)}</p>
              <p className="text-sm text-gray-500 mt-2">{new Date(tweet.created_at).toLocaleString()}</p>
              <a
                href={`https://x.com/i/web/status/${tweet.id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline text-sm"
              >
                View on Twitter
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
