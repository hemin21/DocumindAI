import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { DatasetInfo } from '../types';
import { Database, Search, Activity, Layers, CheckCircle2, Cpu } from 'lucide-react';

interface OverviewProps {
  onNavigate: (tab: string) => void;
}

export const Overview = ({ onNavigate }: OverviewProps) => {
  const [dataset, setDataset] = useState<DatasetInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const ds = await api.getDatasetInfo();
        setDataset(ds);
      } catch (err) {
        console.error('Error loading overview data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-20 text-slate-500">
        <Activity className="w-6 h-6 animate-spin mr-2" />
        Loading AI dataset statistics...
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 border border-slate-800 rounded-2xl p-8 text-white shadow-xl">
        <div className="max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded-full text-xs font-medium uppercase tracking-wider mb-4">
            <Cpu className="w-3.5 h-3.5" /> Artificial Intelligence & Computer Science Testbed
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
            DocuMind AI
          </h1>
          <p className="mt-2 text-lg text-slate-300 italic">
            Ask naturally. Discover relevant AI & Machine Learning documents intelligently.
          </p>
          <p className="mt-4 text-sm text-slate-400 leading-relaxed">
            An academic information retrieval testbed indexing <strong>25,657 peer-reviewed AI and Machine Learning papers</strong> from the official BEIR SciDocs benchmark. Compares <strong>TF-IDF</strong>, <strong>Sentence Transformers (all-MiniLM-L6-v2)</strong>, and <strong>Hybrid Fusion</strong> with real-time extractive answer finding.
          </p>
          <div className="mt-6 flex flex-wrap gap-4">
            <button
              onClick={() => onNavigate('search')}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm rounded-lg shadow transition cursor-pointer"
            >
              <Search className="w-4 h-4" /> Start AI Research Search & Q&A
            </button>
            <button
              onClick={() => onNavigate('evaluation')}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium text-sm rounded-lg border border-slate-700 transition cursor-pointer"
            >
              <Activity className="w-4 h-4" /> View AI Benchmark Experiments
            </button>
          </div>
        </div>
      </div>

      {/* Verified Corpus Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center gap-3 text-slate-500 mb-2">
            <Database className="w-5 h-5 text-indigo-600" />
            <span className="text-xs font-semibold uppercase tracking-wider">Indexed AI Papers</span>
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {dataset?.corpus_statistics.total_documents.toLocaleString() || '25,657'}
          </div>
          <p className="text-xs text-slate-500 mt-1">Full-text scientific abstracts</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center gap-3 text-slate-500 mb-2">
            <Search className="w-5 h-5 text-emerald-600" />
            <span className="text-xs font-semibold uppercase tracking-wider">Benchmark Queries</span>
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {dataset?.query_statistics.total_queries.toLocaleString() || '1,000'}
          </div>
          <p className="text-xs text-slate-500 mt-1">In official test evaluation</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center gap-3 text-slate-500 mb-2">
            <Layers className="w-5 h-5 text-blue-600" />
            <span className="text-xs font-semibold uppercase tracking-wider">Retrieval Engines</span>
          </div>
          <div className="text-2xl font-bold text-slate-900">3 Models</div>
          <p className="text-xs text-slate-500 mt-1">TF-IDF, Dense, Hybrid</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center gap-3 text-slate-500 mb-2">
            <CheckCircle2 className="w-5 h-5 text-teal-600" />
            <span className="text-xs font-semibold uppercase tracking-wider">Relevance Pairs</span>
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {dataset?.relevance_splits.test.num_judgments.toLocaleString() || '29,928'}
          </div>
          <p className="text-xs text-slate-500 mt-1">Test citation ground truth</p>
        </div>
      </div>

      {/* Core Architectural Pillars */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs">
          <h3 className="font-bold text-slate-900 text-lg mb-2 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
            1. TF-IDF Lexical Baseline
          </h3>
          <p className="text-sm text-slate-600 leading-relaxed mb-4">
            Sparse term-frequency vectorizer with sublinear scaling, unigram + bigram representation over a 60,000-token AI vocabulary.
          </p>
          <div className="text-xs font-medium text-slate-500 bg-slate-50 p-2.5 rounded border border-slate-100">
            High precision for exact model names (e.g. GAN, LSTM, ResNet, Word2Vec, BERT).
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs">
          <h3 className="font-bold text-slate-900 text-lg mb-2 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
            2. Semantic Embeddings
          </h3>
          <p className="text-sm text-slate-600 leading-relaxed mb-4">
            Pre-trained <code>all-MiniLM-L6-v2</code> Transformer mapping AI queries and papers into 384-dimensional dense semantic vector space.
          </p>
          <div className="text-xs font-medium text-slate-500 bg-slate-50 p-2.5 rounded border border-slate-100">
            Achieves superior conceptual matching (MRR 0.366, +47.1% over TF-IDF).
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs">
          <h3 className="font-bold text-slate-900 text-lg mb-2 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
            3. Min-Max Hybrid Fusion
          </h3>
          <p className="text-sm text-slate-600 leading-relaxed mb-4">
            Linear combination combining min-max scaled lexical cosine similarity and dense embedding cosine similarity (<code>α = 0.35</code>).
          </p>
          <div className="text-xs font-medium text-slate-500 bg-slate-50 p-2.5 rounded border border-slate-100">
            Balances architecture-specific nomenclature with general machine learning semantics.
          </div>
        </div>
      </div>
    </div>
  );
};
