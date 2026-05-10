import { useState } from 'react'

function App() {
  const [cv, setCv] = useState('')
  const [jd, setJd] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState('mock') // 'mock' or 'claude'

  const analyze = async () => {
    if (!cv.trim() || !jd.trim()) {
      return alert('Please paste both CV and job description')
    }
    setLoading(true)
    setResult(null)

    try {
      if (mode === 'claude') {
        // 🔹 PRO MODE: Requires Claude API key (free tier available)
        const API_KEY = import.meta.env.VITE_CLAUDE_API_KEY
        if (!API_KEY) {
          alert('Claude API key not set. Switching to mock mode.')
          setMode('mock')
          throw new Error('No API key')
        }
        
        const response = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: {
            'x-api-key': API_KEY,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
          },
          body: JSON.stringify({
            model: 'claude-3-haiku-20240307',
            max_tokens: 1000,
            messages: [{
              role: 'user',
              content: `You are an AI career coach for Luxembourg BFSI roles. Analyze this CV against the job description.

Score 0-100 on these 5 dimensions:
1. skills_match
2. experience_relevance  
3. education_alignment
4. ai_fluency
5. communication_clarity

Output ONLY valid JSON in this format:
{
  "fitScore": number,
  "dimensions": {
    "skills_match": {"score": number, "gaps": ["string"]},
    "experience_relevance": {"score": number, "gaps": ["string"]},
    "education_alignment": {"score": number, "gaps": ["string"]},
    "ai_fluency": {"score": number, "gaps": ["string"]},
    "communication_clarity": {"score": number, "gaps": ["string"]}
  },
  "feedback": "string"
}

CV: ${cv}

JD: ${jd}`
            }]
          })
        })
        
        if (!response.ok) throw new Error('Claude API error')
        const data = await response.json()
        const jsonText = data.content[0].text
        setResult(JSON.parse(jsonText))
        
      } else {
        // 🔹 MOCK MODE: No API key needed — perfect for demo
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // Smart mock response based on input keywords
        const hasBFSI = /guidewire|claims|insurance|bfsi|usaa/i.test(cv)
        const hasFrench = /french|français/i.test(cv + jd)
        const hasAI = /prompt|claude|llm|ai automation/i.test(cv)
        
        setResult({
          fitScore: hasBFSI && hasAI ? 88 : hasBFSI ? 82 : 75,
          dimensions: {
            skills_match: { 
              score: hasAI ? 90 : 75, 
              gaps: hasAI ? [] : ['Prompt engineering', 'LLM orchestration'] 
            },
            experience_relevance: { 
              score: hasBFSI ? 92 : 70, 
              gaps: hasBFSI ? [] : ['BFSI domain knowledge'] 
            },
            education_alignment: { score: 88, gaps: [] },
            ai_fluency: { 
              score: hasAI ? 95 : 60, 
              gaps: hasAI ? [] : ['Multi-LLM workflows'] 
            },
            communication_clarity: { 
              score: 85, 
              gaps: hasFrench ? [] : ['French (B1) — recommended for Luxembourg roles'] 
            }
          },
          feedback: hasBFSI 
            ? "Strong BFSI domain fit. Highlight your Guidewire/USAA experience prominently." 
            : "Consider adding BFSI keywords (Guidewire, claims, compliance) to align with Luxembourg finance roles."
        })
      }
    } catch (err) {
      console.error('Analysis error:', err)
      // Fallback to mock on any error
      setResult({
        fitScore: 80,
        dimensions: {
          skills_match: { score: 80, gaps: ['SQL', 'French B1'] },
          experience_relevance: { score: 85, gaps: [] },
          education_alignment: { score: 90, gaps: [] },
          ai_fluency: { score: 88, gaps: [] },
          communication_clarity: { score: 72, gaps: ['Executive summaries'] }
        },
        feedback: "Demo mode: Connect Claude API for live analysis. Strong foundation — tailor BFSI keywords for Luxembourg roles."
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-indigo-900 mb-2">
            🎯 TRAS v1.0
          </h1>
          <p className="text-gray-600 text-lg">
            AI Talent Risk Assessment • Luxembourg BFSI Focus
          </p>
          <div className="mt-3 flex justify-center gap-2">
            <a href="https://pkswaminathan001.github.io/portfolio" 
               className="text-indigo-600 hover:underline text-sm">
               ← Back to Portfolio
            </a>
            <span className="text-gray-400">•</span>
            <a href="https://github.com/pkswaminathan001/tras-ai" 
               target="_blank" rel="noopener"
               className="text-indigo-600 hover:underline text-sm">
               View Code on GitHub
            </a>
          </div>
        </header>

        {/* Mode Toggle */}
        <div className="flex justify-center mb-6">
          <div className="bg-white rounded-full p-1 shadow-sm inline-flex">
            <button
              onClick={() => setMode('mock')}
              className={`px-4 py-2 rounded-full text-sm font-medium transition ${
                mode === 'mock' 
                  ? 'bg-indigo-600 text-white' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              🎭 Mock Mode (Free)
            </button>
            <button
              onClick={() => setMode('claude')}
              className={`px-4 py-2 rounded-full text-sm font-medium transition ${
                mode === 'claude' 
                  ? 'bg-indigo-600 text-white' 
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              🤖 Claude API (Pro)
            </button>
          </div>
        </div>

        {/* Input Grid */}
        <div className="grid md:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              📄 Paste CV Text
            </label>
            <textarea
              className="w-full h-40 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
              placeholder="Example: Prompt Engineer with 2+ years BFSI experience at HCL (USAA). MBA. Skills: Claude API, GitHub Actions, Guidewire..."
              value={cv}
              onChange={e => setCv(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              💼 Paste Job Description
            </label>
            <textarea
              className="w-full h-40 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
              placeholder="Example: AI Business Analyst at Deloitte Luxembourg. Requirements: Python, SQL, prompt engineering, BFSI domain knowledge, French B1..."
              value={jd}
              onChange={e => setJd(e.target.value)}
            />
          </div>
        </div>

        {/* Analyze Button */}
        <button
          onClick={analyze}
          disabled={loading}
          className="w-full py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              Analyzing...
            </>
          ) : (
            '🚀 Analyze Fit'
          )}
        </button>

        {/* API Key Notice (Claude Mode) */}
        {mode === 'claude' && (
          <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-800">
            💡 To use Claude API: 
            1. Get key at <a href="https://console.anthropic.com" className="underline" target="_blank">console.anthropic.com</a>
            2. Create `.env` file with: <code className="bg-yellow-100 px-1 rounded">VITE_CLAUDE_API_KEY=sk-ant-...</code>
            3. Redeploy. <button onClick={() => setMode('mock')} className="underline ml-1">Or stay in Mock Mode</button>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="mt-8 p-6 bg-white rounded-xl shadow-lg border border-gray-100">
            {/* Overall Score */}
            <div className="text-center mb-6 pb-4 border-b border-gray-100">
              <div className="text-6xl font-bold text-indigo-600 mb-1">
                {result.fitScore}
                <span className="text-2xl text-gray-400">/100</span>
              </div>
              <div className="text-gray-600 font-medium">Overall Fit Score</div>
              <div className="mt-2 text-sm text-gray-500">
                {result.fitScore >= 85 ? '✅ Strong match — apply now' : 
                 result.fitScore >= 70 ? '🟡 Good fit — tailor keywords' : 
                 '🔴 Stretch role — address gaps first'}
              </div>
            </div>
            
            {/* Dimensions */}
            <div className="space-y-3 mb-6">
              {Object.entries(result.dimensions).map(([key, val]) => {
                const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
                const color = val.score >= 80 ? 'text-green-600' : val.score >= 60 ? 'text-yellow-600' : 'text-red-600'
                return (
                  <div key={key} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium text-gray-700">{label}</span>
                    <div className="text-right">
                      <span className={`font-bold ${color}`}>{val.score}/100</span>
                      {val.gaps?.length > 0 && (
                        <div className="text-xs text-gray-500 mt-1">
                          Gaps: {val.gaps.join(', ')}
                        </div>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
            
            {/* Feedback */}
            {result.feedback && (
              <div className="p-4 bg-indigo-50 rounded-lg border border-indigo-100">
                <div className="font-semibold text-indigo-900 mb-1">💡 Recommendation</div>
                <p className="text-indigo-800">{result.feedback}</p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="mt-6 flex flex-wrap gap-3 justify-center">
              <button
                onClick={() => { setCv(''); setJd(''); setResult(null) }}
                className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition text-sm"
              >
                🔄 New Analysis
              </button>
              <a
                href="https://pkswaminathan001.github.io/portfolio"
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition text-sm"
              >
                💼 View My Portfolio
              </a>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-gray-500 pb-8">
          <p>Built by <strong>PR Swaminathan</strong> • Prompt Engineer | AI Business Analyst</p>
          <p className="mt-1">🇱🇺 Optimized for Luxembourg BFSI/AI roles</p>
          <p className="mt-2 text-xs">
            Mock mode: No API key needed • Claude mode: Free tier available at{' '}
            <a href="https://console.anthropic.com" className="underline" target="_blank">console.anthropic.com</a>
          </p>
        </footer>
      </div>
    </div>
  )
}

export default App
