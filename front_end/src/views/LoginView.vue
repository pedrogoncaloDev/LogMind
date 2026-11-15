<script setup lang="ts">
import { reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import AuthLayout from '@/components/AuthLayout.vue'
import BaseInput from '@/components/BaseInput.vue'
import BasePasswordInput from '@/components/BasePasswordInput.vue'
import BaseButton from '@/components/BaseButton.vue'
import { useAuthStore } from '@/stores/auth'
import { extractErrorMessage } from '@/utils/errors'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({ email: '', password: '' })
const errorMessage = ref('')
const isSubmitting = ref(false)

async function handleSubmit() {
	errorMessage.value = ''
	isSubmitting.value = true
	try {
		await authStore.login({ email: form.email.trim(), password: form.password })
		router.push('/')
	} catch (error) {
		errorMessage.value = extractErrorMessage(error, 'Não foi possível fazer login. Tente novamente.')
	} finally {
		isSubmitting.value = false
	}
}
</script>

<template>
	<AuthLayout title="Bem-vindo de volta" subtitle="Entre na sua conta para continuar.">
		<form class="auth-form" @submit.prevent="handleSubmit">
			<BaseInput id="email" v-model="form.email" type="email" label="Email" placeholder="seu@email.com"
				autocomplete="email" required />

			<BasePasswordInput id="password" v-model="form.password" label="Senha" required />

			<p v-if="errorMessage" class="auth-form__error" role="alert">{{ errorMessage }}</p>

			<BaseButton type="submit" :loading="isSubmitting">Entrar</BaseButton>
		</form>

		<template #footer>
			Não tem conta? <RouterLink to="/register">Cadastre-se</RouterLink>
		</template>
	</AuthLayout>
</template>

<style scoped>
.auth-form {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.auth-form__error {
	font-size: 0.85rem;
	color: var(--danger);
}
</style>
