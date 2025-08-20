// frontend/src/app/page.tsx
'use client';
import { useState } from 'react';
import styles from './page.module.css';

export default function Home() {
  const [url, setUrl] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResponseMessage('');
    try {
      const response = await fetch('http://localhost:8000/summaries', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'サーバーでエラーが発生しました。');
      }
      const data = await response.json();
      setResponseMessage(data.summary);
    } catch (error) {
      if (error instanceof Error) {
        setResponseMessage(`エラー：${error.message}`);
      } else {
        setResponseMessage('不明なエラーが発生しました。');
      }
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className={styles.main}>
      <div className={styles.description}>
        <h1>Webサイト要約サービス</h1>
        <form onSubmit={handleSubmit} style={{ width: '100%', maxWidth: '500px', display: 'flex', gap: '10px' }}>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            required
            style={{
              flexGrow: 1,
              padding: '10px',
              color: 'black',
              background: 'white',
              border: '2px solid #1976d2',
              borderRadius: '6px',
              fontSize: '1rem',
              boxShadow: '0 2px 6px rgba(0,0,0,0.05)'
            }}
          />
          <button type="submit" disabled={isLoading} style={{ padding: '10px 20px' }}>
            {isLoading ? '処理中...' : '要約する'}
          </button>
        </form>
        {responseMessage && (
          <div style={{ marginTop: '1rem', color: 'cyan', backgroundColor: '#222', padding: '1rem', borderRadius: '8px', width: '100%', maxWidth: '500px', whiteSpace: 'pre-wrap' }}>
            {responseMessage}
          </div>
        )}
      </div>
    </main>
  );
}