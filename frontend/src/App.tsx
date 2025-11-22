import { useState } from 'react'
import { Search, Loader2, Building2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'

interface AnalysisResult {
  startup_name: string
  layer_id: number
  layer_name: string
  jp_name: string
  definition: string
  reasoning: string
  criteria_met: Record<string, string>
  criteria: Record<string, any>
  mode: string
}

function App() {
  const [startupName, setStartupName] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const analyzeStartup = async () => {
    if (!startupName.trim()) {
      setError('スタートアップ名を入力してください')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ startup_name: startupName.trim() }),
      })

      if (!response.ok) {
        throw new Error('分析に失敗しました')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : '分析中にエラーが発生しました')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !loading) {
      analyzeStartup()
    }
  }

  const getLayerColor = (layerId: number) => {
    const colors = [
      'bg-gray-100 text-gray-800 border-gray-300',
      'bg-blue-100 text-blue-800 border-blue-300',
      'bg-green-100 text-green-800 border-green-300',
      'bg-yellow-100 text-yellow-800 border-yellow-300',
      'bg-orange-100 text-orange-800 border-orange-300',
      'bg-purple-100 text-purple-800 border-purple-300',
    ]
    return colors[layerId] || colors[0]
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Building2 className="w-10 h-10 text-slate-700" />
            <h1 className="text-4xl font-bold text-slate-900">
              スタートアップ分析
            </h1>
          </div>
          <p className="text-lg text-slate-600">
            パラダイムシフト6階層モデルによる企業分析
          </p>
        </div>

        <Card className="mb-8 shadow-lg">
          <CardHeader>
            <CardTitle>スタートアップを分析</CardTitle>
            <CardDescription>
              企業名を入力して、パラダイムシフトのどの階層に位置するか分析します
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-2">
              <Input
                type="text"
                placeholder="例: Airbnb, Uber, Stripe..."
                value={startupName}
                onChange={(e) => setStartupName(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
                className="flex-1"
              />
              <Button
                onClick={analyzeStartup}
                disabled={loading || !startupName.trim()}
                className="min-w-24"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    分析中
                  </>
                ) : (
                  <>
                    <Search className="w-4 h-4 mr-2" />
                    分析
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {error && (
          <Alert variant="destructive" className="mb-8">
            <AlertTitle>エラー</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {result && (
          <Card className="shadow-lg">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-2xl mb-2">
                    {result.startup_name}
                  </CardTitle>
                  <div className="flex items-center gap-2 flex-wrap">
                    <Badge
                      variant="outline"
                      className={`text-lg px-4 py-1 ${getLayerColor(result.layer_id)}`}
                    >
                      Layer {result.layer_id}
                    </Badge>
                    <span className="text-xl font-semibold text-slate-700">
                      {result.layer_name}
                    </span>
                    <span className="text-xl text-slate-600">
                      ({result.jp_name})
                    </span>
                    <Badge
                      variant="outline"
                      className={result.mode === 'ai' ? 'bg-green-100 text-green-800 border-green-300' : 'bg-amber-100 text-amber-800 border-amber-300'}
                    >
                      {result.mode === 'ai' ? 'AIモード' : 'ルールベース'}
                    </Badge>
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2">
                  定義
                </h3>
                <p className="text-slate-700 leading-relaxed">
                  {result.definition}
                </p>
              </div>

              <Separator />

              <div>
                <h3 className="text-lg font-semibold text-slate-900 mb-3">
                  分析理由
                </h3>
                <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                  <p className="text-slate-700 leading-relaxed whitespace-pre-wrap">
                    {result.reasoning}
                  </p>
                </div>
              </div>

              {Object.keys(result.criteria_met).length > 0 && (
                <>
                  <Separator />
                  <div>
                    <h3 className="text-lg font-semibold text-slate-900 mb-3">
                      満たされた基準
                    </h3>
                    <div className="space-y-3">
                      {Object.entries(result.criteria_met).map(([key, value]) => (
                        <div
                          key={key}
                          className="bg-slate-50 rounded-lg p-3 border border-slate-200"
                        >
                          <div className="font-medium text-slate-900 mb-1">
                            {key}
                          </div>
                          <div className="text-sm text-slate-600">{value}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              )}

              <Separator />

              <div>
                <h3 className="text-lg font-semibold text-slate-900 mb-3">
                  階層の基準
                </h3>
                <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                  <pre className="text-sm text-slate-700 whitespace-pre-wrap font-mono">
                    {JSON.stringify(result.criteria, null, 2)}
                  </pre>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        <div className="mt-8 text-center text-sm text-slate-500">
          <p>パラダイムシフト6階層モデル (1990年以降創業のスタートアップ対象)</p>
        </div>
      </div>
    </div>
  )
}

export default App
