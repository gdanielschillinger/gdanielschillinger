'use client';

import React, { useState, useEffect } from 'react';

const SentientSyncCore = () => {
  const [pulse, setPulse] = useState({ status: 'OFFLINE', system_fingerprint: '0x000', active_threats: 0 });
  const [lastHash, setLastHash] = useState('');
  const [isNewData, setIsNewData] = useState(false);

  useEffect(() => {
    const fetchPulse = async () => {
      try {
        // Points to public/pulse.json where your Python script now saves data
        const response = await fetch('/pulse.json');
        const data = await response.json();
        
        if (data.system_fingerprint !== lastHash) {
          setIsNewData(true);
          setLastHash(data.system_fingerprint);
          setTimeout(() => setIsNewData(false), 200);
        }
        setPulse(data);
      } catch (e) {
        console.error("Link Lost");
      }
    };

    const interval = setInterval(fetchPulse, 3000);
    return () => clearInterval(interval);
  }, [lastHash]);

  const statusColor = pulse.status === 'ALERT' ? 'text-red-600' : 'text-emerald-500';
  const borderColor = pulse.status === 'ALERT' ? 'border-red-900/40' : 'border-emerald-900/40';

  return (
    <div className={`relative overflow-hidden bg-[#050505] border ${borderColor} p-6 rounded-sm font-mono uppercase shadow-2xl w-full max-w-md`}>
      {/* Scanline Visual */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.03]">
        <div className="w-full h-[1px] bg-white animate-scanline"></div>
      </div>

      <div className="flex justify-between items-start mb-10 relative z-10">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className={`w-1.5 h-1.5 rounded-full ${pulse.status === 'ALERT' ? 'bg-red-600 animate-ping' : 'bg-emerald-500'}`}></div>
            <span className="text-[9px] tracking-[0.3em] text-gray-600">Secure.Terminal.v1.2</span>
          </div>
          <h1 className={`text-2xl font-black tracking-tighter ${isNewData ? 'animate-data-flicker' : 'text-gray-100'}`}>
            SENTIENT<span className="text-gray-600">SYNC</span>
          </h1>
        </div>
        <div className={`px-3 py-1 text-[10px] font-bold border ${borderColor} bg-opacity-10 ${statusColor}`}>
          {pulse.status}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-8 mb-10 relative z-10">
        <div className="space-y-1">
          <p className="text-[8px] text-gray-500 tracking-widest">Active_Threats</p>
          <p className={`text-2xl font-bold tracking-tight ${statusColor}`}>
            {String(pulse.active_threats).padStart(2, '0')}
          </p>
        </div>
        <div className="space-y-1">
          <p className="text-[8px] text-gray-500 tracking-widest">Protocol</p>
          <p className="text-2xl font-bold text-gray-300 tracking-tight">AES-256</p>
        </div>
      </div>

      <div className={`p-3 bg-black/40 border-t ${borderColor} relative z-10`}>
        <span className="text-[8px] text-gray-600 tracking-[0.4em] block mb-2">Audit_Integrity_Hash</span>
        <code className={`text-[10px] block break-all leading-relaxed ${isNewData ? 'text-white' : 'text-gray-500'}`}>
          {pulse.system_fingerprint || "0x00000000000000000000"}
        </code>
      </div>
    </div>
  );
};

export default SentientSyncCore;
