'use client';

import { useState } from 'react';

export default function VideoDemo() {
  const [videoError, setVideoError] = useState(false);

  return (
    <div className="mb-12">
      <div className="video-container max-w-4xl mx-auto">
        {!videoError ? (
          <video
            controls
            className="w-full rounded-lg"
            onError={() => setVideoError(true)}
            preload="metadata"
          >
            <source src="/2.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        ) : (
          <div className="text-center py-12">
            <p className="text-accent mb-4">Video demo not available</p>
            <p className="text-sm text-gray-400">
              The demonstration video could not be loaded.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
