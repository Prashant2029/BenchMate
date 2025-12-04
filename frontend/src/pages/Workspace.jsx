import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Brain, Zap, FileText } from 'lucide-react';
import Chat from '../components/Chat';
import Notes from '../components/Notes';
import Header from '../components/Header';
import api from '../api';

const Workspace = () => {
    const { pdfId } = useParams();
    const navigate = useNavigate();
    const [document, setDocument] = useState(null);
    const [activeLeftTab, setActiveLeftTab] = useState('notes'); // 'notes' or 'info'
    const [notesContent, setNotesContent] = useState('');

    useEffect(() => {
        const fetchDocument = async () => {
            try {
                // We might need a specific endpoint for single doc or filter list
                // For now, let's assume we can get it or just use the ID
                // Ideally we should have an endpoint like /core/documents/:id/
                // But we can just proceed with the ID for now
                setDocument({ id: pdfId, name: 'Document' });
            } catch (error) {
                console.error('Failed to load document', error);
            }
        };

        const fetchNotes = async () => {
            try {
                const response = await api.get(`/core/notes/?pdf_id=${pdfId}`);
                setNotesContent(response.data.content || '');
            } catch (error) {
                console.error('Failed to fetch notes:', error);
            }
        };

        if (pdfId) {
            fetchDocument();
            fetchNotes();
        }
    }, [pdfId]);

    const handleAddToNotes = (text) => {
        const newContent = notesContent ? `${notesContent}\n\n${text}` : text;
        setNotesContent(newContent);
        // Optional: Auto-save immediately or let Notes component handle it via effect
        // For better UX, we might want to trigger a save or switch tab
        setActiveLeftTab('notes');
    };

    return (
        <div className="h-screen flex flex-col bg-black text-white overflow-hidden">
            <Header />

            {/* Sub-Header / Toolbar */}
            <div className="h-14 border-b border-white/10 flex items-center justify-between px-6 bg-white/5">
                <div className="flex items-center gap-4">
                    <Link to="/dashboard" className="p-2 hover:bg-white/10 rounded-full transition-colors">
                        <ArrowLeft className="w-5 h-5" />
                    </Link>
                    <h1 className="font-bold text-lg truncate max-w-md">
                        {document?.name || 'Workspace'}
                    </h1>
                </div>

                <div className="flex items-center gap-4">
                    <button
                        onClick={() => navigate(`/quiz/${pdfId}`)}
                        className="flex items-center gap-2 px-3 py-1.5 bg-purple-500/20 text-purple-400 rounded-lg hover:bg-purple-500/30 transition-colors border border-purple-500/30 text-sm"
                    >
                        <Brain className="w-4 h-4" />
                        <span>Generate Quiz</span>
                    </button>
                    <button
                        onClick={() => navigate(`/flashcards/${pdfId}`)}
                        className="flex items-center gap-2 px-3 py-1.5 bg-yellow-500/20 text-yellow-400 rounded-lg hover:bg-yellow-500/30 transition-colors border border-yellow-500/30 text-sm"
                    >
                        <Zap className="w-4 h-4" />
                        <span>Flashcards</span>
                    </button>
                </div>
            </div>

            {/* Main Content - Split View */}
            <div className="flex-1 flex overflow-hidden">
                {/* Left Panel: Notes / PDF Info */}
                <div className="w-1/2 border-r border-white/10 flex flex-col p-4">
                    <div className="flex gap-4 mb-4">
                        <button
                            onClick={() => setActiveLeftTab('notes')}
                            className={`pb-2 border-b-2 transition-colors ${activeLeftTab === 'notes' ? 'border-purple-500 text-white' : 'border-transparent text-white/40'}`}
                        >
                            Notes
                        </button>
                        {/* Future: Add PDF Viewer tab here */}
                    </div>

                    <div className="flex-1 overflow-hidden">
                        {activeLeftTab === 'notes' && (
                            <Notes
                                pdfId={pdfId}
                                content={notesContent}
                                onChange={setNotesContent}
                            />
                        )}
                    </div>
                </div>

                {/* Right Panel: Chat */}
                <div className="w-1/2 flex flex-col bg-white/5">
                    <Chat pdfId={pdfId} onAddToNotes={handleAddToNotes} />
                </div>
            </div>
        </div>
    );
};

export default Workspace;
