'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { pagesAPI } from '@/utils/api';

export default function TermsPage() {
  const [content, setContent] = useState<string>('');
  const [title, setTitle] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPageContent();
  }, []);

  const loadPageContent = async () => {
    try {
      const response = await pagesAPI.getPage('terms');
      setTitle(response.title);
      setContent(response.content);
    } catch (err) {
      console.error('Failed to load page content:', err);
      // Fallback content
      setTitle('Terms & Conditions');
      setContent(`
#### 1. Service Description
LegaLens provides **document review services only**. This is NOT a substitute for professional legal advice.
Our AI analyzes rental agreements for potential compliance issues with local housing regulations.

#### 2. User Responsibilities
- Users are solely responsible for reviewing AI findings with a qualified attorney
- Users must not rely on our analysis as legal advice
- Users acknowledge all compliance reviews are for informational purposes only

#### 3. Liability Limitation
LegaLens shall not be liable for any damages, losses, or consequences arising from the use of our service.
Professional legal consultation is required for legal decisions.

#### 4. Intellectual Property
All content, analysis methods, and reports are proprietary to LegaLens.

#### 5. Modifications
We reserve the right to modify terms at any time. Continued use implies acceptance.
      `);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex justify-center items-center min-h-[400px]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-6">
        <Link
          href="/"
          className="inline-flex items-center text-gray-600 hover:text-primary transition-colors"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back Home
        </Link>
      </div>

      <div className="card">
        <h1 className="text-3xl font-bold text-black mb-6">📋 {title}</h1>
        <div className="prose prose-gray max-w-none">
          {content.split('\n').map((line, index) => {
            if (line.startsWith('####')) {
              return (
                <h4 key={index} className="text-xl font-semibold text-black mt-6 mb-3">
                  {line.replace('####', '').trim()}
                </h4>
              );
            } else if (line.startsWith('-')) {
              return (
                <li key={index} className="text-gray-700 ml-6 mb-2">
                  {line.replace('-', '').trim()}
                </li>
              );
            } else if (line.trim() === '') {
              return <br key={index} />;
            } else {
              return (
                <p key={index} className="text-gray-700 mb-3 leading-relaxed">
                  {line}
                </p>
              );
            }
          })}
        </div>
      </div>
    </div>
  );
}
