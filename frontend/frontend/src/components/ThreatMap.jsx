'use client';
import React, { useState, useEffect } from 'react';

const ThreatMap = () => {
  const [origin, setOrigin] = useState({ name: "SCANNING", lat: "0", lon: "0" });

  useEffect(() => {
    const fetchOrigin = async () => {
      try {
        const res = await fetch('http://localhost:8000/system/vitals');
        const data = await res.json();
        setOrigin(data.active_threat_origin || { name: 'UNKNOWN', lat: '0', lon: '0' });
      } catch (e) { }
    };
    fetchOrigin();
    const interval = setInterval(fetchOrigin, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-[#050505] border border-gray-900 p-6 rounded-sm h-full flex flex-col justify-between">
      <div className="flex justify-between items-center">
        <span className="text-[10px] text-gray-500 tracking-[0.4em] uppercase">Threat_Origin_Map</span>
        <span className="text-[9px] text-emerald-500 font-mono animate-pulse">{origin.name}</span>
      </div>

      <div className="relative mt-4 flex-grow border border-gray-900/50 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] overflow-hidden">
        <div className="absolute inset-0 opacity-20 bg-emerald-900/10"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
           <div className="w-2 h-2 bg-red-500 rounded-full animate-ping"></div>
           <div className="w-1 h-1 bg-red-500 rounded-full absolute top-0.5 left-0.5"></div>
        </div>
        <div className="absolute bottom-2 left-2 text-[7px] text-gray-700 font-mono">
          LAT: {origin.lat} // LON: {origin.lon}
        </div>
      </div>
    </div>
  );
};

export default ThreatMap;
