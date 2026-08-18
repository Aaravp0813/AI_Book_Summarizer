import { useState } from 'react';
import TopicChips from '../components/TopicChips';
import QuestionInput from '../components/QuestionInput';
import AnswerPanel from '../components/AnswerPanel';
import { askQuestion } from '../services/api';
import './Home.css';

export default function Home({ subject, onChangeSubject }) {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [state, setState] = useState('idle'); // 'idle', 'loading', 'success', 'error'
  const [error, setError] = useState('');

  const handleTopicClick = (topic) => {
    setQuestion(topic);
  };

  const handleQuestionChange = (newQuestion) => {
    setQuestion(newQuestion);
    if (error) {
      setError('');
    }
  };

  const handleSubmit = async () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) {
      setError('Please ask a question first.');
      return;
    }

    setState('loading');
    setError('');
    setAnswer('');

    try {
      const response = await askQuestion(subject, trimmedQuestion);
      setQuestion(response.question);
      setAnswer(response.answer);
      setState('success');
    } catch (err) {
      setError(err.message);
      setState('error');
    }
  };

  const handleRetry = () => {
    handleSubmit();
  };

  return (
    <div className="home-page">
      <div className="home-container">
        <TopicChips subject={subject} onTopicClick={handleTopicClick} />

        <QuestionInput
          value={question}
          onChange={handleQuestionChange}
          onSubmit={handleSubmit}
          isLoading={state === 'loading'}
          error={error && state === 'idle' ? error : ''}
        />

        <AnswerPanel
          state={state}
          question={question}
          answer={answer}
          error={error}
          onRetry={handleRetry}
        />
      </div>
    </div>
  );
}