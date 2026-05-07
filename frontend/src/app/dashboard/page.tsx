'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { FileText, Download, LogOut, Upload, AlertCircle, CheckCircle } from 'lucide-react';
import AnalysisReport from '@/components/AnalysisReport';
import { analysisAPI } from '@/utils/api';

export default function Dashboard() {
  const [jurisdictions, setJurisdictions] = useState<string[]>([]);
  const [selectedJurisdiction, setSelectedJurisdiction] = useState('');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<string | null>(null);
  const [error, setError] = useState('');
  const [pdfGenerated, setPdfGenerated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/');
      return;
    }

    // Load jurisdictions
    loadJurisdictions();
  }, [router]);

  const loadJurisdictions = async () => {
    try {
      const response = await analysisAPI.getJurisdictions();
      setJurisdictions(response.jurisdictions);
      if (response.jurisdictions.length > 0) {
        setSelectedJurisdiction(response.jurisdictions[0]);
      }
    } catch (err) {
      console.error('Failed to load jurisdictions:', err);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setUploadedFile(file);
      setError('');
    } else {
      setError('Please select a valid PDF file.');
      setUploadedFile(null);
    }
  };

  const handleAnalysis = async () => {
    if (!uploadedFile || !selectedJurisdiction) return;

    setIsAnalyzing(true);
    setError('');
    setAnalysisResult(null);
    setPdfGenerated(false);

    try {
      const response = await analysisAPI.analyzeDocument(selectedJurisdiction, uploadedFile);
      setAnalysisResult(response.report);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!analysisResult) return;

    try {
      const pdfBlob = await analysisAPI.generatePDF({ report: analysisResult });
      const url = window.URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Lease_Report.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      setPdfGenerated(true);
    } catch (err) {
      setError('Failed to generate PDF. Please try again.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    router.push('/');
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header */}

      <div className="flex justify-between items-center gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold text-black mb-2">
              📑 Analysis Dashboard
            </h1>

            <p className="text-gray-600 text-sm font-medium text-black mb-3">
              Upload your lease agreement for AI-powered compliance review
            </p>
          </div>

          <div>
            <button
              onClick={handleLogout}
              className="btn-custom bg-red-600 hover:bg-red-700"
            >
              <LogOut />
              Logouts
            </button>
          </div>
      </div>



      {/* Jurisdiction Selection */}
      <div className="card mb-6">
        <label htmlFor="jurisdiction" className="block text-sm font-medium text-black mb-3">
          Property Jurisdiction
        </label>
        <select
          id="jurisdiction"
          value={selectedJurisdiction}
          onChange={(e) => setSelectedJurisdiction(e.target.value)}
          className="input-primary w-full"
        >
          {jurisdictions.map((jurisdiction) => (
            <option key={jurisdiction} value={jurisdiction}>
              {jurisdiction}
            </option>
          ))}
        </select>
      </div>

      {/* File Upload */}
      <div className="card mb-6">
        <label className="block text-sm font-medium text-black mb-3">
          Upload Lease Agreement (PDF)
        </label>
        <div className="border-2 border-dashed border-gray-300 rounded-xl p-10 text-center hover:border-primary hover:bg-blue-50/30 transition-all duration-200 cursor-pointer">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            className="hidden"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-black font-medium mb-2">
              {uploadedFile ? uploadedFile.name : 'Click to upload PDF'}
            </p>
            <p className="text-gray-500 text-sm">
              Only PDF files are supported
            </p>
          </label>
        </div>
      </div>


       {/* Analysis Button */}
       {!analysisResult && (
         <div className="mb-8">
           <button className="btn-primary w-full py-3 text-lg font-medium shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200"
             onClick={handleAnalysis}
             disabled={!uploadedFile || !selectedJurisdiction || isAnalyzing}
           >
             {isAnalyzing ? (
               <div className="flex items-center justify-center">
                 <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                 Reviewing tenancy agreement...
               </div>
             ) : (
               <>
                 <FileText  className="w-5 h-5 mr-2" />
                 Run AI Legal Audit
               </>
             )}
           </button>
         </div>
       )}

      {/* Analysis Results */}
      {analysisResult && (
        <div className="card">

        <div className="flex justify-between items-center gap-4 mb-8">
          <div className="flex items-center gap-4">
            <CheckCircle className="w-6 h-6 text-green-500" />
            <h2 className="text-xl font-bold text-black">
              Analysis Complete
            </h2>
          </div>

          <div className="flex items-center">
            <button
              onClick={handleDownloadPDF}
              className="btn-primary flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Download PDF Report
            </button>
          </div>
        </div>


          <div className="max-h-96 overflow-y-auto">
            <AnalysisReport report={analysisResult} />
          </div>
        </div>
      )}
    </div>
  );
}
