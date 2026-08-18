import './TopicChips.css';
import { getSubject } from '../config/subjects';

export default function TopicChips({ subject, onTopicClick }) {
  const subjectInfo = getSubject(subject);
  const topics = subjectInfo?.topics || [];

  return (
    <div className="topic-chips-container">
      <p className="topic-chips-label">Try asking about these topics:</p>
      <div className="topic-chips">
        {topics.map((topic) => (
          <button
            key={topic}
            className="chip"
            onClick={() => onTopicClick(topic)}
          >
            {topic}
          </button>
        ))}
      </div>
    </div>
  );
}
