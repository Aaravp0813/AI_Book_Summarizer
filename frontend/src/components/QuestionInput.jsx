import { useState } from 'react';
import './QuestionInput.css';

export default function QuestionInput({
  value,
  onChange,
  onSubmit,
  isLoading,
  error,
}) {
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit();
  };

  const handleKeyDown = (e) => {
    // Allow Ctrl+Enter to submit
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  const isEmpty = !value || !value.trim();

  return (
    <form className="question-input-form" onSubmit={handleSubmit}>
      <div className="input-wrapper">
        <label htmlFor="question-input" className="visually-hidden">
          Ask your question
        </label>
        <textarea
          id="question-input"
          className="question-input"
          placeholder="Ask me anything about NCERT Grade 8 Science..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          aria-describedby={error ? 'error-message' : undefined}
        />
      </div>

      <div className="input-actions">
        <button
          type="submit"
          className="submit-button primary"
          disabled={isLoading || isEmpty}
        >
          {isLoading ? 'Thinking...' : 'Ask Tutor'}
        </button>
        <p className="hint">
          Tip: Press Ctrl+Enter to submit
        </p>
      </div>

      {error && (
        <p id="error-message" className="input-error">
          {error}
        </p>
      )}
    </form>
  );
}
