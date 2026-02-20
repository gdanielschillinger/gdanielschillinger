"use client";
import React, { useEffect, useState } from 'react';
import SentientSyncCore from '../components/SentientSyncCore';
import TerminalModule from '../components/TerminalModule';
import EvidenceLocker from '../components/EvidenceLocker';
import SystemVitals from '../components/SystemVitals';
import ThreatMap from '../components/ThreatMap';
import SentientCreed from '../components/SentientCreed';
import NeuralLink from '../components/NeuralLink';
import DeepTrace from '../components/DeepTrace';

export default function Home() {
  const [pulseData, setPulseData] = useState({});
  const [apiOnline, setApiOnline] = useState(true);

  useEffect(() => {
    const fetchPulse = async () => {
      try {
        const res = await fetch('/pulse.json');
        const d = await res.json();
        setPulseData(d || {});
      } catch (e) {
        // silent
      }
    };
    fetchPulse();
    const iv = setInterval(fetchPulse, 3000);
    return () => clearInterval(iv);
  }, []);

  useEffect(() => {
    const checkApi = async () => {
      try {
        const res = await fetch('http://localhost:8000/system/vitals');
        if (res.ok) {
          setApiOnline(true);
        } else {
          setApiOnline(false);
        }
      } catch (e) {
        setApiOnline(false);
      }
    };
    checkApi();
    const iv = setInterval(checkApi, 2000);
    return () => clearInterval(iv);
  }, []);
  return (
    <main className="min-h-screen bg-[#050505] p-8 md:p-16 font-mono selection:bg-emerald-500/30 relative">
      <SentientCreed />
      <NeuralLink />
      {!apiOnline && (
        <div className="fixed inset-0 z-[10000] bg-red-900/20 backdrop-blur-md flex items-center justify-center">
          <div className="text-red-500 font-mono text-xl animate-bounce text-center">
            <div>CRITICAL_SYSTEM_FAILURE</div>
            <div className="text-sm mt-2">API_OFFLINE</div>
          </div>
        </div>
      )}
      {/* Header Section */}
      <div className="max-w-6xl mx-auto mb-12 flex justify-between items-end border-b border-gray-900 pb-6">
        <div>
          <h1 className="text-white text-2xl font-bold tracking-[0.3em] uppercase">Sentient_Sync // SOC</h1>
          <p className="text-[10px] text-gray-500 mt-2 tracking-widest uppercase">
            Forensic Integrity: <span className="text-emerald-500">Active</span> // HMAC-256 Verified
          </p>
        </div>
        <div className="text-right hidden md:block">
          <SystemVitals />
        </div>
      </div>
      </div>

      {/* Module 05: Evidence Locker (The 'Paper Trail') */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        <div className="lg:col-span-1">
          <EvidenceLocker />
        </div>
      </div>
      {/* Bento Grid Scaffolding */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Module 1: The Core Signal */}
        <div className="lg:col-span-1">
          <SentientSyncCore />
        </div>

        {/* Module 2: The Live Forensic Feed */}
        <div className="lg:col-span-2">
          <TerminalModule />
        </div>

        {/* Module 3: The Sentient Brain (LIVE) */}
        <div className="bg-[#080808] border border-emerald-900/20 rounded-sm p-6 flex flex-col justify-between group hover:border-emerald-500/40 transition-all">
          <div className="flex justify-between items-start">
            <span className="text-[9px] text-emerald-500 tracking-[0.3em] uppercase">Agent_Logic_Gate</span>
            <div className="flex gap-1">
              <div className="w-1 h-1 bg-emerald-500 animate-ping"></div>
            </div>
          </div>
          
          <div className="mt-4">
            <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">Current_Thought:</p>
            <p className="text-[11px] text-emerald-500/80 mt-1 italic">"{pulseData.ai_thought || 'Passive monitoring active...'}"</p>
          </div>

          <div className="mt-4 pt-4 border-t border-gray-900 flex justify-between items-center">
            <span className="text-[8px] text-gray-600 uppercase">Decision_Node: AUDITOR_V1</span>
            <span className="text-[8px] bg-emerald-900/20 text-emerald-500 px-2 py-0.5 rounded-full uppercase">Active</span>
          </div>
        </div>

        {/* Module 4: Threat Origin Map */}
        <div className="lg:col-span-2 md:col-span-2">
          <ThreatMap />
        </div>

        {/* Module 5: Deep Trace (Agentic Monologue) */}
        <div className="lg:col-span-1">
          <DeepTrace />
        </div>

      </div>
    </main>
  );
}
