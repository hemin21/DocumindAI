import { useEffect, useState } from 'react';
import { api } from '../services/api';
import { ArrowLeft, ExternalLink, Calendar } from 'lucide-react';

interface DocDetailProps {
  docId: string;
  onBack: () => void;
}

export const DocumentDetail = ({ docId, onBack }: DocDetailProps) => {
  const [doc, setDoc] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getDocument(docId)
      .then(setDoc)
      .catch((err) => {
        console.error("Failed to load document:", err);
      })
      .finally(() => setLoading(false));
  }, [docId]);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Loading document details...</div>;
  }

  if (!doc) {
    return (
      <div className="p-8 text-center text-red-500 bg-white rounded-xl border border-red-200">
        Document ID <code className="font-mono">{docId}</code> was not found.
        <button onClick={onBack} className="block mx-auto mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium">Return to Search</button>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <button
        onClick={onBack}
        className="inline-flex items-center gap-1.5 text-sm font-medium text-slate-600 hover:text-indigo-600 transition cursor-pointer"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Search Results
      </button>

      <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-xs space-y-6">
        <div className="flex flex-wrap items-center gap-3">
          <span className="text-xs font-mono font-semibold px-2.5 py-1 bg-indigo-50 text-indigo-700 border border-indigo-100 rounded-md">
            ID: {doc.doc_id || docId}
          </span>
          {doc.metadata?.year && (
            <span className="inline-flex items-center gap-1 text-xs text-slate-500 px-2 py-0.5 bg-slate-100 rounded">
              <Calendar className="w-3 h-3" /> Year {doc.metadata.year}
            </span>
          )}
          {doc.metadata?.url && (
            <a
              href={doc.metadata.url}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1 text-xs text-indigo-600 hover:underline"
            >
              External Reference <ExternalLink className="w-3 h-3" />
            </a>
          )}
        </div>

        <h1 className="text-2xl font-bold text-slate-900 leading-snug">
          {doc.title || 'Untitled Research Document'}
        </h1>

        <div className="pt-4 border-t border-slate-100">
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
            Full Document Text / Abstract
          </h3>
          <p className="text-base text-slate-700 leading-relaxed whitespace-pre-line">
            {doc.text || "No abstract text available for this record."}
          </p>
        </div>
      </div>
    </div>
  );
};
