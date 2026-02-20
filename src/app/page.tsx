 'use client';
import React, { useEffect, useState } from 'react';
import SentientSyncCore from '@/components/SentientSyncCore';
import TerminalModule from '@/components/TerminalModule';
import EvidenceLocker from '@/components/EvidenceLocker';
import NeuralLink from '@/components/NeuralLink';
import DeepTrace from '@/components/DeepTrace';

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
    <main className="min-h-screen bg-[#050505] text-gray-400 p-6 md:p-12 font-mono relative">
      <NeuralLink />
      {!apiOnline && (
        <div className="fixed inset-0 z-[10000] bg-red-900/20 backdrop-blur-md flex items-center justify-center">
          <div className="text-red-500 font-mono text-xl animate-bounce text-center">
            <div>CRITICAL_SYSTEM_FAILURE</div>
            <div className="text-sm mt-2">API_OFFLINE</div>
          </div>
        </div>
      )}
      {/* Header Info */}
      <div className="max-w-6xl mx-auto mb-12 flex justify-between items-end">
        <div>
          <h1 className="text-white text-xl font-bold tracking-[0.2em] uppercase">Sentient_Sync // Terminal</h1>
          <p className="text-[10px] text-gray-600 mt-1 uppercase">Operator: Gerd Daniel Schillinger // Auth: Level_01</p>
        </div>
        <div className="text-right hidden md:block">
          <p className="text-[10px] text-gray-600 uppercase">System_Clock</p>
          <p className="text-xs text-emerald-500/50">{new Date().toLocaleDateString()} // {new Date().toLocaleTimeString()}</p>
        </div>
      </div>

      {/* Bento Grid */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-fr">
        
        {/* Module 01: Core Status (Spans 1 col) */}
        <div className="md:col-span-1 flex flex-col">
          <SentientSyncCore />
        </div>

        {/* Module 02: Forensic Feed (Spans 2 cols) */}
        <div className="md:col-span-2 flex flex-col">
          <TerminalModule />
        </div>

        {/* Module 03: The Sentient Brain (LIVE) */}
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

        {/* Module 04: The Logic Path (Visualizing the Brain) */}
        <div className="md:col-span-2 border border-emerald-900/10 bg-[#080808] p-6 rounded-sm">
          <div className="flex justify-between items-center mb-6">
            <span className="text-[9px] text-gray-500 tracking-[0.3em] uppercase">Decision_Path_Visualization</span>
            <span className="text-[8px] text-emerald-500/50">NODE_COUNT: 04</span>
          </div>
          
          <div className="flex justify-between items-center px-4 relative">
            {/* Simple SVG/CSS path to show logic flow */}
            <div className="flex flex-col items-center gap-2">
              <div className="w-12 h-6 border border-emerald-500/50 rounded-sm text-[8px] flex items-center justify-center text-emerald-500">AUDITOR</div>
              <div className="h-4 w-px bg-emerald-900/40"></div>
            </div>
            <div className="flex flex-col items-center gap-2 opacity-50">
              <div className="w-12 h-6 border border-gray-800 rounded-sm text-[8px] flex items-center justify-center">TRIAGER</div>
            </div>
            {/* Adding a "Pulse" to the active node */}
            <div className="absolute left-[15%] top-[-10px] w-2 h-2 bg-emerald-500 rounded-full animate-ping"></div>
          </div>
        </div>

      </div>

      {/* Module 05: Evidence Locker (The 'Paper Trail') */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
        <div className="md:col-span-1">
          <EvidenceLocker />
        </div>
        <div className="md:col-span-2">
          <DeepTrace />
        </div>
      </div>

      {/* Footer / Disclaimer */}
      <div className="max-w-6xl mx-auto mt-12 pt-6 border-t border-gray-900 flex justify-between">
        <span className="text-[8px] text-gray-700 uppercase tracking-widest">Sentient Sync v1.2 // Forensic Integrity Protocol</span>
        <span className="text-[8px] text-gray-700 uppercase tracking-widest underline decoration-gray-800 cursor-help">Security_Whitepaper.pdf</span>
      </div>
    </main>
  );
}
