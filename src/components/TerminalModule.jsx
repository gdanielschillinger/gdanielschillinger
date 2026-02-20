'use client';
import React, { useState, useEffect } from 'react';

const TerminalModule = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await fetch('/terminal_feed.json');
        const data = await response.json();
        setLogs(data.logs || []);
      } catch (e) {
        console.error("Terminal Link Lost");
      }
    };

    const interval = setInterval(fetchLogs, 3000);
    fetchLogs();
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-[#050505] border border-gray-900 p-4 rounded-sm font-mono text-[10px] h-64 w-full max-w-md shadow-2xl overflow-hidden relative">
      <div className="flex justify-between items-center mb-3 border-b border-gray-900 pb-2">
        <span className="text-gray-600 tracking-widest uppercase">Live_Forensic_Feed</span>
        <span className="text-emerald-500/50 animate-pulse">REC ●</span>
      </div>
      
      <div className="space-y-1 opacity-80">
        {logs.map((log, i) => (
          <div key={i} className="border-l border-emerald-900/30 pl-2 py-0.5">
            <span className="text-emerald-500/70 mr-2">[{new Date().toLocaleTimeString()}]</span>
            <span className="text-gray-400 break-all">{log}</span>
          </div>
        ))}
      </div>

      {/* Fade effect at the bottom for that "Infinite Scroll" vibe */}
      <div className="absolute bottom-0 left-0 w-full h-12 bg-gradient-to-t from-[#050505] to-transparent pointer-events-none"></div>
    </div>
  );
};

export default TerminalModule;
