import './TopicChips.css';

const TOPICS = [
  'What is force?',
  'Explain pressure.',
  'What is friction?',
  'How does sound travel?',
  'What is the function of the cell membrane?',
  'Explain photosynthesis.',
  'How is light reflected?',
  'What are chemical effects of electric current?',
];

export default function TopicChips({ onTopicClick }) {
  return (
    <div className="topic-chips-container">
      <p className="topic-chips-label">Try asking about these topics:</p>
      <div className="topic-chips">
        {TOPICS.map((topic) => (
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
