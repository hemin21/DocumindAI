import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { EvaluationSummaryItem, ErrorCase } from '../types';
import { BarChart3, AlertTriangle, Clock, Award } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

export const EvaluationPage = () => {
  const [summary, setSummary] = useState<EvaluationSummaryItem[]>([]);
  const [errors, setErrors] = useState<ErrorCase[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [sum, err] = await Promise.all([
          api.getEvaluationSummary(),
          api.getEvaluationErrors()
        ]);
        setSummary(sum || []);
        setErrors(err || []);
      } catch (e) {
        console.error('Failed to load evaluation artifacts:', e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Loading experimental benchmarks...</div>;
  }

  // Format data for Recharts safely with null checks
  const chartData = (summary || []).map((s) => ({
    name: (s.Model || '').replace(" (all-MiniLM-L6-v2)", "").replace(" (TF-IDF + Semantic)", ""),
    "Precision@5": Number((s["Precision@5"] != null ? s["Precision@5"] : 0).toFixed(3)),
    "Recall@5": Number((s["Recall@5"] != null ? s["Recall@5"] : 0).toFixed(3)),
    "F1@5": Number((s["F1@5"] != null ? s["F1@5"] : 0).toFixed(3)),
    MRR: Number((s.MRR != null ? s.MRR : 0).toFixed(3)),
    "nDCG@10": Number((s["nDCG@10"] != null ? s["nDCG@10"] : 0).toFixed(3)),
    "Latency (ms)": Number((s["Mean Latency (ms)"] != null ? s["Mean Latency (ms)"] : 0).toFixed(1))
  }));

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Page Title */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900">
          Experimental Evaluation & Comparative Benchmarks
        </h2>
        <p className="text-sm text-slate-500 mt-1">
          Measured results across 1,000 queries and 25,657 indexed papers on the official BEIR SciDocs Artificial Intelligence benchmark.
        </p>
      </div>

      {/* Main Results Table */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <h3 className="font-bold text-slate-900 flex items-center gap-2">
            <Award className="w-5 h-5 text-indigo-600" />
            Official SciDocs AI Benchmark Evaluation Summary
          </h3>
          <span className="text-xs font-mono bg-slate-100 text-slate-600 px-2 py-1 rounded">
            Split: test (qrels/test.tsv) • 1,000 Queries
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                <th className="py-3 px-4">Retrieval Model</th>
                <th className="py-3 px-4">Precision@5</th>
                <th className="py-3 px-4">Recall@5</th>
                <th className="py-3 px-4">F1@5</th>
                <th className="py-3 px-4 font-bold text-indigo-700">MRR</th>
                <th className="py-3 px-4 font-bold text-indigo-700">nDCG@10</th>
                <th className="py-3 px-4">Mean Latency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {(summary || []).map((row) => (
                <tr key={row.Model} className="hover:bg-slate-50/50">
                  <td className="py-3.5 px-4 font-medium text-slate-900">{row.Model}</td>
                  <td className="py-3.5 px-4">{(row["Precision@5"] != null ? row["Precision@5"] : 0).toFixed(4)}</td>
                  <td className="py-3.5 px-4">{(row["Recall@5"] != null ? row["Recall@5"] : 0).toFixed(4)}</td>
                  <td className="py-3.5 px-4">{(row["F1@5"] != null ? row["F1@5"] : 0).toFixed(4)}</td>
                  <td className="py-3.5 px-4 font-bold text-indigo-700">{(row.MRR != null ? row.MRR : 0).toFixed(4)}</td>
                  <td className="py-3.5 px-4 font-bold text-indigo-700">{(row["nDCG@10"] != null ? row["nDCG@10"] : 0).toFixed(4)}</td>
                  <td className="py-3.5 px-4 font-mono text-xs">{(row["Mean Latency (ms)"] != null ? row["Mean Latency (ms)"] : 0).toFixed(1)} ms</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Interactive Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Quality Chart */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <h3 className="font-bold text-slate-900 text-sm mb-4 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-indigo-600" />
            Ranking Quality Comparison (MRR vs nDCG@10)
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis domain={[0, 0.45]} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="MRR" fill="#4f46e5" radius={[4, 4, 0, 0]} />
                <Bar dataKey="nDCG@10" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Latency Chart */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
          <h3 className="font-bold text-slate-900 text-sm mb-4 flex items-center gap-2">
            <Clock className="w-4 h-4 text-amber-600" />
            Query Latency Comparison Across 25k Docs (ms)
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="Latency (ms)" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Error Analysis Section */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <h3 className="font-bold text-slate-900 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-500" />
            Qualitative Error & Failure Analysis Sample in AI Literature
          </h3>
          <span className="text-xs text-slate-500">{errors.length} failure cases analyzed</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                <th className="py-3 px-4">Query ID</th>
                <th className="py-3 px-4">AI Research Query</th>
                <th className="py-3 px-4">Observed Failure Category</th>
                <th className="py-3 px-4">NLP Mechanism Explanation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {errors.slice(0, 8).map((err, idx) => (
                <tr key={idx} className="hover:bg-slate-50/50">
                  <td className="py-3 px-4 font-mono text-xs font-semibold text-slate-600">{(err.query_id || '').slice(0, 10)}...</td>
                  <td className="py-3 px-4 text-slate-900 font-medium">{err.query_text}</td>
                  <td className="py-3 px-4">
                    <span className="inline-block px-2.5 py-1 text-xs rounded-full font-medium bg-amber-50 text-amber-800 border border-amber-200">
                      {err.error_category}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-xs text-slate-600">{err.explanation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
