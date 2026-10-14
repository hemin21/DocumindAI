import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { CustomDocumentItem } from '../types';
import { Upload, FileText, Trash2, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

export const PdfUploadPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [documents, setDocuments] = useState<CustomDocumentItem[]>([]);
  const [loadingDocs, setLoadingDocs] = useState(true);

  const loadDocs = async () => {
    try {
      setLoadingDocs(true);
      const docs = await api.getCustomDocuments();
      setDocuments(docs);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingDocs(false);
    }
  };

  useEffect(() => {
    loadDocs();
  }, []);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setMessage(null);
    try {
      const res = await api.uploadPdf(file);
      setMessage({
        type: 'success',
        text: `Successfully indexed ${res.filename}! Extracted ${res.page_count} pages and created ${res.chunks_created} searchable passages.`
      });
      setFile(null);
      loadDocs();
    } catch (err: any) {
      setMessage({ type: 'error', text: err.message || 'Upload failed' });
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (docId: string) => {
    try {
      await api.deleteCustomDocument(docId);
      loadDocs();
    } catch (err: any) {
      alert(err.message || 'Failed to delete');
    }
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div>
        <h2 className="text-2xl font-bold text-slate-900">Custom PDF Upload & Passage Indexing</h2>
        <p className="text-sm text-slate-500 mt-1">
          Upload any research paper or document in PDF format. DocuMind uses PyMuPDF to extract text and splits it into overlapping passages.
        </p>
      </div>

      {/* Upload Box */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
        <form onSubmit={handleUpload} className="space-y-4">
          <div className="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:border-indigo-400 transition bg-slate-50/50">
            <Upload className="w-10 h-10 text-indigo-600 mx-auto mb-3" />
            <p className="text-sm font-medium text-slate-700">
              Select a research document or PDF to index
            </p>
            <p className="text-xs text-slate-400 mt-1 mb-4">
              Supports standard PDFs. Text is parsed page-by-page.
            </p>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer"
            />
          </div>

          {file && (
            <div className="flex items-center justify-between text-xs text-slate-600 bg-slate-100 px-4 py-2 rounded-lg">
              <span>Selected: <strong>{file.name}</strong> ({(file.size / 1024).toFixed(1)} KB)</span>
              <button
                type="submit"
                disabled={uploading}
                className="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-md shadow-xs transition flex items-center gap-1.5 cursor-pointer disabled:bg-indigo-300"
              >
                {uploading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Upload className="w-3.5 h-3.5" />}
                Process & Index PDF
              </button>
            </div>
          )}
        </form>

        {message && (
          <div className={`mt-4 p-4 rounded-xl text-sm flex items-center gap-2 ${
            message.type === 'success' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-red-50 text-red-800 border border-red-200'
          }`}>
            {message.type === 'success' ? <CheckCircle className="w-4 h-4 text-emerald-600" /> : <AlertCircle className="w-4 h-4 text-red-600" />}
            {message.text}
          </div>
        )}
      </div>

      {/* Uploaded Documents List */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <h3 className="font-bold text-slate-900 text-sm">Indexed Custom PDF Documents</h3>
          <span className="text-xs text-slate-500">{documents.length} document(s) uploaded</span>
        </div>

        {loadingDocs ? (
          <div className="p-8 text-center text-slate-400 text-sm">Loading uploaded documents...</div>
        ) : documents.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-sm">
            No custom documents uploaded yet. Upload a PDF above to begin.
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {documents.map((d) => (
              <div key={d.id} className="p-4 flex items-center justify-between hover:bg-slate-50 transition">
                <div className="flex items-center gap-3">
                  <FileText className="w-5 h-5 text-indigo-600" />
                  <div>
                    <div className="text-sm font-bold text-slate-900">{d.filename}</div>
                    <div className="text-xs text-slate-400 mt-0.5">
                      {d.page_count} pages • {d.total_chunks} passages • Uploaded {d.uploaded_at}
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(d.id)}
                  className="text-slate-400 hover:text-red-600 p-2 rounded-lg hover:bg-red-50 transition cursor-pointer"
                  title="Delete Document"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
