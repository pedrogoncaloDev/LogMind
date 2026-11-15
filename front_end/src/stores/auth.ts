import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { login as loginRequest, register as registerRequest } from '@/services/authService'
import { tokenStorage } from '@/services/tokenStorage'
import { decodeAuthUser } from '@/utils/jwt'
import type { LoginCredentials, RegisterPayload } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
	const accessToken = ref<string | null>(tokenStorage.getAccess())
	const refreshToken = ref<string | null>(tokenStorage.getRefresh())

	const isAuthenticated = computed(() => !!accessToken.value)
	const user = computed(() => decodeAuthUser(accessToken.value ?? refreshToken.value))

	async function login(credentials: LoginCredentials) {
		const tokens = await loginRequest(credentials)
		accessToken.value = tokens.access_token
		refreshToken.value = tokens.refresh_token
		tokenStorage.set(tokens.access_token, tokens.refresh_token)
	}

	async function register(payload: RegisterPayload) {
		await registerRequest(payload)
		await login({ email: payload.email, password: payload.password })
	}

	function logout() {
		accessToken.value = null
		refreshToken.value = null
		tokenStorage.clear()
	}

	return { accessToken, refreshToken, isAuthenticated, user, login, register, logout }
})
