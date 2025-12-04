import { useState, useEffect, useContext } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Trophy, Star, LogOut, FileText, Trash2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import api from '../api';
import Upload from '../components/Upload';
import Header from '../components/Header';

const Dashboard = () => {
    const { user, logout } = useContext(AuthContext);
    const [profile, setProfile] = useState(null);
    const [documents, setDocuments] = useState([]);
    const [showUpload, setShowUpload] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchProfile();
        fetchDocuments();
    }, []);

    const fetchProfile = async () => {
        try {
            const response = await api.get('/gamification/profile/');
            setProfile(response.data);
        } catch (error) {
            console.error('Error fetching profile:', error);
            setError('Failed to load profile. Please try refreshing.');
        }
    };

    const fetchDocuments = async () => {
        try {
            const response = await api.get('/core/upload/');
            setDocuments(response.data);
        } catch (error) {
            console.error('Error fetching documents:', error);
        }
    };

    const handleUploadSuccess = (data) => {
        setShowUpload(false);
        fetchDocuments();
    };

    const handleDelete = async (e, id) => {
        e.preventDefault(); // Prevent navigation
        if (window.confirm('Are you sure you want to delete this document?')) {
            try {
                await api.delete(`/core/documents/${id}/`);
                fetchDocuments();
            } catch (error) {
                console.error('Failed to delete document:', error);
                alert('Failed to delete document');
            }
        }
    };

    if (error) {
        return (
            <div className="text-white text-center mt-20">
                <p className="text-red-400 mb-4">{error}</p>
                <button
                    onClick={() => window.location.reload()}
                    className="px-4 py-2 bg-white/10 rounded-lg hover:bg-white/20 transition-colors"
                >
                    Retry
                </button>
            </div>
        );
    }

    if (!profile) return <div className="text-white text-center mt-20">Loading...</div>;

    return (
        <div className="min-h-screen bg-black text-white">
            <Header />
            <div className="p-8 max-w-7xl mx-auto">

                {/* Library Section */}
                <div className="mb-8 flex justify-between items-center">
                    <h2 className="text-xl font-bold">My Library</h2>
                    <button
                        onClick={() => setShowUpload(!showUpload)}
                        className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg font-semibold hover:opacity-90 transition-opacity"
                    >
                        {showUpload ? 'Cancel Upload' : 'New Upload'}
                    </button>
                </div>

                {showUpload && (
                    <div className="mb-8 p-6 bg-white/5 rounded-2xl border border-white/10">
                        <Upload onUploadSuccess={handleUploadSuccess} />
                    </div>
                )}

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {documents.map((doc) => (
                        <Link
                            to={`/workspace/${doc.id}`}
                            key={doc.id}
                            className="block p-6 bg-white/5 rounded-2xl border border-white/10 hover:bg-white/10 transition-all hover:scale-[1.02] group"
                        >
                            <div className="flex items-start justify-between mb-4">
                                <div className="p-3 bg-purple-500/20 rounded-xl text-purple-400 group-hover:bg-purple-500/30 transition-colors">
                                    <FileText className="w-8 h-8" />
                                </div>
                                <div className="flex flex-col items-end gap-2">
                                    <button
                                        onClick={(e) => handleDelete(e, doc.id)}
                                        className="p-2 hover:bg-red-500/20 text-white/40 hover:text-red-400 rounded-lg transition-colors"
                                        title="Delete Document"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                    <span className="text-xs text-white/40">
                                        {new Date(doc.uploaded_at).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>
                            <h3 className="font-bold text-lg mb-2 truncate" title={doc.file.split('/').pop()}>
                                {doc.file.split('/').pop()}
                            </h3>
                            <p className="text-sm text-white/60">
                                Click to open workspace
                            </p>
                        </Link>
                    ))}

                    {documents.length === 0 && !showUpload && (
                        <div className="col-span-full text-center py-20 text-white/40">
                            <p>No documents yet. Upload one to get started!</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
