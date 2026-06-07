import React, { useState, useRef, useEffect } from 'react';
import { Menu, Plus, MessageSquare, Send, Mic, Image as ImageIcon, Settings, User, Compass, Code, Lightbulb, History } from 'lucide-react';

export default function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll ke pesan terbaru
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Simulasi pemanggilan backend FastAPI & Turbovec
  const handleSend = () => {
    if (!input.trim()) return;

    const newUserMessage = { id: Date.now(), text: input, sender: 'user' };
    setMessages(prev => [...prev, newUserMessage]);
    setInput('');
    setIsTyping(true);

    // Simulasi delay pencarian vektor (RAG)
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        text: `Ini adalah simulasi jawaban dari AcehGPT berdasarkan dokumen RAG yang dicari menggunakan Turbovec. Anda bertanya tentang: "${newUserMessage.text}". \n\nDi tahap produksi, teks ini akan dihasilkan oleh model LLM (seperti Llama 3 atau Gemini) melalui backend FastAPI Anda.`,
        sender: 'ai'
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsTyping(false);
    }, 1500);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const suggestions = [
    { icon: <Compass className="w-5 h-5" />, text: "Sejarah Kesultanan Aceh" },
    { icon: <Lightbulb className="w-5 h-5" />, text: "Ringkas dokumen kebijakan" },
    { icon: <Code className="w-5 h-5" />, text: "Jelaskan algoritma Turbovec" },
    { icon: <History className="w-5 h-5" />, text: "Analisis sentimen wisata Aceh" },
  ];

  return (
    <div className="flex h-screen w-full bg-white text-gray-800 font-sans overflow-hidden selection:bg-red-200">
      
      {/* SIDEBAR */}
      <div className={`${isSidebarOpen ? 'w-72' : 'w-0'} transition-all duration-300 ease-in-out bg-gray-50 flex flex-col border-r border-gray-100 flex-shrink-0 overflow-hidden`}>
        <div className="p-4 flex items-center h-16">
          <button 
            onClick={() => setIsSidebarOpen(false)}
            className="p-2 hover:bg-gray-200 rounded-full transition-colors text-gray-600"
          >
            <Menu className="w-6 h-6" />
          </button>
        </div>

        <div className="px-4 pb-4">
          <button className="flex items-center gap-3 bg-red-50 hover:bg-red-100 text-red-700 px-4 py-3 rounded-2xl w-fit font-medium transition-all shadow-sm border border-red-100">
            <Plus className="w-5 h-5" />
            <span>Chat Baru</span>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-3 py-2">
          <h3 className="text-xs font-semibold text-gray-400 mb-3 px-3 uppercase tracking-wider">Terbaru</h3>
          <ul className="space-y-1">
            {['Analisis Sentimen Data', 'Integrasi Turbovec', 'Resep Mie Aceh'].map((title, i) => (
              <li key={i}>
                <button className="w-full flex items-center gap-3 px-3 py-2.5 hover:bg-gray-200 rounded-xl text-left text-sm text-gray-700 transition-colors truncate">
                  <MessageSquare className="w-4 h-4 flex-shrink-0 text-gray-400" />
                  <span className="truncate">{title}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div className="p-3 border-t border-gray-100">
          <button className="w-full flex items-center gap-3 px-3 py-2.5 hover:bg-gray-200 rounded-xl text-left text-sm text-gray-700 transition-colors">
            <Settings className="w-4 h-4 text-gray-500" />
            <span>Pengaturan</span>
          </button>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div className="flex-1 flex flex-col h-full relative">
        
        {/* HEADER */}
        <header className="h-16 flex items-center justify-between px-4 lg:px-8 absolute top-0 w-full z-10 bg-white/80 backdrop-blur-md">
          <div className="flex items-center gap-4">
            {!isSidebarOpen && (
              <button 
                onClick={() => setIsSidebarOpen(true)}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors text-gray-600"
              >
                <Menu className="w-6 h-6" />
              </button>
            )}
            <h1 className="text-xl font-semibold text-gray-800 tracking-tight">
              Aceh<span className="text-red-600">GPT</span>
            </h1>
          </div>
          <div className="w-9 h-9 rounded-full bg-red-100 flex items-center justify-center text-red-600 border border-red-200 cursor-pointer hover:ring-2 ring-red-100 transition-all">
            <User className="w-5 h-5" />
          </div>
        </header>

        {/* CHAT AREA */}
        <div className="flex-1 overflow-y-auto scroll-smooth pt-20 pb-32 px-4 lg:px-0">
          <div className="max-w-3xl mx-auto w-full flex flex-col gap-6">
            
            {/* EMPTY STATE (Welcome Screen) */}
            {messages.length === 0 && (
              <div className="mt-10 lg:mt-20 flex flex-col px-2">
                <h2 className="text-4xl lg:text-5xl font-medium tracking-tight mb-2">
                  <span className="bg-gradient-to-r from-red-600 to-red-400 bg-clip-text text-transparent drop-shadow-sm">Halo, ada yang</span><br/>
                  <span className="text-gray-300">bisa dibantu hari ini?</span>
                </h2>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-12">
                  {suggestions.map((item, idx) => (
                    <button 
                      key={idx}
                      onClick={() => { setInput(item.text); }}
                      className="flex flex-col gap-3 p-4 bg-gray-50 hover:bg-red-50 rounded-2xl border border-transparent hover:border-red-100 transition-all text-left group"
                    >
                      <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center text-gray-600 group-hover:text-red-600 shadow-sm transition-colors">
                        {item.icon}
                      </div>
                      <span className="text-sm text-gray-600 group-hover:text-gray-900 font-medium leading-relaxed">
                        {item.text}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* CHAT BUBBLES */}
            {messages.map((msg) => (
              <div key={msg.id} className={`flex gap-4 w-full ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                {msg.sender === 'ai' && (
                  <div className="w-8 h-8 rounded-full bg-red-600 flex-shrink-0 flex items-center justify-center shadow-md">
                    <span className="text-white text-xs font-bold font-serif">A</span>
                  </div>
                )}
                <div className={`px-5 py-3.5 max-w-[85%] lg:max-w-[75%] text-[15px] leading-relaxed ${
                  msg.sender === 'user' 
                    ? 'bg-red-50 text-red-900 rounded-3xl rounded-tr-sm' 
                    : 'bg-transparent text-gray-800'
                }`}>
                  {msg.text}
                </div>
              </div>
            ))}

            {/* TYPING INDICATOR */}
            {isTyping && (
              <div className="flex gap-4 w-full justify-start animate-pulse">
                <div className="w-8 h-8 rounded-full bg-red-600/50 flex-shrink-0 flex items-center justify-center">
                  <span className="text-white text-xs font-bold font-serif">A</span>
                </div>
                <div className="px-5 py-3.5 bg-transparent text-gray-500 text-[15px]">
                  Sedang menelusuri dokumen...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* INPUT AREA */}
        <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-white via-white to-transparent pt-6 pb-6 px-4 lg:px-0">
          <div className="max-w-3xl mx-auto relative">
            <div className="bg-gray-100 rounded-[2rem] p-2 flex items-end gap-2 border border-gray-200 focus-within:bg-white focus-within:border-red-300 focus-within:shadow-md transition-all duration-300">
              
              <button className="p-3 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors flex-shrink-0">
                <ImageIcon className="w-5 h-5" />
              </button>
              
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Tanya AcehGPT atau cari dokumen..."
                className="flex-1 bg-transparent border-none outline-none resize-none max-h-32 py-3 px-2 text-gray-800 placeholder-gray-400 overflow-y-auto leading-relaxed"
                rows={1}
                style={{ minHeight: '44px' }}
              />

              <div className="flex items-center gap-1 mb-1 pr-1">
                {input.trim() ? (
                  <button 
                    onClick={handleSend}
                    className="p-3 bg-red-600 text-white hover:bg-red-700 rounded-full transition-colors shadow-sm flex-shrink-0"
                  >
                    <Send className="w-4 h-4 ml-0.5" />
                  </button>
                ) : (
                  <button className="p-3 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors flex-shrink-0">
                    <Mic className="w-5 h-5" />
                  </button>
                )}
              </div>
            </div>
            <div className="text-center mt-3">
              <span className="text-xs text-gray-400">
                AcehGPT dapat menampilkan informasi yang tidak akurat. Harap verifikasi kembali.
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}