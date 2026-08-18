/**
 * Subject Configuration for NCERT AI Tutor
 * Centralized subject metadata and topic examples
 */

export const SUBJECTS = {
  science: {
    id: 'science',
    label: 'Science',
    description: 'NCERT Grade 8 Science',
    topics: [
      'What is force?',
      'Explain pressure.',
      'What is friction?',
      'How does sound travel?',
      'What is the function of the cell membrane?',
      'Explain photosynthesis.',
      'How is light reflected?',
      'What are chemical effects of electric current?',
    ],
  },
  maths: {
    id: 'maths',
    label: 'Mathematics',
    description: 'NCERT Grade 8 Mathematics',
    topics: [
      'What are rational numbers?',
      'Explain linear equations.',
      'How do we find square roots?',
      'What are cubes and cube roots?',
      'How do we compare quantities?',
      'What is mensuration?',
      'Explain algebraic expressions.',
      'What is the Pythagorean theorem?',
    ],
  },
  social_science: {
    id: 'social_science',
    label: 'Social Science',
    description: 'NCERT Grade 8 Social Science',
    topics: [
      'What is the Indian Constitution?',
      'Explain different types of resources.',
      'What are industries?',
      'What is human resources?',
      'Explain marginalisation.',
      'What is the Indian national movement?',
      'Explain the concept of democracy.',
      'What is sustainable development?',
    ],
  },
  english: {
    id: 'english',
    label: 'English',
    description: 'NCERT Grade 8 English',
    topics: [
      'What is a simile?',
      'Explain metaphors.',
      'What is onomatopoeia?',
      'Explain narrative writing.',
      'What is a haiku?',
      'What is personification?',
      'Explain the parts of a story.',
      'What is descriptive writing?',
    ],
  },
};

export const SUBJECT_IDS = Object.keys(SUBJECTS);

export function getSubject(id) {
  return SUBJECTS[id];
}

export function isValidSubject(id) {
  return SUBJECT_IDS.includes(id);
}
