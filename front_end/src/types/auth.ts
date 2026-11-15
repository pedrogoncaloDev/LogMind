export interface LoginCredentials {
	email: string
	password: string
}

export interface RegisterPayload {
	name: string
	email: string
	password: string
}

export interface TokenResponse {
	access_token: string
	token_type: string
	refresh_token: string
}

export interface AuthUser {
	id: string
	email: string
}
