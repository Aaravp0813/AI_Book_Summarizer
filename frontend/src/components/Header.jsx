import './Header.css';
import { getSubject } from '../config/subjects';

export default function Header({ subject, onChangeSubject }) {
  const subjectInfo = subject ? getSubject(subject) : null;

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-content">
          <h1 className="header-title">NCERT AI Tutor</h1>
          {subjectInfo && (
            <>
              <p className="header-subtitle">AI Study Tutor for Grade 8 {subjectInfo.label}</p>
              <button className="change-subject-btn" onClick={onChangeSubject}>
                Change Subject
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
