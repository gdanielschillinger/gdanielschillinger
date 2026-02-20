'use client';
import React, { useState, useEffect } from 'react';

const EvidenceLocker = () => {
  const [cases, setCases] = useState([]);

  const fetchCases = async () => {
    try {
      const response = await fetch('/evidence_list.json');
      const data = await response.json();
      setCases(data);
    } catch (e) { console.log('Waiting for evidence...'); }
  };

  useEffect(() => {
    fetchCases();
    const interval = setInterval(fetchCases, 3000);
    return () => clearInterval(interval);
  }, []);

  const resetVault = async () => {
    const confirmReset = window.confirm('PERMANENTLY PURGE FORENSIC VAULT?');
    if (!confirmReset) return;
    try {
      await fetch('http://localhost:8000/system/clear-vault', { method: 'POST' });
      alert('VAULT PURGED // SYSTEM IDLE');
      fetchCases();
    } catch (e) {
      console.error('Vault purge failed', e);
      alert('VAULT PURGE FAILED');
    }
  };

  return (
    <div className="bg-[#050505] border border-gray-900 p-6 rounded-sm min-h-[200px]">
      <div className="flex justify-between items-center mb-6">
        <span className="text-[10px] text-gray-500 tracking-[0.4em] uppercase">Forensic_Archive</span>
        <div className="flex items-center gap-2">
          <button 
            onClick={resetVault}
            className="text-[8px] border border-red-900/50 px-2 py-1 text-red-500 hover:bg-red-500 hover:text-black transition-all uppercase tracking-widest"
          >
            Purge_Vault
          </button>
          <span className="text-[8px] text-red-500 animate-pulse">VAULT_ENCRYPTED</span>
        </div>
      </div>

      <div className="space-y-4">
        {cases.length > 0 ? cases.map((c, i) => (
          <div key={i} className="group border-l-2 border-red-900/30 bg-black/20 p-3 hover:bg-red-950/10 transition-all cursor-crosshair">
            <div className="flex justify-between items-start">
              <span className="text-[9px] text-red-500 font-bold uppercase tracking-tighter">{c.id}</span>
              <span className="text-[7px] text-gray-700">{c.time}</span>
            </div>
            <p className="text-[10px] text-gray-400 mt-1 uppercase leading-tight">{c.type}</p>
            <div className="mt-3 opacity-0 group-hover:opacity-100 transition-opacity flex justify-end">
              <a className="text-[7px] text-red-500/50 underline uppercase tracking-widest" href={`/${c.file}`} target="_blank" rel="noreferrer">Download_Artifact</a>
            </div>
          </div>
        )) : (
          <div className="h-32 flex items-center justify-center border border-dashed border-gray-900">
            <p className="text-[8px] text-gray-800 uppercase">No_Threats_Archived</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default EvidenceLocker;
