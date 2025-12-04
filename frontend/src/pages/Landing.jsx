import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Sparkles, Brain, Layers, Trophy, ArrowRight } from 'lucide-react';

const Landing = () => {
    return (
        <div className="min-h-screen bg-black text-white overflow-hidden">
            {/* Navbar */}
            <nav className="p-6 flex justify-between items-center max-w-7xl mx-auto">
                <div className="flex items-center gap-2">
                    <Sparkles className="w-8 h-8 text-purple-400" />
                    <span className="text-xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                        BenchMate
                    </span>
                </div>
                <div className="flex gap-4">
                    <Link to="/login" className="px-4 py-2 hover:text-purple-400 transition-colors">
                        Login
                    </Link>
                    <Link
                        to="/register"
                        className="px-4 py-2 bg-white text-black rounded-full font-semibold hover:bg-gray-200 transition-colors"
                    >
                        Get Started
                    </Link>
                </div>
            </nav>

            {/* Hero Section */}
            <div className="max-w-7xl mx-auto px-6 py-20 text-center relative">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-purple-500/20 rounded-full blur-[100px] -z-10" />

                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-6xl md:text-8xl font-bold mb-8 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent"
                >
                    AI-Powered Study <br /> Assistant for Students
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="text-xl text-white/60 mb-12 max-w-2xl mx-auto"
                >
                    Upload any course book or document. Generate quizzes, flashcards, and chat with your content instantly. Gamify your learning journey.
                </motion.p>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="flex justify-center gap-4"
                >
                    <Link
                        to="/register"
                        className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full font-bold text-lg hover:shadow-lg hover:shadow-purple-500/50 transition-all flex items-center gap-2"
                    >
                        Start Learning Now <ArrowRight className="w-5 h-5" />
                    </Link>
                </motion.div>
            </div>

            {/* Features */}
            <div className="max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-3 gap-8">
                <FeatureCard
                    icon={<Brain className="w-8 h-8 text-blue-400" />}
                    title="AI Quizzes"
                    description="Generate smart quizzes from your documents. Test your knowledge and earn XP."
                    delay={0.6}
                />
                <FeatureCard
                    icon={<Layers className="w-8 h-8 text-emerald-400" />}
                    title="Flashcards"
                    description="Create study sets instantly. Perfect for memorizing definitions and concepts."
                    delay={0.7}
                />
                <FeatureCard
                    icon={<Trophy className="w-8 h-8 text-yellow-400" />}
                    title="Gamification"
                    description="Level up, earn ranks, and compete on the leaderboard. Make studying fun."
                    delay={0.8}
                />
            </div>
        </div>
    );
};

const FeatureCard = ({ icon, title, description, delay }) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay }}
        className="bg-white/5 p-8 rounded-2xl border border-white/10 hover:bg-white/10 transition-colors"
    >
        <div className="mb-4">{icon}</div>
        <h3 className="text-xl font-bold mb-2">{title}</h3>
        <p className="text-white/60">{description}</p>
    </motion.div>
);

export default Landing;
