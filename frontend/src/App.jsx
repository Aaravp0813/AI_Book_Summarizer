import { useState } from 'react';
import Layout from './components/Layout';
import Home from './pages/Home';
import SubjectSelection from './pages/SubjectSelection';
import './styles/global.css';

export default function App() {
  const [selectedSubject, setSelectedSubject] = useState(null);

  if (!selectedSubject) {
    return (
      <Layout>
        <SubjectSelection onSelectSubject={setSelectedSubject} />
      </Layout>
    );
  }

  return (
    <Layout subject={selectedSubject} onChangeSubject={() => setSelectedSubject(null)}>
      <Home 
        subject={selectedSubject} 
        onChangeSubject={() => setSelectedSubject(null)}
      />
    </Layout>
  );
}
