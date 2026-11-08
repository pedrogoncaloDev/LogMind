import httpClient from './httpClient'
import type { LoginCredentials, TokenResponse } from '@/types/auth'

export async function login(credentials: LoginCredentials): Promise<TokenResponse> {
  const { data } = await httpClient.post<TokenResponse>('/users/login', credentials)
  return data
}
