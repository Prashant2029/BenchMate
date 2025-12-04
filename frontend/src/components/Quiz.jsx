import { useState } from 'react';
import api from '../api';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, Loader, CheckCircle, XCircle } from 'lucide-react';

const Quiz = ({ pdfId, onComplete }) => {
    const [quiz, setQuiz] = useState(null);
    const [loading, setLoading] = useState(false);
    const [answers, setAnswers] = useState({});
    const [showResults, setShowResults] = useState(false);
    const [numQuestions, setNumQuestions] = useState(5);
    const [topic, setTopic] = useState('');

    const generateQuiz = async () => {
        setLoading(true);
        setQuiz(null);
        setShowResults(false);
        setAnswers({});
        try {
            const response = await api.post('/core/generate/quiz/', {
                pdf_id: pdfId,
                num_questions: numQuestions,
                topic: topic
            });

            const quizData = JSON.parse(response.data.quiz);
            setQuiz(quizData);
            setAnswers({});
            setShowResults(false);
        } catch (error) {
            console.error('Quiz generation failed:', error);
            alert('Failed to generate quiz. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleAnswer = (questionIndex, answer) => {
        setAnswers({ ...answers, [questionIndex]: answer });
    };

    const submitQuiz = async () => {
        const score = calculateScore();
        try {
            await api.post('/core/submit/quiz/', {
                score: score,
                total_questions: quiz.questions.length
            });
            setShowResults(true);
            if (onComplete) onComplete();
        } catch (error) {
            console.error('Quiz submission failed:', error);
            alert('Failed to submit quiz score.');
            setShowResults(true); // Show results anyway
        }
    };

    const calculateScore = () => {
        if (!quiz) return 0;
        let correct = 0;
        quiz.questions.forEach((q, index) => {
            if (answers[index] === q.correct_answer) {
                correct++;
            }
        });
        return correct;
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
                        <Brain className="w-8 h-8 text-blue-400" />
                        <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                            Quiz
                        </h2>
                    </div>

                    {!quiz && (
                        <div className="flex flex-col gap-4 w-full md:w-auto">
                            <div className="flex gap-4">
                                <input
                                    type="text"
                                    placeholder="Topic (optional)"
                                    value={topic}
                                    onChange={(e) => setTopic(e.target.value)}
                                    className="bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white placeholder-white/40 focus:outline-none focus:border-blue-500"
                                />
                                <select
                                    value={numQuestions}
                                    onChange={(e) => setNumQuestions(Number(e.target.value))}
                                    className="bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                                >
                                    <option value={5} className="bg-gray-900">5 Questions</option>
                                    <option value={10} className="bg-gray-900">10 Questions</option>
                                    <option value={15} className="bg-gray-900">15 Questions</option>
                                </select>
                            </div>
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={generateQuiz}
                                disabled={loading}
                                className="px-6 py-3 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg font-semibold text-white shadow-lg hover:shadow-blue-500/50 transition-shadow disabled:opacity-50 flex items-center justify-center gap-2"
                            >
                                {loading ? (
                                    <>
                                        <Loader className="w-5 h-5 animate-spin" />
                                        Generating...
                                    </>
                                ) : (
                                    'Generate Quiz'
                                )}
                            </motion.button>
                        </div>
                    )}
                </div>

                {quiz && (
                    <div className="space-y-6">
                        <AnimatePresence mode="wait">
                            {quiz.questions.map((question, qIndex) => (
                                <motion.div
                                    key={qIndex}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: qIndex * 0.1 }}
                                    className="bg-white/5 rounded-xl p-6 border border-white/10"
                                >
                                    <h3 className="text-xl font-semibold mb-4 text-white/90">
                                        {qIndex + 1}. {question.question}
                                    </h3>

                                    <div className="space-y-3">
                                        {Object.entries(question.options).map(([key, value]) => {
                                            const isSelected = answers[qIndex] === key;
                                            const isCorrect = key === question.correct_answer;
                                            const showCorrectness = showResults && isSelected;

                                            return (
                                                <motion.button
                                                    key={key}
                                                    whileHover={{ scale: 1.02 }}
                                                    whileTap={{ scale: 0.98 }}
                                                    onClick={() => !showResults && handleAnswer(qIndex, key)}
                                                    disabled={showResults}
                                                    className={`w-full text-left p-4 rounded-lg border transition-all flex items-center justify-between ${showResults && isCorrect
                                                        ? 'bg-green-500/20 border-green-400'
                                                        : showCorrectness && !isCorrect
                                                            ? 'bg-red-500/20 border-red-400'
                                                            : isSelected
                                                                ? 'bg-blue-500/20 border-blue-400'
                                                                : 'bg-white/5 border-white/10 hover:border-white/30'
                                                        }`}
                                                >
                                                    <span className="text-white/80">
                                                        <strong className="text-white/90">{key}.</strong> {value}
                                                    </span>
                                                    {showResults && isCorrect && (
                                                        <CheckCircle className="w-5 h-5 text-green-400" />
                                                    )}
                                                    {showCorrectness && !isCorrect && (
                                                        <XCircle className="w-5 h-5 text-red-400" />
                                                    )}
                                                </motion.button>
                                            );
                                        })}
                                    </div>
                                </motion.div>
                            ))}
                        </AnimatePresence>

                        {!showResults ? (
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={submitQuiz}
                                disabled={Object.keys(answers).length !== quiz.questions.length}
                                className="w-full px-6 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg font-semibold text-white shadow-lg hover:shadow-blue-500/50 transition-shadow disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Submit Quiz
                            </motion.button>
                        ) : (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-xl p-6 border border-blue-400/30"
                            >
                                <div className="text-center">
                                    <h3 className="text-2xl font-bold mb-2">
                                        Score: {calculateScore()} / {quiz.questions.length}
                                    </h3>
                                    <p className="text-white/70">
                                        {calculateScore() === quiz.questions.length
                                            ? '🎉 Perfect score!'
                                            : calculateScore() >= quiz.questions.length * 0.7
                                                ? '👍 Great job!'
                                                : '📚 Keep studying!'}
                                    </p>
                                </div>
                            </motion.div>
                        )}
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default Quiz;
