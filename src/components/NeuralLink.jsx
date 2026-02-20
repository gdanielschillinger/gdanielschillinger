'use client';
import React, { useState, useEffect } from 'react';

const NeuralLink = () => {
  const [active, setActive] = useState(false);

  useEffect(() => {
    const checkLink = async () => {
      try {
        const res = await fetch('http://localhost:8000/system/vitals');
        const data = await res.json();
        if (data.neural_link && data.neural_link.active) {
          setActive(true);
          // Auto-deactivate after 3 seconds
          setTimeout(() => setActive(false), 3000);
        }
      } catch (e) {}
    };
    const interval = setInterval(checkLink, 500);
    return () => clearInterval(interval);
  }, []);

  if (!active) return null;

  return (
    <svg className="fixed inset-0 pointer-events-none z-10 w-full h-full opacity-50">
      <defs>
        <linearGradient id="neural-glow" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="transparent" />
          <stop offset="50%" stopColor="#10b981" />
          <stop offset="100%" stopColor="transparent" />
        </linearGradient>
        <filter id="neural-blur">
          <feGaussianBlur in="SourceGraphic" stdDeviation="2" />
        </filter>
      </defs>
      {/* Animated path from threat origin (upper area) to evidence locker (lower area) */}
      <path
        d="M 300 200 Q 600 400 950 750"
        stroke="url(#neural-glow)"
        strokeWidth="3"
        fill="transparent"
        strokeDasharray="500"
        className="animate-pulse"
        filter="url(#neural-blur)"
      />
      {/* Pulsing nodes at start and end */}
      <circle cx="300" cy="200" r="4" fill="#10b981" className="animate-pulse" />
      <circle cx="950" cy="750" r="4" fill="#10b981" className="animate-pulse" />
    </svg>
  );
};

export default NeuralLink;
