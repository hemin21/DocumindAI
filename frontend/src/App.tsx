import { useState } from 'react';
import { Overview } from './pages/Overview';
import { SearchPage } from './pages/SearchPage';
import { EvaluationPage } from './pages/EvaluationPage';
import { MethodologyPage } from './pages/MethodologyPage';
import { DocumentDetail } from './pages/DocumentDetail';
import { PdfUploadPage } from './pages/PdfUploadPage';
import { LayoutDashboard, Search, BarChart3, BookOpen, FileUp } from 'lucide-react';

export function App() {
  const [activeTab, setActiveTab] = useState<'overview' | 'search' | 'evaluation' | 'methodology' | 'pdf' | 'detail'>('overview');
  const [selectedDocId, setSelectedDocId] = useState<string | null>(null);

  const handleSelectDoc = (docId: string) => {
    setSelectedDocId(docId);
    setActiveTab('detail');
  };

  const navItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'search', label: 'Intelligent Search & Q&A', icon: Search },
    { id: 'evaluation', label: 'Benchmark Evaluation', icon: BarChart3 },
    { id: 'pdf', label: 'Custom PDF Upload', icon: FileUp },
    { id: 'methodology', label: 'Methodology & Dataset', icon: BookOpen },
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans antialiased">
      {/* Top Navigation */}
      <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('overview')}>
            <div className="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center text-white font-black text-lg shadow-sm">
              D
            </div>
            <div>
              <span className="font-extrabold text-lg tracking-tight text-slate-900">DocuMind</span>
              <span className="text-xs font-semibold px-1.5 py-0.5 ml-1.5 bg-indigo-50 text-indigo-700 rounded border border-indigo-200/50">AI</span>
            </div>
          </div>

          <nav className="flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id as any)}
                  className={`inline-flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition cursor-pointer ${
                    isActive
                      ? 'bg-indigo-50 text-indigo-700 font-semibold shadow-2xs'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-600' : 'text-slate-400'}`} />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && <Overview onNavigate={(t) => setActiveTab(t as any)} />}
        {activeTab === 'search' && <SearchPage onSelectDoc={handleSelectDoc} />}
        {activeTab === 'evaluation' && <EvaluationPage />}
        {activeTab === 'pdf' && <PdfUploadPage />}
        {activeTab === 'methodology' && <MethodologyPage />}
        {activeTab === 'detail' && selectedDocId && (
          <DocumentDetail docId={selectedDocId} onBack={() => setActiveTab('search')} />
        )}
      </main>

      {/* Academic Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <strong>DocuMind AI</strong> — Question-to-Document Similarity Based Intelligent Search System
          </div>
          <div>
            Evaluated on official BEIR NFCorpus • Built with FastAPI, scikit-learn & Sentence Transformers
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
