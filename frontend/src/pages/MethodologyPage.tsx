import { BookOpen, ShieldCheck, Cpu } from 'lucide-react';

export const MethodologyPage = () => {
  return (
    <div className="space-y-8 max-w-4xl mx-auto text-slate-800">
      <div>
        <h2 className="text-2xl font-bold text-slate-900">
          AI Dataset & Methodology Documentation
        </h2>
        <p className="text-sm text-slate-500 mt-1">
          Complete academic specification of dataset provenance, preprocessing pipeline, retrieval formalisms, and research hypotheses on Artificial Intelligence literature.
        </p>
      </div>

      {/* Research Question and Hypotheses */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 space-y-4 shadow-xs">
        <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-indigo-600" />
          Research Question & Academic Hypotheses
        </h3>
        <blockquote className="p-4 bg-slate-50 border-l-4 border-indigo-600 rounded-r text-sm text-slate-700 italic">
          "How does semantic embedding-based retrieval compare with TF-IDF-based lexical retrieval for question-to-document similarity in Artificial Intelligence and Computer Science literature?"
        </blockquote>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <div className="p-4 bg-slate-50 border border-slate-100 rounded-lg text-xs leading-relaxed">
            <span className="font-bold text-slate-900 block mb-1">H1: Semantic Generalization</span>
            Dense embeddings significantly outperform lexical models in AI literature due to rapid vocabulary evolution and conceptual synonymy (Confirmed: MRR 0.366 vs 0.249, +47.1%).
          </div>
          <div className="p-4 bg-slate-50 border border-slate-100 rounded-lg text-xs leading-relaxed">
            <span className="font-bold text-slate-900 block mb-1">H2: Exact Acronym Precision</span>
            TF-IDF remains fast and precise when queries explicitly query specific named benchmarks, datasets, or architecture acronyms.
          </div>
          <div className="p-4 bg-slate-50 border border-slate-100 rounded-lg text-xs leading-relaxed">
            <span className="font-bold text-slate-900 block mb-1">H3: Indexing Scalability</span>
            Encoding 25,657 documents into 384-dimensional dense vectors requires substantial batch processing compared to sparse CSR matrix construction.
          </div>
        </div>
      </div>

      {/* Dataset Provenance */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 space-y-3 shadow-xs">
        <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-600" />
          Official Benchmark Dataset: SciDocs (BEIR Benchmark)
        </h3>
        <p className="text-sm text-slate-600 leading-relaxed">
          SciDocs is a standardized scientific paper evaluation benchmark developed by the Allen Institute for AI (AI2). It consists of 25,657 peer-reviewed papers spanning artificial intelligence, machine learning, natural language processing, computer vision, and neural engineering. Ground-truth relevance is defined through direct and co-citation linkages.
        </p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 text-xs">
          <div className="p-3 bg-slate-50 rounded border border-slate-100">
            <div className="text-slate-400 font-semibold">Indexed AI Papers</div>
            <div className="text-base font-bold text-slate-900 mt-0.5">25,657</div>
          </div>
          <div className="p-3 bg-slate-50 rounded border border-slate-100">
            <div className="text-slate-400 font-semibold">Test Queries</div>
            <div className="text-base font-bold text-slate-900 mt-0.5">1,000</div>
          </div>
          <div className="p-3 bg-slate-50 rounded border border-slate-100">
            <div className="text-slate-400 font-semibold">Citation Qrels</div>
            <div className="text-base font-bold text-slate-900 mt-0.5">29,928</div>
          </div>
          <div className="p-3 bg-slate-50 rounded border border-slate-100">
            <div className="text-slate-400 font-semibold">License</div>
            <div className="text-base font-bold text-slate-900 mt-0.5">CC BY-SA 4.0</div>
          </div>
        </div>
      </div>

      {/* Preprocessing and Modeling Formalisms */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 space-y-4 shadow-xs">
        <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
          <Cpu className="w-5 h-5 text-purple-600" />
          Mathematical & Algorithmic Formulation
        </h3>
        <div className="space-y-3 text-sm text-slate-600">
          <div>
            <h4 className="font-semibold text-slate-900">1. Lexical Model (TF-IDF):</h4>
            <p className="text-xs text-slate-500 mt-0.5">
              Utilizes sublinear term frequency: <code>tf' = 1 + log(tf)</code> and smooth inverse document frequency: <code>idf(t) = log((1 + n) / (1 + df(t))) + 1</code>. Built over 60,000 unigrams and bigrams.
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-slate-900">2. Semantic Model (Sentence Transformers):</h4>
            <p className="text-xs text-slate-500 mt-0.5">
              Utilizes <code>all-MiniLM-L6-v2</code>. Text sequences are encoded into 384-dimensional dense vectors with mean-pooling over contextual token representations. Embeddings are L2-normalized: <code>||v||_2 = 1</code>, allowing fast dot products to compute exact cosine similarity across all 25k documents in ~20ms.
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-slate-900">3. Extractive Question Answering:</h4>
            <p className="text-xs text-slate-500 mt-0.5">
              Computes keyword-density and relevance scores across candidate sentences in the top retrieved paper to extract the most informative conclusion answering the user's question.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
