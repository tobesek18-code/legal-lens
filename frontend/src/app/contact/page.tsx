'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, Mail, Clock } from 'lucide-react';
import { pagesAPI } from '@/utils/api';

export default function ContactPage() {
  const [content, setContent] = useState<string>('');
  const [title, setTitle] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPageContent();
  }, []);

  const loadPageContent = async () => {
    try {
      const response = await pagesAPI.getPage('contact');
      setTitle(response.title);
      setContent(response.content);
    } catch (err) {
      console.error('Failed to load page content:', err);
      // Fallback content
      setTitle('Contact Us');
      setContent(`
Have questions about LegaLens? We'd love to hear from you.

**Email:** contact@zartechai.com

**Hours:** Monday - Friday, 9AM - 5PM NZST

**Response Time:** We typically respond within 24 hours.

**For urgent legal matters:** Please contact a licensed attorney in your jurisdiction.
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
        <h1 className="text-3xl font-bold text-black mb-6">📧 {title}</h1>

        <div className="space-y-6">
          {content.split('\n').map((line, index) => {
            if (line.includes('**Email:**')) {
              return (
                <div key={index} className="flex items-center p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <Mail className="w-6 h-6 text-primary mr-3" />
                  <div>
                    <p className="text-black font-medium">Email</p>
                    <p className="text-gray-600">contact@zartechai.com</p>
                  </div>
                </div>
              );
            } else if (line.includes('**Hours:**')) {
              return (
                <div key={index} className="flex items-center p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <Clock className="w-6 h-6 text-primary mr-3" />
                  <div>
                    <p className="text-black font-medium">Business Hours</p>
                    <p className="text-gray-600">Monday - Friday, 9AM - 5PM NZST</p>
                  </div>
                </div>
              );
            } else if (line.includes('**Response Time:**')) {
              return (
                <div key={index} className="flex items-start p-4 bg-green-50 border border-green-200 rounded-lg">
                  <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center mr-3 mt-0.5">
                    <span className="text-white text-sm">⏱️</span>
                  </div>
                  <div>
                    <p className="text-black font-medium">Response Time</p>
                    <p className="text-gray-600">We typically respond within 24 hours</p>
                  </div>
                </div>
              );
            } else if (line.includes('**For urgent legal matters:**')) {
              return (
                <div key={index} className="flex items-start p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <div className="w-6 h-6 bg-yellow-500 rounded-full flex items-center justify-center mr-3 mt-0.5">
                    <span className="text-white text-sm">⚠️</span>
                  </div>
                  <div>
                    <p className="text-yellow-700 font-medium">Important Notice</p>
                    <p className="text-gray-600">For urgent legal matters, please contact a licensed attorney in your jurisdiction.</p>
                  </div>
                </div>
              );
            } else if (line.trim() === '') {
              return <br key={index} />;
            } else if (line.trim()) {
              return (
                <p key={index} className="text-gray-700 leading-relaxed">
                  {line}
                </p>
              );
            }
            return null;
          })}
        </div>
      </div>
    </div>
  );
}
