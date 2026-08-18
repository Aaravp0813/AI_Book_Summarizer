import { SUBJECTS, SUBJECT_IDS } from '../config/subjects';
import './SubjectSelection.css';

export default function SubjectSelection({ onSelectSubject }) {
  return (
    <div className="subject-selection-page">
      <div className="subject-selection-container">
        <h1 className="selection-title">NCERT AI Tutor</h1>
        <p className="selection-subtitle">What would you like to study?</p>
        
        <div className="subjects-grid">
          {SUBJECT_IDS.map((subjectId) => {
            const subject = SUBJECTS[subjectId];
            return (
              <button
                key={subjectId}
                className="subject-card"
                onClick={() => onSelectSubject(subjectId)}
              >
                <div className="subject-icon">📚</div>
                <h2 className="subject-name">{subject.label}</h2>
                <p className="subject-grade">Grade 8</p>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
