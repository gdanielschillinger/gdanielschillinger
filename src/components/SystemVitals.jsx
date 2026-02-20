'use client';
import React, { useState, useEffect } from 'react';

const SystemVitals = () => {
  const [vitals, setVitals] = useState(null);
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const fetchVitals = async () => {
      try {
        const res = await fetch('http://localhost:8000/system/vitals');
        const data = await res.json();
        setVitals(data);
      } catch (e) { setVitals(null); }
    };
    fetchVitals();
    const iv = setInterval(fetchVitals, 2000);
    const t = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    return () => { clearInterval(iv); clearInterval(t); };
  }, []);

  if (!vitals) return <div className="text-[8px] text-red-900 animate-pulse">API_OFFLINE</div>;

  return (
    <div className="flex gap-6 items-center">
      <div className="flex flex-col">
        <span className="text-[7px] text-gray-600 uppercase">Node_Load</span>
        <span className="text-[9px] text-emerald-500 font-mono">{vitals.cpu_load}</span>
      </div>
      <div className="flex flex-col">
        <span className="text-[7px] text-gray-600 uppercase">Agent_Status</span>
        <span className="text-[9px] text-emerald-500 font-mono">{vitals.status}</span>
      </div>
      <div className="flex flex-col border-l border-gray-900 pl-4">
        <span className="text-[7px] text-gray-600 uppercase">2026_Sync_Time</span>
        <span className="text-[9px] text-white/80 font-mono">{time}</span>
      </div>
      <div className="flex flex-col border-l border-gray-900 pl-4">
        <span className="text-[7px] text-gray-600 uppercase">Lifetime_Neutralized</span>
        <span className="text-[10px] text-emerald-500 font-mono font-bold">
          {(vitals.total_neutralized || 0).toLocaleString()}
        </span>
      </div>
      <div className="flex flex-col border-l border-gray-900 pl-4">
        <span className="text-[7px] text-gray-600 uppercase">System_ID</span>
        <span className="text-[9px] text-white/80 font-mono">{vitals.node}</span>
      </div>
    </div>
  );
};

export default SystemVitals;
