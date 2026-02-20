'use client';
import React, { useState, useEffect } from 'react';

const SentientCreed = () => {
  const [text, setText] = useState('');
  const [isVisible, setIsVisible] = useState(true);
  
  const fullText = [
    '>> SENTIENT_SYNC_INITIALIZED...',
    '>> PROTOCOL: SECURE THE AGI. PROTECT THE SYNC.',
    '>> AUTHOR: D. SCHILLINGER // MIAMI_NODE_01',
    '>> STATUS: DEFENSE_GRID_ACTIVE'
  ].join('\n');

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      setText(fullText.slice(0, index));
      index++;
      if (index > fullText.length) {
        clearInterval(interval);
        setTimeout(() => setIsVisible(false), 2000);
      }
    }, 30);

    return () => clearInterval(interval);
  }, []);

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 z-[9999] bg-black flex items-center justify-center p-10 font-mono">
      <div className="max-w-2xl w-full">
        <pre className="text-emerald-500 text-sm md:text-lg leading-relaxed whitespace-pre-wrap">
          {text}
          <span className="animate-pulse bg-emerald-500 ml-1">_</span>
        </pre>
      </div>
    </div>
  );
};

export default SentientCreed;
