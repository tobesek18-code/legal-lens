import React from 'react';
import { AlertTriangle, CheckCircle, Info, XCircle } from 'lucide-react';
interface AnalysisReportProps {
  report: string;
}
export default function AnalysisReport({ report }: AnalysisReportProps) {
  const formatReport = (text: string) => {
    const lines = text.split('\n');
    const sections: JSX.Element[] = [];
    let currentSection = '';
    let currentItems: string[] = [];
    const addSection = (title: string, items: string[], type: 'success' | 'warning' | 'error' | 'info' = 'info') => {
      if (items.length > 0) {
        const IconComponent = type === 'success' ? CheckCircle : type === 'warning' ? AlertTriangle : type === 'error' ? XCircle : Info;
        const colorClass = type === 'success' ? 'text-green-600' : type === 'warning' ? 'text-yellow-600' : type === 'error' ? 'text-red-600' : 'text-blue-600';
        const bgClass = type === 'success' ? 'bg-green-50 border-green-200' : type === 'warning' ? 'bg-yellow-50 border-yellow-200' : type === 'error' ? 'bg-red-50 border-red-200' : 'bg-blue-50 border-blue-200';
        sections.push(
          <div key={title} className={`mb-6 p-6 rounded-lg border ${bgClass}`} style={{ padding: '10px', clear: 'both', marginBottom: '20px', text_align: 'left' }}>
            <div className="flex items-center mb-4">
              <IconComponent className={`w-6 h-6 ${colorClass} mr-3`} />
              <h3 className="text-xl font-semibold text-gray-900">{title}</h3>
            </div>
            <ul className="space-y-4">
              {items.map((item, idx) => (
                <li key={idx} className="text-gray-700 leading-relaxed flex items-start text-base">
                  <span className="text-gray-400 mr-3 mt-1 text-lg">•</span>
                  <span className="flex-1 whitespace-pre-wrap">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        );
      }
    };
    lines.forEach((line) => {
      const trimmed = line.trim();
      if (trimmed.match(/^\d+\./) || trimmed.includes('Executive Summary') || trimmed.includes('Critical Violations') || trimmed.includes('Missing Mandatory') || trimmed.includes('Unfair or Risky') || trimmed.includes('Negotiation Suggestions') || trimmed.includes('Overall Risk Score') || trimmed.includes('Final Disclaimer')) {
        if (currentSection && currentItems.length > 0) {
          let sectionType: 'success' | 'warning' | 'error' | 'info' = 'info';
          if (currentSection.includes('Critical') || currentSection.includes('Violations')) sectionType = 'error';
          else if (currentSection.includes('Missing') || currentSection.includes('Unfair')) sectionType = 'warning';
          else if (currentSection.includes('Executive') || currentSection.includes('Overall Risk Score')) sectionType = 'success';
          addSection(currentSection, currentItems, sectionType);
        }
        currentSection = trimmed.replace(/^\d+\.\s*/, '').replace(/:$/, '');
        currentItems = [];
      } else if (trimmed && !trimmed.startsWith('-') && !trimmed.startsWith('•') && trimmed.length > 10) {
        if (currentSection) {
          currentItems.push(trimmed);
        }
      } else if ((trimmed.startsWith('-') || trimmed.startsWith('•')) && trimmed.length > 2) {
        if (currentSection) {
          currentItems.push(trimmed.substring(1).trim());
        }
      }
    });
    if (currentSection && currentItems.length > 0) {
      addSection(currentSection, currentItems, 'info');
    }
    return sections.length > 0 ? sections : (
      <div className="p-6 bg-gray-50 rounded-lg border">
        <pre className="text-gray-700 whitespace-pre-wrap font-sans text-sm leading-relaxed" style={{ lineHeight: '1.8' }}>
          {text.split('\n').join('\n\n')}
        </pre>
      </div>
    );
  };
  return (
    <div className="space-y-6">
      {formatReport(report)}
    </div>
  );
}
