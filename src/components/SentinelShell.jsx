'use client';
import React, { useState } from 'react';

const SentinelShell = () => {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState(['>> SYSTEM READY. ENTER COMMAND...']);

  const handleCommand = async (e) => {
    if (e.key === 'Enter') {
      const cmd = input;
      setInput('');
      setHistory(prev => [...prev, `> ${cmd}`]);
      
      try {
        const res = await fetch('http://localhost:8000/system/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ command: cmd })
        });
        const data = await res.json();
        setHistory(prev => [...prev, data.response]);
      } catch (e) {
        setHistory(prev => [...prev, `[ERROR] API_UNAVAILABLE: ${e.message}`]);
      }
    }
  };

  return (
    <div className="bg-black border border-emerald-900/30 p-4 font-mono h-full flex flex-col">
      <div className="flex-grow overflow-y-auto text-[10px] text-emerald-500/80 mb-2 space-y-1 scrollbar-hide">
        {history.map((line, i) => <div key={i}>{line}</div>)}
      </div>
      <div className="flex items-center gap-2 border-t border-emerald-900/30 pt-2">
        <span className="text-emerald-500 animate-pulse">_</span>
        <input 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleCommand}
          className="bg-transparent border-none outline-none text-emerald-400 text-[10px] w-full"
          placeholder="TYPE_COMMAND..."
        />
      </div>
    </div>
  );
};

export default SentinelShell;
