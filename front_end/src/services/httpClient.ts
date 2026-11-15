import axios, { type InternalAxiosRequestConfig } from 'axios';
import { tokenStorage } from './tokenStorage';
import type { TokenResponse } from '@/types/auth';

const baseURL = import.meta.env.VITE_API_BASE_URL;

const httpClient = axios.create({
	baseURL,
	headers: {
		'Content-Type': 'application/json',
	},
});

const AUTH_ROUTES = ['/users/login', '/users/token/refresh'];

type RetriableConfig = InternalAxiosRequestConfig & { _retry?: boolean };

let refreshing: Promise<string> | null = null;

async function refreshAccessToken(): Promise<string> {
	const refreshToken = tokenStorage.getRefresh();
	if (!refreshToken) throw new Error('Sem refresh token');

	// axios "puro" para não cair nos interceptors e entrar em loop.
	const { data } = await axios.post<TokenResponse>(`${baseURL}/users/token/refresh`, {
		refresh_token: refreshToken,
	});
	tokenStorage.set(data.access_token, data.refresh_token);
	return data.access_token;
}

httpClient.interceptors.request.use((config) => {
	const token = tokenStorage.getAccess();
	if (token) config.headers.Authorization = `Bearer ${token}`;
	return config;
});

httpClient.interceptors.response.use(
	(response) => response,
	async (error) => {
		const original = error.config as RetriableConfig | undefined;
		const isAuthRoute = AUTH_ROUTES.some((route) => original?.url?.startsWith(route));

		if (error.response?.status === 401 && original && !original._retry && !isAuthRoute) {
			original._retry = true;
			try {
				refreshing ??= refreshAccessToken().finally(() => {
					refreshing = null;
				});
				const token = await refreshing;
				original.headers.Authorization = `Bearer ${token}`;
				return httpClient(original);
			} catch {
				tokenStorage.clear();
				window.location.assign('/login');
			}
		}

		return Promise.reject(error);
	},
);

export default httpClient;
