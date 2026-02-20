'use client';
import React, { useState, useEffect } from 'react';

const SentientSyncCore = () => {
  const [entropy, setEntropy] = useState("STABLE");

  useEffect(() => {
    const checkEntropy = async () => {
      try {
        const res = await fetch('http://localhost:8000/system/vitals');
        const data = await res.json();
        setEntropy(data.entropy);
      } catch (e) {}
    };
    checkEntropy();
    const interval = setInterval(checkEntropy, 2000);
    return () => clearInterval(interval);
  }, []);

  const isHigh = entropy === "HIGH_ENTROPY";

  return (
    <div className="flex items-center justify-center h-full relative group">
      {/* The Core Orb */}
      <div className={`
        w-24 h-24 rounded-full border-2 transition-all duration-1000
        ${isHigh ? 'border-red-500 shadow-[0_0_50px_rgba(239,68,68,0.5)]' : 'border-emerald-500 shadow-[0_0_30px_rgba(16,185,129,0.3)]'}
      `}>
        {/* Internal Neural Pulse */}
        <div className={`
          absolute inset-4 rounded-full animate-ping
          ${isHigh ? 'bg-red-900/40' : 'bg-emerald-900/40'}
        `}></div>
        
        {/* Core Status Text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-[8px] uppercase tracking-tighter ${isHigh ? 'text-red-500' : 'text-emerald-500/50'}`}>
            Core_{entropy}
          </span>
        </div>
      </div>
      
      {/* Background Grid Accent */}
      <div className="absolute -inset-10 bg-[radial-gradient(circle,_rgba(16,185,129,0.05)_1px,_transparent_1px)] bg-[size:10px_10px] opacity-20"></div>
    </div>
  );
};

export default SentientSyncCore;
