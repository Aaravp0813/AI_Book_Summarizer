import './AnswerPanel.css';

export default function AnswerPanel({
  state,
  answer,
  question,
  error,
  onRetry,
}) {
  if (state === 'idle') {
    return (
      <div className="answer-panel idle">
        <p className="idle-message">
          Welcome to your AI Study Tutor! Choose a topic above or ask your own question to get started.
        </p>
      </div>
    );
  }

  if (state === 'loading') {
    return (
      <div className="answer-panel loading">
        <div className="spinner"></div>
        <p className="loading-message">
          The tutor is thinking about your question...
        </p>
      </div>
    );
  }

  if (state === 'error') {
    return (
      <div className="answer-panel error">
        <div className="error-container">
          <h3 className="error-title">Oops! Something went wrong</h3>
          <p className="error-message">{error}</p>
          <button className="retry-button" onClick={onRetry}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (state === 'success') {
    return (
      <div className="answer-panel success">
        <div className="answer-header">
          <p className="answer-question">
            <span className="label">Your question:</span>
            <span className="text">{question}</span>
          </p>
        </div>
        <div className="answer-body">
          <div className="answer-content">
            {answer}
          </div>
        </div>
      </div>
    );
  }

  return null;
}
