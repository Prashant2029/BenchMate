import { useState } from 'react';
import api from '../api';
import { motion, AnimatePresence } from 'framer-motion';
import { Layers, Loader, ChevronLeft, ChevronRight } from 'lucide-react';

const Flashcards = ({ pdfId }) => {
    const [flashcards, setFlashcards] = useState(null);
    const [loading, setLoading] = useState(false);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isFlipped, setIsFlipped] = useState(false);
    const [numCards, setNumCards] = useState(10);

    const generateFlashcards = async () => {
        setLoading(true);
        try {
            const response = await api.post('/core/generate/flashcards/', {
                pdf_id: pdfId,
                num_cards: numCards,
            });

            const flashcardsData = JSON.parse(response.data.flashcards);
            setFlashcards(flashcardsData);
            setCurrentIndex(0);
            setIsFlipped(false);
        } catch (error) {
            console.error('Flashcard generation failed:', error);
            alert('Failed to generate flashcards. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleFlip = () => {
        setIsFlipped(!isFlipped);
    };

    const handleNext = () => {
        if (currentIndex < flashcards.flashcards.length - 1) {
            setCurrentIndex(currentIndex + 1);
            setIsFlipped(false);
        }
    };

    const handlePrev = () => {
        if (currentIndex > 0) {
            setCurrentIndex(currentIndex - 1);
            setIsFlipped(false);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-4xl mx-auto"
        >
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                        <Layers className="w-8 h-8 text-emerald-400" />
                        <h2 className="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
                            Flashcards
                        </h2>
                    </div>

                    {!flashcards && (
                        <div className="flex flex-col gap-4 w-full md:w-auto">
                            <select
                                value={numCards}
                                onChange={(e) => setNumCards(Number(e.target.value))}
                                className="bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-500"
                            >
                                <option value={5} className="bg-gray-900">5 Cards</option>
                                <option value={10} className="bg-gray-900">10 Cards</option>
                                <option value={15} className="bg-gray-900">15 Cards</option>
                                <option value={20} className="bg-gray-900">20 Cards</option>
                            </select>
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={generateFlashcards}
                                disabled={loading}
                                className="px-6 py-3 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-lg font-semibold text-white shadow-lg hover:shadow-emerald-500/50 transition-shadow disabled:opacity-50 flex items-center justify-center gap-2"
                            >
                                {loading ? (
                                    <>
                                        <Loader className="w-5 h-5 animate-spin" />
                                        Generating...
                                    </>
                                ) : (
                                    'Generate Flashcards'
                                )}
                            </motion.button>
                        </div>
                    )}
                </div>

                {flashcards && flashcards.flashcards && flashcards.flashcards.length > 0 && (
                    <div className="space-y-6">
                        <div className="text-center text-white/60 text-sm mb-4">
                            Card {currentIndex + 1} of {flashcards.flashcards.length}
                        </div>

                        <div className="perspective-1000">
                            <motion.div
                                className="relative w-full h-80 cursor-pointer"
                                onClick={handleFlip}
                                style={{ perspective: '1000px' }}
                            >
                                <motion.div
                                    className="relative w-full h-full"
                                    initial={false}
                                    animate={{ rotateY: isFlipped ? 180 : 0 }}
                                    transition={{ duration: 0.6, type: 'spring' }}
                                    style={{ transformStyle: 'preserve-3d' }}
                                >
                                    {/* Front */}
                                    <div
                                        className="absolute w-full h-full bg-gradient-to-br from-emerald-500/20 to-teal-500/20 rounded-2xl p-8 flex items-center justify-center border border-emerald-400/30"
                                        style={{ backfaceVisibility: 'hidden' }}
                                    >
                                        <div className="text-center">
                                            <p className="text-sm text-emerald-400 mb-4 uppercase tracking-wide">
                                                Question
                                            </p>
                                            <p className="text-2xl font-semibold text-white">
                                                {flashcards.flashcards[currentIndex].front}
                                            </p>
                                            <p className="text-sm text-white/50 mt-8">
                                                Click to reveal answer
                                            </p>
                                        </div>
                                    </div>

                                    {/* Back */}
                                    <div
                                        className="absolute w-full h-full bg-gradient-to-br from-teal-500/20 to-emerald-500/20 rounded-2xl p-8 flex items-center justify-center border border-teal-400/30"
                                        style={{
                                            backfaceVisibility: 'hidden',
                                            transform: 'rotateY(180deg)',
                                        }}
                                    >
                                        <div className="text-center">
                                            <p className="text-sm text-teal-400 mb-4 uppercase tracking-wide">
                                                Answer
                                            </p>
                                            <p className="text-xl text-white/90">
                                                {flashcards.flashcards[currentIndex].back}
                                            </p>
                                            <p className="text-sm text-white/50 mt-8">
                                                Click to flip back
                                            </p>
                                        </div>
                                    </div>
                                </motion.div>
                            </motion.div>
                        </div>

                        <div className="flex items-center justify-between">
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={handlePrev}
                                disabled={currentIndex === 0}
                                className="px-6 py-3 bg-white/10 rounded-lg font-semibold text-white border border-white/20 hover:bg-white/20 transition-colors disabled:opacity-30 disabled:cursor-not-allowed flex items-center gap-2"
                            >
                                <ChevronLeft className="w-5 h-5" />
                                Previous
                            </motion.button>

                            <div className="flex gap-2">
                                {flashcards.flashcards.map((_, index) => (
                                    <div
                                        key={index}
                                        className={`w-2 h-2 rounded-full transition-all ${index === currentIndex
                                            ? 'bg-emerald-400 w-8'
                                            : 'bg-white/30'
                                            }`}
                                    />
                                ))}
                            </div>

                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={handleNext}
                                disabled={currentIndex === flashcards.flashcards.length - 1}
                                className="px-6 py-3 bg-white/10 rounded-lg font-semibold text-white border border-white/20 hover:bg-white/20 transition-colors disabled:opacity-30 disabled:cursor-not-allowed flex items-center gap-2"
                            >
                                Next
                                <ChevronRight className="w-5 h-5" />
                            </motion.button>
                        </div>
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default Flashcards;
