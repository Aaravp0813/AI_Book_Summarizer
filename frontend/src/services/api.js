/**
 * API Service for NCERT AI Tutor
 * Communicates with FastAPI backend at http://127.0.0.1:8000
 */

const API_BASE_URL = 'aibooksummarizer-production.up.railway.app';

/**
 * Ask a question to the tutor
 * @param {string} subject - The selected subject (science, maths, social_science, english)
 * @param {string} question - The student's question
 * @returns {Promise<{question: string, answer: string}>}
 * @throws {Error} If the request fails or server returns an error
 */
export async function askQuestion(subject, question) {
  try {
    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        subject: subject.trim(),
        question: question.trim() 
      }),
    });

    // Parse the response body once
    const data = await response.json();

    // Handle HTTP error responses
    if (!response.ok) {
      const errorMessage = data.detail || `Server error: ${response.status}`;
      throw new Error(errorMessage);
    }

    // Return the successful response
    return {
      question: data.question,
      answer: data.answer,
    };
  } catch (error) {
    // Network errors and other issues
    if (error instanceof TypeError) {
      throw new Error(
        'Cannot connect to the tutor server. Make sure the FastAPI backend is running at http://127.0.0.1:8000'
      );
    }

    // Re-throw the error (could be from the server)
    throw error;
  }
}
