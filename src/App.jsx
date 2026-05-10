import { useState } from 'react'
function App() {
  const [cv, setCv] = useState('')
  const [jd, setJd] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState('mock')
  const analyze = async () => {
    if (!cv.trim() || !jd.trim()) return alert('Paste CV and JD')
    setLoading(true); setResult(null)
    try {
      if (mode === 'claude') {
        const API_KEY = import.meta.env.VITE_CLAUDE_API_KEY
        if (!API_KEY) { alert('No key → Mock mode'); setMode('mock'); return }
        // Claude API call would go here (omitted for demo)
      } else {
        await new Promise(r => setTimeout(r, 1000))
        const hasBFSI = /guidewire|claims|insurance|bfsi/i.test(cv)
        const hasFrench = /french|français/i.test(cv+jd)
        setResult({
          fitScore: hasBFSI ? 88 : 75,
          dimensions: {
            skills_match: { score: 90, gaps: hasBFSI ? [] : ['Prompt engineering'] },
            experience_relevance: { score: hasBFSI ? 92 : 70, gaps: hasBFSI ? [] : ['BFSI domain'] },
            education_alignment: { score: 88, gaps: [] },
            ai_fluency: { score: 95, gaps: [] },
            communication_clarity: { score: 85, gaps: hasFrench ? [] : ['French B1'] }
          },
          feedback: hasBFSI ? "Strong BFSI fit — highlight Guidewire/USAA experience." : "Add BFSI keywords for Luxembourg roles."
        })
      }
    } catch(e) { console.error(e); setResult({ fitScore: 80, feedback: "Demo mode" }) }
    finally { setLoading(false) }
  }
  return (
    <div className="min-h-screen p-4 md:p-8 bg-gradient-to-br from-indigo-50 to-purple-50">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center text-indigo-900 mb-2">🎯 TRAS v1.0</h1>
        <p className="text-center text-gray-600 mb-6">AI Talent Risk Assessment • Luxembourg BFSI</p>
        <div className="flex justify-center mb-4">
          <button onClick={()=>setMode('mock')} className={`px-4 py-2 rounded-l ${mode==='mock'?'bg-indigo-600 text-white':'bg-white'}`}>🎭 Mock</button>
          <button onClick={()=>setMode('claude')} className={`px-4 py-2 rounded-r ${mode==='claude'?'bg-indigo-600 text-white':'bg-white'}`}>🤖 Claude</button>
        </div>
        <div className="grid md:grid-cols-2 gap-4 mb-4">
          <textarea className="w-full h-32 p-3 border rounded" placeholder="Paste CV..." value={cv} onChange={e=>setCv(e.target.value)} />
          <textarea className="w-full h-32 p-3 border rounded" placeholder="Paste Job Description..." value={jd} onChange={e=>setJd(e.target.value)} />
        </div>
        <button onClick={analyze} disabled={loading} className="w-full py-3 bg-indigo-600 text-white rounded font-semibold hover:bg-indigo-700 disabled:opacity-50">
          {loading ? 'Analyzing...' : '🚀 Analyze Fit'}
        </button>
        {result && (
          <div className="mt-6 p-4 bg-white rounded shadow">
            <div className="text-4xl font-bold text-indigo-600 text-center">{result.fitScore}/100</div>
            <div className="mt-2 text-center text-gray-600">{result.feedback}</div>
            <div className="mt-4 space-y-2">
              {Object.entries(result.dimensions).map(([k,v])=>(
                <div key={k} className="flex justify-between p-2 bg-gray-50 rounded">
                  <span className="capitalize">{k.replace(/_/g,' ')}</span>
                  <span className="font-bold text-green-600">{v.score}/100</span>
                </div>
              ))}
            </div>
          </div>
        )}
        <footer className="mt-8 text-center text-sm text-gray-500">
          Built by PR Swaminathan • <a href="https://pkswaminathan001.github.io/portfolio" className="text-indigo-600">Portfolio</a>
        </footer>
      </div>
    </div>
  )
}
export default App
