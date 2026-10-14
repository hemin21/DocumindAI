import { useState } from 'react';
import { api } from '../services/api';
import type { SearchResponse, SearchResultItem } from '../types';
import { Search, Loader2, Clock, ChevronRight, Sparkles } from 'lucide-react';

interface SearchProps {
  onSelectDoc: (docId: string) => void;
}

export const SearchPage = ({ onSelectDoc }: SearchProps) => {
  const [query, setQuery] = useState('what is a transformer neural network?');
  const [model, setModel] = useState('semantic');
  const [topK, setTopK] = useState(10);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<SearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const sampleQuestions = [
    'what is a transformer neural network?',
    'how does gradient descent work in deep learning?',
    'what are generative adversarial networks?',
    'how to perform reinforcement learning?',
    'what is attention mechanism in natural language processing?',
    'convolutional neural networks for image classification'
  ];

  const handleSearch = async (e?: React.FormEvent, explicitQuery?: string) => {
    if (e) e.preventDefault();
    const q = (explicitQuery !== undefined ? explicitQuery : query).trim();
    if (!q) return;

    setLoading(true);
    setError(null);
    try {
      const data = await api.search(q, model, topK);
      setResponse(data);
    } catch (err: any) {
      setError(err.message || 'Search execution failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Search Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
        <h2 className="text-xl font-bold text-slate-900 mb-1">
          AI & Machine Learning Research Search & Question Answering
        </h2>
        <p className="text-sm text-slate-500 mb-4">
          Ask questions across 25,657 AI papers. DocuMind extracts direct research answers and ranks relevant scientific documents.
        </p>

        <form onSubmit={handleSearch} className="space-y-4">
          <div className="relative">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask an AI question (e.g. what is a transformer? or how does gradient descent work?)"
              className="w-full pl-11 pr-28 py-3.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition text-base"
            />
            <Search className="w-5 h-5 text-slate-400 absolute left-3.5 top-4" />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-2 top-2 px-5 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-300 text-white font-medium text-sm rounded-lg shadow-xs transition flex items-center gap-1.5 cursor-pointer"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
              Ask AI
            </button>
          </div>

          {/* Controls: Model & Top-K */}
          <div className="flex flex-wrap items-center justify-between gap-4 pt-1">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <label className="text-xs font-semibold text-slate-600 uppercase tracking-wide">
                  Model:
                </label>
                <select
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  className="text-sm bg-slate-50 border border-slate-300 rounded-lg px-3 py-1.5 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-medium cursor-pointer"
                >
                  <option value="semantic">Semantic (all-MiniLM-L6-v2) [Best for AI Concepts]</option>
                  <option value="hybrid">Hybrid (TF-IDF + Semantic) [Fused Representation]</option>
                  <option value="tfidf">TF-IDF Lexical Baseline [Exact Model Names]</option>
                </select>
              </div>

              <div className="flex items-center gap-2">
                <label className="text-xs font-semibold text-slate-600 uppercase tracking-wide">
                  Top-K:
                </label>
                <select
                  value={topK}
                  onChange={(e) => setTopK(Number(e.target.value))}
                  className="text-sm bg-slate-50 border border-slate-300 rounded-lg px-3 py-1.5 text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-medium cursor-pointer"
                >
                  <option value={5}>Top 5</option>
                  <option value={10}>Top 10</option>
                  <option value={20}>Top 20</option>
                </select>
              </div>
            </div>

            {/* Quick Sample Questions */}
            <div className="flex items-center gap-2 overflow-x-auto text-xs text-slate-500">
              <span className="font-semibold text-slate-400">Sample Questions:</span>
              {sampleQuestions.map((sq, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => {
                    setQuery(sq);
                    handleSearch(undefined, sq);
                  }}
                  className="px-2.5 py-1 bg-slate-100 hover:bg-indigo-50 hover:text-indigo-700 text-slate-700 rounded-md transition whitespace-nowrap cursor-pointer border border-slate-200/60"
                >
                  {sq}
                </button>
              ))}
            </div>
          </div>
        </form>
      </div>

      {/* Error state */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl text-sm">
          {error}
        </div>
      )}

      {/* Direct Extractive Answer Card */}
      {response && response.direct_answer && (
        <div className="bg-gradient-to-r from-indigo-50/90 via-white to-purple-50/60 border border-indigo-200 rounded-2xl p-5 shadow-xs">
          <div className="flex items-center gap-2 text-indigo-900 font-bold text-sm mb-2">
            <Sparkles className="w-4 h-4 text-indigo-600" />
            <span>Key Research Finding / Direct Answer:</span>
          </div>
          <p className="text-slate-800 text-base leading-relaxed pl-6 border-l-2 border-indigo-500 italic">
            "{response.direct_answer}"
          </p>
          <div className="mt-2 text-xs text-slate-500 pl-6">
            Extracted from top-ranked AI paper: <strong>{response.results?.[0]?.title || 'AI Research Record'}</strong>
            {response.results?.[0]?.doc_id && <span> (ID: {response.results[0].doc_id})</span>}
          </div>
        </div>
      )}

      {/* Results Header */}
      {response && (
        <div className="flex items-center justify-between text-xs text-slate-500 px-1">
          <div className="flex items-center gap-2">
            <span>Retrieved <strong>{response.total_results ?? response.results?.length ?? 0}</strong> relevant AI documents</span>
            <span>•</span>
            <span className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5" /> {(response.latency_ms != null ? response.latency_ms : 0).toFixed(1)} ms
            </span>
          </div>
          <span className="italic text-slate-400">
            Cosine similarity scores represent vector closeness (0.0 to 1.0).
          </span>
        </div>
      )}

      {/* Results List */}
      <div className="space-y-4">
        {response?.results?.map((item: SearchResultItem) => (
          <div
            key={item.doc_id}
            className="bg-white p-5 rounded-xl border border-slate-200 hover:border-indigo-300 transition shadow-xs group"
          >
            <div className="flex items-start justify-between gap-4 mb-2">
              <div className="flex items-center gap-2">
                <span className="w-6 h-6 rounded-md bg-slate-100 text-slate-700 text-xs font-bold flex items-center justify-center">
                  #{item.rank}
                </span>
                <span className="text-xs font-mono font-medium text-slate-500 px-2 py-0.5 bg-slate-100 rounded">
                  {(item.doc_id || '').slice(0, 12)}...
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-medium text-slate-500">
                  Similarity Score:
                </span>
                <span className="text-sm font-bold text-indigo-700 bg-indigo-50 border border-indigo-100 px-2.5 py-0.5 rounded-full">
                  {(item.score != null ? item.score : 0).toFixed(4)}
                </span>
              </div>
            </div>

            <h3
              onClick={() => onSelectDoc(item.doc_id)}
              className="text-base font-bold text-slate-900 group-hover:text-indigo-600 cursor-pointer transition mb-2"
            >
              {item.title || 'Untitled AI Paper'}
            </h3>

            <p className="text-sm text-slate-600 leading-relaxed mb-3">
              {item.snippet}
            </p>

            <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-xs text-slate-500">
              <div className="flex items-center gap-3">
                {item.tfidf_raw != null && (
                  <span>TF-IDF raw: {Number(item.tfidf_raw).toFixed(4)}</span>
                )}
                {item.semantic_raw != null && (
                  <span>Semantic raw: {Number(item.semantic_raw).toFixed(4)}</span>
                )}
                {item.metadata?.year && (
                  <span>Year: {item.metadata.year}</span>
                )}
              </div>
              <button
                onClick={() => onSelectDoc(item.doc_id)}
                className="inline-flex items-center gap-1 text-slate-700 font-medium hover:text-indigo-600 cursor-pointer"
              >
                Inspect Paper <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
