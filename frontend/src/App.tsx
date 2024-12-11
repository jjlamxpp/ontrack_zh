import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { WelcomePage } from './components/WelcomePage';
import { SurveyPage } from './components/SurveyPage';
import { CareerAnalysis } from './components/result/CareerAnalysis';

function App() {
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
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

function RequireAnalysis({ children }: { children: React.ReactNode }) {
  const result = localStorage.getItem('analysisResult');
  
  try {
    if (!result) {
      throw new Error('No analysis result found');
    }
    const parsedResult = JSON.parse(result);
    if (!parsedResult || !parsedResult.personality || !parsedResult.industries) {
      throw new Error('Invalid analysis result format');
    }
  } catch (error) {
    console.error('Error in RequireAnalysis:', error);
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}

export default App;
