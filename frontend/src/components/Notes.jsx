import { useState, useEffect } from 'react';
import api from '../api';
import { Save, Loader } from 'lucide-react';

const Notes = ({ pdfId, content, onChange, onSave }) => {
    const [saving, setSaving] = useState(false);
    const [lastSaved, setLastSaved] = useState(null);

    // Fetching is now done in parent (Workspace)
    // useEffect(() => {
    //     const fetchNotes = async () => {
    //         try {
    //             const response = await api.get(`/core/notes/?pdf_id=${pdfId}`);
    //             setContent(response.data.content || '');
    //         } catch (error) {
    //             console.error('Failed to fetch notes:', error);
    //         }
    //     };
    //     if (pdfId) fetchNotes();
    // }, [pdfId]);

    const handleSave = async () => {
        setSaving(true);
        try {
            await api.post('/core/notes/', {
                pdf_id: pdfId,
                content: content
            });
            setLastSaved(new Date());
            if (onSave) onSave();
        } catch (error) {
            console.error('Failed to save notes:', error);
        } finally {
            setSaving(false);
        }
    };

    // Auto-save every 30 seconds if changed
    useEffect(() => {
        const interval = setInterval(() => {
            if (content) handleSave();
        }, 30000);
        return () => clearInterval(interval);
    }, [content, pdfId]);

    return (
        <div className="flex flex-col h-full bg-white/5 rounded-2xl border border-white/10 overflow-hidden">
            <div className="p-4 border-b border-white/10 flex justify-between items-center bg-white/5">
                <h3 className="font-bold text-white">Notes</h3>
                <div className="flex items-center gap-3">
                    {lastSaved && (
                        <span className="text-xs text-white/40">
                            Saved {lastSaved.toLocaleTimeString()}
                        </span>
                    )}
                    <button
                        onClick={handleSave}
                        disabled={saving}
                        className="p-2 hover:bg-white/10 rounded-lg transition-colors text-purple-400"
                        title="Save Notes"
                    >
                        {saving ? <Loader className="w-5 h-5 animate-spin" /> : <Save className="w-5 h-5" />}
                    </button>
                </div>
            </div>
            <textarea
                value={content}
                onChange={(e) => onChange(e.target.value)}
                placeholder="Type your notes here..."
                className="flex-1 bg-transparent p-4 text-white resize-none focus:outline-none placeholder-white/20 leading-relaxed"
            />
        </div>
    );
};

export default Notes;
