/** Transport configuration reserved for the FastAPI integration. Mock services remain active for the demo. */
export const apiConfig = { baseUrl: import.meta.env.VITE_API_BASE_URL ?? '/api/v1', useMock: !import.meta.env.VITE_API_BASE_URL };
