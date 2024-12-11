interface Config {
  API_BASE_URL: string;
}

export const config: Config = {
  API_BASE_URL: import.meta.env.VITE_API_URL || 'https://ontrack-zh.onrender.com'
};
