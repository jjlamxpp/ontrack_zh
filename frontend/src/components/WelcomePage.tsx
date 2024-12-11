import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import { Button } from '@/components/ui/button';

export const WelcomePage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Clear any previous results when landing on welcome page
    localStorage.removeItem('analysisResult');
    localStorage.removeItem('surveyAnswers');
  }, []);

  return (
    <main className="min-h-screen bg-[#1B2541] text-white flex flex-col items-center justify-center p-4">
      <div className="max-w-2xl w-full text-center space-y-8">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold">
            <span className="text-[#3B82F6]">On</span>Track
          </h1>
          <p className="text-lg">
            透過我們的職業興趣測驗，探索最適合你的職業方向。
          </p>
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold">使用步驟</h2>
          <div className="flex flex-col items-center space-y-2">
            <div className="text-left max-w-md">
              <p>1. 參加測驗：回答40個簡單問題，了解你的興趣和技能。</p>
              <p>2. 獲取報告：收到一份詳細的職業偏好分析報告。</p>
              <p>3. 規劃路徑：利用專家建議探索職業並規劃下一步。</p>
            </div>
          </div>
        </div>

        <Button 
          size="lg"
          className="bg-[#3B82F6] hover:bg-[#2563EB] text-white text-xl px-12 py-6 rounded-full relative"
          onClick={() => navigate('/survey/1')}
        >
          <span className="relative z-10">開始測驗</span>
          <div className="absolute inset-0 rounded-full bg-[#3B82F6] blur-lg opacity-50" />
        </Button>
      </div>
    </main>
  );
};