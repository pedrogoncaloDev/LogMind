<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseInput from '@/components/BaseInput.vue'
import BasePasswordInput from '@/components/BasePasswordInput.vue'
import BaseButton from '@/components/BaseButton.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
})

const errorMessage = ref('')
const isSubmitting = ref(false)

function extractErrorMessage(error: unknown): string {
  if (typeof error === 'object' && error !== null && 'response' in error) {
    const response = (error as { response?: { data?: { detail?: string } } }).response
    if (response?.data?.detail) return response.data.detail
  }
  return 'Não foi possível fazer login. Tente novamente.'
}

async function handleSubmit() {
  errorMessage.value = ''
  isSubmitting.value = true
  try {
    await authStore.login({ email: form.email, password: form.password })
    router.push('/')
  } catch (error) {
    errorMessage.value = extractErrorMessage(error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="login-view">
    <form class="login-card" @submit.prevent="handleSubmit">
      <h1 class="login-card__title">LogMind</h1>
      <p class="login-card__subtitle">Acesse sua conta</p>

      <BaseInput
        id="email"
        v-model="form.email"
        type="email"
        label="Email"
        placeholder="seu@email.com"
        autocomplete="email"
        required
      />

      <BasePasswordInput id="password" v-model="form.password" label="Senha" required />

      <p v-if="errorMessage" class="login-card__error">{{ errorMessage }}</p>

      <BaseButton type="submit" :loading="isSubmitting">Entrar</BaseButton>
    </form>
  </div>
</template>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f3f4f6;
  padding: 1.5rem;
}

.login-card {
  width: 100%;
  max-width: 360px;
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  background-color: #fff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.login-card__title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  text-align: center;
}

.login-card__subtitle {
  margin: -0.6rem 0 0;
  font-size: 0.9rem;
  color: #6b7280;
  text-align: center;
}

.login-card__error {
  margin: 0;
  font-size: 0.85rem;
  color: #dc2626;
  text-align: center;
}
</style>
