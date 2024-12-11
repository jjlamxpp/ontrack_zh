import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { WelcomePage } from './components/WelcomePage';
import { SurveyPage } from './components/SurveyPage';
import { CareerAnalysis } from './components/result/CareerAnalysis';
import { useEffect } from 'react';

function App() {
  // Clear localStorage on initial load
  useEffect(() => {
    const handleBeforeUnload = () => {
      localStorage.removeItem('analysisResult');
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<WelcomePage />} />
        <Route path="/survey/:questionId" element={<SurveyPage />} />
        <Route 
          path="/result" 
          element={
            <RequireAnalysis>
              <CareerAnalysis />
            </RequireAnalysis>
          } 
        />
        {/* Catch all other routes and redirect to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

function RequireAnalysis({ children }: { children: React.ReactNode }) {
  const result = localStorage.getItem('analysisResult');
  
  try {
    if (!result) {
      console.log('No analysis result found, redirecting to home');
      return <Navigate to="/" replace />;
    }
    const parsedResult = JSON.parse(result);
    if (!parsedResult || !parsedResult.personality || !parsedResult.industries) {
      console.log('Invalid analysis result format, redirecting to home');
      localStorage.removeItem('analysisResult');
      return <Navigate to="/" replace />;
    }
  } catch (error) {
    console.error('Error in RequireAnalysis:', error);
    localStorage.removeItem('analysisResult');
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}

export default App;
