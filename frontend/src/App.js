import Upload from "./Upload";
import Chat from "./Chat";
import "./App.css";

function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <h2>🤖 AI Q&A</h2>
        <Upload />
      </aside>

      <main className="chat-section">
        <Chat />
      </main>
    </div>
  );
}

export default App;