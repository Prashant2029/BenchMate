import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import Quiz from '../components/Quiz';
import Header from '../components/Header';

const QuizPage = () => {
    const { pdfId } = useParams();
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-black text-white">
            <Header />
            <div className="p-8 max-w-4xl mx-auto">
                <button
                    onClick={() => navigate(`/workspace/${pdfId}`)}
                    className="flex items-center gap-2 text-white/60 hover:text-white mb-8 transition-colors"
                >
                    <ArrowLeft className="w-5 h-5" /> Back to Workspace
                </button>
                <Quiz pdfId={pdfId} onComplete={() => { }} />
            </div>
        </div>
    );
};

export default QuizPage;
