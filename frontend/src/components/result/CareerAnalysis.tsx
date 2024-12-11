"use client"

import React, { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { CareerPersonalityAnalysis } from "./CareerPersonalityAnalysis"
import { RecommendedIndustry } from "./RecommendedIndustry"
import type { AnalysisResult } from '../../types/survey'
import { config } from '../../config';

export function CareerAnalysis() {
  const navigate = useNavigate();
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [activeSession, setActiveSession] = useState<'personality' | 'industry'>('personality');

  useEffect(() => {
    const savedResult = localStorage.getItem('analysisResult');
    if (!savedResult) {
      navigate('/', { replace: true });
      return;
    }

    try {
      const parsedResult = JSON.parse(savedResult);
      if (!parsedResult || !parsedResult.personality || !parsedResult.industries) {
        throw new Error('Invalid analysis result format');
      }
      setResult(parsedResult);
    } catch (error) {
      console.error('Error parsing analysis result:', error);
      navigate('/', { replace: true });
    }
  }, [navigate]);

  useEffect(() => {
    // Add event listener for page refresh
    const handleBeforeUnload = () => {
      localStorage.removeItem('analysisResult');
      navigate('/');
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    // Cleanup
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, [navigate]);

  if (!result) {
    return (
      <div className="min-h-screen w-full bg-[#1B2541] text-white flex items-center justify-center">
        <div className="text-center">
          <div className="text-xl mb-4">正在加載結果...</div>
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full bg-[#1B2541] text-white">
      <div className="text-center pt-8">
        <h1 className="text-4xl font-bold">
          <span className="text-[#3B82F6]">On</span>
          <span className="text-white">Track</span>
        </h1>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center gap-4 mb-8">
          <button
            className={`px-6 py-3 rounded-full transition-colors ${
              activeSession === 'personality'
                ? 'bg-[#3B82F6] text-white'
                : 'bg-white/10 hover:bg-white/20'
            }`}
            onClick={() => setActiveSession('personality')}
          >
            個人特質分析
          </button>
          <button
            className={`px-6 py-3 rounded-full transition-colors ${
              activeSession === 'industry'
                ? 'bg-[#3B82F6] text-white'
                : 'bg-white/10 hover:bg-white/20'
            }`}
            onClick={() => setActiveSession('industry')}
          >
            推薦行業
          </button>
        </div>

        {activeSession === 'personality' ? (
          <CareerPersonalityAnalysis analysis={result.personality} />
        ) : (
          <RecommendedIndustry industries={result.industries} />
        )}
      </div>
    </div>
  );
}
