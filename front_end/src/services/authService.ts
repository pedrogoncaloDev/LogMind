import httpClient from './httpClient';
import type { LoginCredentials, RegisterPayload, TokenResponse } from '@/types/auth';

export async function login(credentials: LoginCredentials): Promise<TokenResponse> {
	const { data } = await httpClient.post<TokenResponse>('/users/login', credentials);
	return data;
}

export async function register(payload: RegisterPayload): Promise<void> {
	await httpClient.post('/users', payload);
}
