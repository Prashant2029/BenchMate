import { useState } from 'react';
import api from '../api';
import { motion } from 'framer-motion';
import { Upload as UploadIcon, FileText, Loader } from 'lucide-react';

const Upload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const droppedFile = e.dataTransfer.files[0];
            if (droppedFile.type === 'application/pdf') {
                setFile(droppedFile);
            } else {
                alert('Please upload a PDF file');
            }
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            if (selectedFile.type === 'application/pdf') {
                setFile(selectedFile);
            } else {
                alert('Please upload a PDF file');
            }
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await api.post('/core/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            onUploadSuccess(response.data);
            setFile(null);
        } catch (error) {
            console.error('Upload failed:', error);
            const errorMessage = error.response?.data?.error || 'Upload failed. Please try again.';
            alert(errorMessage);
        } finally {
            setUploading(false);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-2xl mx-auto"
        >
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
                <div className="flex items-center gap-3 mb-6">
                    <FileText className="w-8 h-8 text-purple-400" />
                    <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                        Upload PDF
                    </h2>
                </div>

                <div
                    className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all ${dragActive
                        ? 'border-purple-400 bg-purple-500/20'
                        : 'border-white/30 hover:border-purple-400/50'
                        }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    {!file && (
                        <input
                            type="file"
                            accept=".pdf"
                            onChange={handleChange}
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                            disabled={uploading}
                        />
                    )}

                    <UploadIcon className="w-16 h-16 mx-auto mb-4 text-purple-400/70" />

                    {file ? (
                        <div className="space-y-4 relative z-10">
                            <p className="text-lg text-white/90 font-medium">{file.name}</p>
                            <p className="text-sm text-white/60">
                                {(file.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={handleUpload}
                                disabled={uploading}
                                className="px-8 py-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg font-semibold text-white shadow-lg hover:shadow-purple-500/50 transition-shadow disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 mx-auto"
                            >
                                {uploading ? (
                                    <>
                                        <Loader className="w-5 h-5 animate-spin" />
                                        Uploading...
                                    </>
                                ) : (
                                    'Upload & Analyze'
                                )}
                            </motion.button>
                        </div>
                    ) : (
                        <div>
                            <p className="text-lg text-white/70 mb-2">
                                Drag and drop your PDF here, or click to browse
                            </p>
                            <p className="text-sm text-white/50">
                                PDF files only, up to 10MB
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
};

export default Upload;
