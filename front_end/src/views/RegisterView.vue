<script setup lang="ts">
import { computed, reactive, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import AuthLayout from '@/components/AuthLayout.vue';
import BaseInput from '@/components/BaseInput.vue';
import BasePasswordInput from '@/components/BasePasswordInput.vue';
import BaseButton from '@/components/BaseButton.vue';
import { useAuthStore } from '@/stores/auth';
import { extractErrorMessage } from '@/utils/errors';

const MIN_PASSWORD_LENGTH = 8;

const router = useRouter();
const authStore = useAuthStore();

const form = reactive({ name: '', email: '', password: '', confirmPassword: '' });
const touched = reactive({ password: false, confirmPassword: false });
const errorMessage = ref('');
const isSubmitting = ref(false);

const passwordError = computed(() =>
	touched.password && form.password.length < MIN_PASSWORD_LENGTH
		? `A senha deve ter pelo menos ${MIN_PASSWORD_LENGTH} caracteres.`
		: '',
);

const confirmError = computed(() =>
	touched.confirmPassword && form.confirmPassword !== form.password
		? 'As senhas não coincidem.'
		: '',
);

const canSubmit = computed(
	() =>
		form.name.trim().length > 0 &&
		form.email.trim().length > 0 &&
		form.password.length >= MIN_PASSWORD_LENGTH &&
		form.confirmPassword === form.password,
);

async function handleSubmit() {
	touched.password = true;
	touched.confirmPassword = true;
	if (!canSubmit.value) return;

	errorMessage.value = '';
	isSubmitting.value = true;
	try {
		await authStore.register({
			name: form.name.trim(),
			email: form.email.trim(),
			password: form.password,
		});
		router.push('/');
	} catch (error) {
		errorMessage.value = extractErrorMessage(error, 'Não foi possível criar a conta. Tente novamente.');
	} finally {
		isSubmitting.value = false;
	}
}
</script>

<template>
	<AuthLayout title="Crie sua conta" subtitle="Cadastre-se para começar a conversar.">
		<form class="auth-form" novalidate @submit.prevent="handleSubmit">
			<BaseInput id="name" v-model="form.name" label="Nome" placeholder="Seu nome" autocomplete="name" required />

			<BaseInput id="email" v-model="form.email" type="email" label="Email" placeholder="seu@email.com"
				autocomplete="email" required />

			<BasePasswordInput id="password" v-model="form.password" label="Senha" autocomplete="new-password"
				:error="passwordError" required @focusout="touched.password = true" />

			<BasePasswordInput id="confirm-password" v-model="form.confirmPassword" label="Confirmar senha"
				autocomplete="new-password" :error="confirmError" required @focusout="touched.confirmPassword = true" />

			<p v-if="errorMessage" class="auth-form__error" role="alert">{{ errorMessage }}</p>

			<BaseButton type="submit" :loading="isSubmitting">Criar conta</BaseButton>
		</form>

		<template #footer>
			Já tem conta? <RouterLink to="/login">Entrar</RouterLink>
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
