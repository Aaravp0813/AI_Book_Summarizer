import Header from './Header';
import './Layout.css';

export default function Layout({ children }) {
  return (
    <div className="layout">
      <Header />
      <main className="main-content">
        {children}
      </main>
      <footer className="footer">
        <p>NCERT Grade 8 Science AI Tutor • Study with confidence</p>
      </footer>
    </div>
  );
}
