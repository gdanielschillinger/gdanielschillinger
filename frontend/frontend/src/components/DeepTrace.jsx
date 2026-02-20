'use client';
import React, { useState, useEffect } from 'react';

const DeepTrace = () => {
  const [thoughts, setThoughts] = useState([]);

  useEffect(() => {
    const fetchThoughts = async () => {
      try {
        const res = await fetch('http://localhost:8000/system/thoughts');
        const data = await res.json();
        setThoughts(data.thoughts || []);
      } catch (e) {}
    };
    const interval = setInterval(fetchThoughts, 800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-black/40 border border-gray-900 p-4 rounded-sm h-full font-mono overflow-hidden flex flex-col">
      <div className="flex justify-between items-center mb-3 border-b border-gray-900 pb-2">
        <span className="text-[10px] text-emerald-500/50 uppercase tracking-[0.2em]">Agentic_Deep_Trace</span>
        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
      </div>
      <div className="flex flex-col gap-1 overflow-y-auto flex-grow scrollbar-hide">
        {thoughts && thoughts.length > 0 ? (
          thoughts.map((t, i) => (
            <div key={i} className="text-[9px] text-emerald-400/80 leading-tight whitespace-nowrap overflow-hidden text-ellipsis">
              <span className="opacity-30 mr-2">[{new Date().toLocaleTimeString().split(' ')[0]}]</span>
              {t}
            </div>
          ))
        ) : (
          <div className="text-[9px] text-gray-700 italic py-2">Awaiting neural activity...</div>
        )}
      </div>
    </div>
  );
};

export default DeepTrace;
