import { useState, useEffect, useContext } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sparkles, Trophy, Star, LogOut, Menu } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import AuthContext from '../context/AuthContext';
import api from '../api';
import Leaderboard from './Leaderboard';

const Header = () => {
    const { user, logout } = useContext(AuthContext);
    const [profile, setProfile] = useState(null);
    const [showLeaderboard, setShowLeaderboard] = useState(false);
    const location = useLocation();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await api.get('/gamification/profile/');
                setProfile(response.data);
            } catch (error) {
                console.error('Error fetching profile:', error);
            }
        };
        if (user) fetchProfile();
    }, [user, location.pathname]); // Refresh on route change to update XP/Rank if needed

    if (!user) return null;

    return (
        <>
            <header className="h-20 border-b border-white/10 flex items-center justify-between px-8 bg-black/50 backdrop-blur-md sticky top-0 z-40">
                <div className="flex items-center gap-4">
                    <Link to="/dashboard" className="flex items-center gap-3 group">
                        {/* Logo - User can replace /logo.png in public folder */}
                        <img
                            src="/logo.png"
                            alt="BenchMate Logo"
                            className="h-10 w-auto object-contain"
                            onError={(e) => {
                                e.target.onerror = null;
                                e.target.style.display = 'none';
                                e.target.nextSibling.style.display = 'block';
                            }}
                        />
                        {/* Fallback Text Logo */}
                        <div className="hidden flex items-center gap-2">
                            <Sparkles className="w-8 h-8 text-purple-400" />
                            <span className="text-2xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
                                BenchMate
                            </span>
                        </div>
                    </Link>
                </div>

                {profile && (
                    <div className="flex items-center gap-6">
                        <button
                            onClick={() => setShowLeaderboard(!showLeaderboard)}
                            className={`flex items-center gap-2 px-4 py-2 rounded-full border transition-colors ${showLeaderboard ? 'bg-white/10 border-white/20' : 'bg-white/5 border-white/10 hover:bg-white/10'}`}
                        >
                            <Star className="w-5 h-5 text-yellow-400" />
                            <span className="font-bold text-white">{profile.xp} XP</span>
                        </button>

                        <Link to="/profile" className="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/10 hover:bg-white/10 transition-colors">
                            <Trophy className="w-5 h-5 text-purple-400" />
                            <span className="font-bold text-white">{profile.rank}</span>
                        </Link>

                        <div className="h-8 w-px bg-white/10 mx-2"></div>

                        <button
                            onClick={logout}
                            className="p-2 hover:bg-white/10 rounded-full transition-colors text-white/60 hover:text-white"
                            title="Logout"
                        >
                            <LogOut className="w-5 h-5" />
                        </button>
                    </div>
                )}
            </header>

            {/* Leaderboard Sidebar */}
            <AnimatePresence>
                {showLeaderboard && (
                    <>
                        {/* Backdrop */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setShowLeaderboard(false)}
                            className="fixed inset-0 bg-black/50 z-40"
                        />
                        {/* Sidebar */}
                        <motion.div
                            initial={{ x: '100%' }}
                            animate={{ x: 0 }}
                            exit={{ x: '100%' }}
                            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                            className="fixed right-0 top-0 h-full w-80 bg-[#0a0a0a] border-l border-white/10 z-50 shadow-2xl overflow-hidden flex flex-col"
                        >
                            <div className="p-4 border-b border-white/10 flex justify-between items-center">
                                <h3 className="font-bold text-lg text-white">Leaderboard</h3>
                                <button
                                    onClick={() => setShowLeaderboard(false)}
                                    className="p-2 hover:bg-white/10 rounded-lg text-white/60 hover:text-white"
                                >
                                    ✕
                                </button>
                            </div>
                            <div className="flex-1 overflow-y-auto p-4">
                                <Leaderboard />
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </>
    );
};

export default Header;
