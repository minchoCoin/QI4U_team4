import { useState, useEffect } from 'react'
import './App.css'

function App() {
  // 1. バックエンドから取得したデータを保持する変数 (State)
  const [message, setMessage] = useState("")
  const [numbers, setNumbers] = useState([])

  // 2. 画面が表示された時に一度だけ実行される処理 (useEffect)
  useEffect(() => {
    // APIを叩く関数
    const fetchData = async () => {
      try {
        // Helloメッセージの取得
        const rootResponse = await fetch("http://localhost:8000/")
        const rootData = await rootResponse.json()
        setMessage(rootData.message)

        // 数値データの取得
        const dataResponse = await fetch("http://localhost:8000/api/data")
        const dataJson = await dataResponse.json()
        setNumbers(dataJson.data)
        
      } catch (error) {
        console.error("データの取得に失敗しました:", error)
      }
    }

    fetchData()
  }, []) // [] は「最初の1回だけ実行」という意味

  // 3. 画面の表示 (JSX)
  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>React + FastAPI連携テスト</h1>
      
      <div style={{ margin: "20px", border: "1px solid #ccc", padding: "10px" }}>
        <h2>バックエンドからのメッセージ:</h2>
        <p style={{ color: "blue", fontWeight: "bold" }}>{message}</p>
      </div>

      <div style={{ margin: "20px", border: "1px solid #ccc", padding: "10px" }}>
        <h2>取得したデータリスト:</h2>
        <ul>
          {numbers.map((num, index) => (
            <li key={index}>データ番号: {num}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default App