<script setup lang="ts">
import { ref, computed } from 'vue'
import BaseInput from './BaseInput.vue'

withDefaults(
  defineProps<{
    modelValue?: string
    label?: string
    error?: string
    id?: string
  }>(),
  {
    modelValue: '',
    label: 'Senha',
  },
)

defineEmits<{ 'update:modelValue': [value: string] }>()

const visible = ref(false)
const inputType = computed(() => (visible.value ? 'text' : 'password'))
</script>

<template>
  <BaseInput
    :id="id"
    :model-value="modelValue"
    :label="label"
    :type="inputType"
    :error="error"
    autocomplete="current-password"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <template #suffix>
      <button
        type="button"
        class="base-password-input__toggle"
        :aria-label="visible ? 'Ocultar senha' : 'Mostrar senha'"
        @click="visible = !visible"
      >
        {{ visible ? 'Ocultar' : 'Mostrar' }}
      </button>
    </template>
  </BaseInput>
</template>

<style scoped>
.base-password-input__toggle {
  background: none;
  border: none;
  color: #2563eb;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0 0.25rem;
  white-space: nowrap;
}

.base-password-input__toggle:hover {
  text-decoration: underline;
}
</style>
