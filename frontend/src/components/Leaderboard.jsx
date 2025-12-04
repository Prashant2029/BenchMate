import { useState, useEffect } from 'react';
import api from '../api';
import { motion } from 'framer-motion';
import { Trophy, Medal, Crown } from 'lucide-react';

const Leaderboard = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchLeaderboard = async () => {
            try {
                const response = await api.get('/gamification/leaderboard/');
                setUsers(response.data);
            } catch (error) {
                console.error('Failed to fetch leaderboard:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchLeaderboard();
    }, []);

    const getRankIcon = (index) => {
        switch (index) {
            case 0: return <Crown className="w-6 h-6 text-yellow-400" />;
            case 1: return <Medal className="w-6 h-6 text-gray-300" />;
            case 2: return <Medal className="w-6 h-6 text-amber-600" />;
            default: return <span className="font-bold text-white/50">#{index + 1}</span>;
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 w-full max-w-md"
        >
            <div className="flex items-center gap-3 mb-6">
                <Trophy className="w-6 h-6 text-yellow-400" />
                <h2 className="text-xl font-bold text-white">Leaderboard</h2>
            </div>

            <div className="space-y-3">
                {users.map((user, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="flex items-center justify-between p-3 bg-white/5 rounded-xl border border-white/5 hover:bg-white/10 transition-colors"
                    >
                        <div className="flex items-center gap-4">
                            <div className="w-8 flex justify-center">
                                {getRankIcon(index)}
                            </div>
                            <div>
                                <p className="font-semibold text-white">{user.username}</p>
                                <p className="text-xs text-white/50">{user.rank}</p>
                            </div>
                        </div>
                        <div className="text-right">
                            <p className="font-bold text-purple-400">{user.xp} XP</p>
                            <p className="text-xs text-white/50">Lvl {user.level}</p>
                        </div>
                    </motion.div>
                ))}
                {loading && <p className="text-center text-white/50">Loading...</p>}
            </div>
        </motion.div>
    );
};

export default Leaderboard;
