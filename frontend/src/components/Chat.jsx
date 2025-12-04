import { useState, useRef, useEffect } from 'react';
import api from '../api';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, Send, Loader, Bot, User, PlusCircle } from 'lucide-react';

const Chat = ({ pdfId, onAddToNotes }) => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await api.get(`/core/chat/?pdf_id=${pdfId}`);
                setMessages(response.data);
            } catch (error) {
                console.error('Failed to fetch chat history:', error);
            }
        };
        if (pdfId) fetchHistory();
    }, [pdfId]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            // Optimistic update
            const newMessages = [...messages, userMessage];
            setMessages(newMessages);

            const response = await api.post('/core/chat/', {
                pdf_id: pdfId,
                message: userMessage.content,
                // History is handled by backend now
            });

            const botMessage = { role: 'assistant', content: response.data.response };
            setMessages([...newMessages, botMessage]);
        } catch (error) {
            console.error('Chat failed:', error);
            setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-4xl mx-auto h-[600px] flex flex-col"
        >
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 flex flex-col h-full overflow-hidden">
                {/* Header */}
                <div className="p-4 border-b border-white/10 flex items-center gap-3 bg-white/5">
                    <MessageSquare className="w-6 h-6 text-purple-400" />
                    <h2 className="text-xl font-bold text-white">AI Tutor</h2>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
                    {messages.map((msg, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            {msg.role === 'assistant' && (
                                <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center border border-purple-500/30">
                                    <Bot className="w-5 h-5 text-purple-400" />
                                </div>
                            )}
                            <div
                                className={`p-4 rounded-2xl max-w-[80%] ${msg.role === 'user'
                                    ? 'bg-purple-500 text-white rounded-tr-none'
                                    : 'bg-white/10 text-white rounded-tl-none'
                                    }`}
                            >
                                <p className="whitespace-pre-wrap">{msg.content}</p>
                                {msg.role === 'assistant' && onAddToNotes && (
                                    <button
                                        onClick={() => onAddToNotes(msg.content)}
                                        className="mt-2 flex items-center gap-1 text-xs text-white/40 hover:text-white transition-colors"
                                    >
                                        <PlusCircle className="w-3 h-3" /> Save to Notes
                                    </button>
                                )}
                            </div>
                            {msg.role === 'user' && (
                                <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center border border-blue-500/30">
                                    <User className="w-5 h-5 text-blue-400" />
                                </div>
                            )}
                        </motion.div>
                    ))}
                    {loading && (
                        <div className="flex gap-3 justify-start">
                            <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center border border-purple-500/30">
                                <Bot className="w-5 h-5 text-purple-400" />
                            </div>
                            <div className="bg-white/10 p-3 rounded-2xl rounded-tl-none border border-white/10 flex items-center gap-2">
                                <span className="w-2 h-2 bg-white/40 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                <span className="w-2 h-2 bg-white/40 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                <span className="w-2 h-2 bg-white/40 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input */}
                <form onSubmit={handleSend} className="p-4 border-t border-white/10 bg-white/5">
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask a question about the document..."
                            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/40 focus:outline-none focus:border-purple-500 transition-colors"
                        />
                        <button
                            type="submit"
                            disabled={!input.trim() || loading}
                            className="bg-purple-500 hover:bg-purple-600 text-white p-3 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <Send className="w-5 h-5" />
                        </button>
                    </div>
                </form>
            </div>
        </motion.div>
    );
};

export default Chat;
