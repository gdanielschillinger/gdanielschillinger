'use client';
import React, { useState, useEffect } from 'react';

const ForensicTimeline = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch('http://localhost:8000/system/history');
        const data = await res.json();
        setHistory(data.history.reverse()); // Newest first
      } catch (e) {}
    };
    const interval = setInterval(fetchHistory, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-[#050505] border border-gray-900 p-4 rounded-sm h-full font-mono overflow-hidden flex flex-col">
      <div className="flex justify-between items-center mb-4 border-b border-gray-900 pb-2">
        <span className="text-[10px] text-gray-500 uppercase tracking-widest">Forensic_Chronicle</span>
      </div>
      <div className="flex-grow overflow-y-auto space-y-3 scrollbar-hide">
        {history.map((event, i) => (
          <div key={i} className="flex gap-4 items-start border-l border-gray-900 pl-4 relative">
            <div className={`absolute -left-[5px] top-1 w-2 h-2 rounded-full ${
              event.type === 'CRITICAL' ? 'bg-red-500 shadow-[0_0_10px_red]' : 'bg-emerald-500'
            }`}></div>
            <div className="flex flex-col">
              <span className="text-[8px] text-gray-700">{event.time}</span>
              <span className={`text-[9px] leading-tight ${
                event.type === 'CRITICAL' ? 'text-red-400' : 'text-gray-300'
              }`}>{event.msg}</span>
              <span className="text-[7px] text-gray-600 mt-1 font-mono">#{event.hash}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ForensicTimeline;
