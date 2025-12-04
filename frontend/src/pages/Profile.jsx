import { useState, useEffect } from 'react';
import api from '../api';
import { motion } from 'framer-motion';
import { Trophy, Star, Calendar, History, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';

const Profile = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await api.get('/gamification/profile/');
                setProfile(response.data);
            } catch (error) {
                console.error('Failed to fetch profile:', error);
                setError('Failed to load profile. Please try refreshing.');
            } finally {
                setLoading(false);
            }
        };
        fetchProfile();
    }, []);

    if (loading) return <div className="text-white text-center mt-20">Loading...</div>;

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

    if (!profile) return <div className="text-white text-center mt-20">Error loading profile</div>;

    return (
        <div className="min-h-screen bg-black text-white">
            <Header />
            <div className="p-8 max-w-4xl mx-auto">
                <Link to="/dashboard" className="flex items-center gap-2 text-white/60 hover:text-white mb-8 transition-colors">
                    <ArrowLeft className="w-5 h-5" /> Back to Dashboard
                </Link>

                {/* Header Stats */}
                <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-2xl p-8 border border-purple-500/30 mb-8">
                    <div className="flex items-center gap-6 mb-6">
                        <div className="w-20 h-20 rounded-full bg-purple-500 flex items-center justify-center text-3xl font-bold">
                            {profile.username[0].toUpperCase()}
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold">{profile.username}</h1>
                            <p className="text-purple-400 font-semibold">{profile.rank}</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                        <StatCard icon={<Star className="text-yellow-400" />} label="Total XP" value={profile.xp} />
                        <StatCard icon={<Calendar className="text-blue-400" />} label="Weekly XP" value={profile.weekly_xp} />
                        <StatCard icon={<Trophy className="text-purple-400" />} label="Level" value={profile.level} />
                    </div>
                </div>

                <div className="grid md:grid-cols-2 gap-8">
                    {/* Achievements */}
                    <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
                        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                            <Trophy className="w-5 h-5 text-yellow-400" /> Achievements
                        </h2>
                        {profile.achievements.length > 0 ? (
                            <div className="space-y-4">
                                {profile.achievements.map((ach, i) => (
                                    <div key={i} className="flex items-center gap-4 p-3 bg-white/5 rounded-xl">
                                        <div className="text-2xl">{ach.icon === 'trophy' ? '🏆' : '⭐'}</div>
                                        <div>
                                            <p className="font-bold">{ach.name}</p>
                                            <p className="text-xs text-white/60">{ach.description}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-white/40 text-center py-8">No achievements yet. Keep learning!</p>
                        )}
                    </div>

                    {/* Quiz History */}
                    <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
                        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                            <History className="w-5 h-5 text-blue-400" /> Recent Activity
                        </h2>
                        {profile.quiz_history.length > 0 ? (
                            <div className="space-y-4 max-h-[400px] overflow-y-auto custom-scrollbar">
                                {profile.quiz_history.slice().reverse().map((quiz, i) => (
                                    <div key={i} className="flex justify-between items-center p-3 bg-white/5 rounded-xl">
                                        <div>
                                            <p className="font-semibold">Quiz Completed</p>
                                            <p className="text-xs text-white/40">{new Date(quiz.created_at).toLocaleDateString()}</p>
                                        </div>
                                        <div className="text-right">
                                            <p className="text-green-400 font-bold">+{quiz.xp_earned} XP</p>
                                            <p className="text-xs text-white/60">{quiz.score}/{quiz.total_questions}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-white/40 text-center py-8">No quizzes taken yet.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

const StatCard = ({ icon, label, value }) => (
    <div className="bg-black/20 rounded-xl p-4 flex items-center gap-3">
        <div className="p-2 bg-white/5 rounded-lg">{icon}</div>
        <div>
            <p className="text-sm text-white/60">{label}</p>
            <p className="text-xl font-bold">{value}</p>
        </div>
    </div>
);

export default Profile;
