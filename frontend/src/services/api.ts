import type { Question, SurveyResponse, AnalysisResult } from '../types/survey';

import { config } from '../config';

const API_BASE_URL = config.API_BASE_URL;

export async function fetchQuestions() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/survey/questions`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching questions:', error);
        throw error;
    }
}

export async function submitSurveyAndGetAnalysis(answers: string[]) {
    try {
        console.log('Submitting answers:', answers);
        const response = await fetch(`${API_BASE_URL}/survey/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answers }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('API Response:', data);
        return data;
    } catch (error) {
        console.error('Error submitting survey:', error);
        throw error;
    }
}
