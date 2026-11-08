<script setup lang="ts">
defineOptions({ inheritAttrs: false })

withDefaults(
  defineProps<{
    modelValue?: string
    label?: string
    type?: string
    error?: string
    id?: string
  }>(),
  {
    modelValue: '',
    type: 'text',
  },
)

defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <div class="base-input">
    <label v-if="label" :for="id" class="base-input__label">{{ label }}</label>

    <div class="base-input__control">
      <input
        :id="id"
        :type="type"
        :value="modelValue"
        class="base-input__field"
        :class="{
          'base-input__field--error': !!error,
          'base-input__field--with-suffix': !!$slots.suffix,
        }"
        v-bind="$attrs"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
      <span v-if="$slots.suffix" class="base-input__suffix">
        <slot name="suffix" />
      </span>
    </div>

    <p v-if="error" class="base-input__error">{{ error }}</p>
  </div>
</template>

<style scoped>
.base-input {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  text-align: left;
}

.base-input__label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #374151;
}

.base-input__control {
  position: relative;
  display: flex;
  align-items: center;
}

.base-input__field {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #111827;
  background-color: #fff;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.base-input__field--with-suffix {
  padding-right: 4.5rem;
}

.base-input__field:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.base-input__field--error {
  border-color: #dc2626;
}

.base-input__suffix {
  position: absolute;
  right: 0.5rem;
  display: flex;
  align-items: center;
}

.base-input__error {
  margin: 0;
  font-size: 0.8rem;
  color: #dc2626;
}
</style>
