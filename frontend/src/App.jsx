import { useState } from "react"
import axios from "axios"

function App() {

  const [groups, setGroups] = useState({
    A: 30, B: 200, C: 10,
    D: 40, E: 60, F: 10,
    G: 20, H: 30, I: 20
  })

  const [result, setResult] = useState(null)

  const handleChange = (key, value) => {
    setGroups({...groups, [key]: Number(value)})
  }

  const optimize = async () => {
    const res = await axios.post("http://localhost:8000/optimize", groups)
    setResult(res.data)
  }

  return (
    <div style={{padding: 40}}>
      <h1>避難ルート最適化アプリ</h1>

      <h2>人数入力</h2>
      {Object.keys(groups).map(g => (
        <div key={g}>
          {g}:
          <input
            type="number"
            value={groups[g]}
            onChange={(e)=>handleChange(g, e.target.value)}
          />
        </div>
      ))}

      <button onClick={optimize}>最適化実行</button>

      {result && (
        <>
          <h2>ルート結果</h2>
          {Object.entries(result.routes).map(([g, route]) => (
            <div key={g}>
              {g} → {route.join(" → ")}
            </div>
          ))}

          <h2>エッジ混雑状況</h2>
          {Object.entries(result.edge_load).map(([e, load]) => (
            <div key={e}>
              {e}: {load}人
            </div>
          ))}
        </>
      )}
    </div>
  )
}

export default App