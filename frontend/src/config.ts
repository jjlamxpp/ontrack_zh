interface Config {
  API_BASE_URL: string;
  LOCAL_API_URL: string;
}

export const config: Config = {
  API_BASE_URL: import.meta.env.VITE_API_URL || 'https://ontrack-zh.onrender.com',
  LOCAL_API_URL: 'http://localhost:8000'
};

// You can add more configuration options here
export const isDevelopment = import.meta.env.DEV;
export const isProduction = import.meta.env.PROD;
