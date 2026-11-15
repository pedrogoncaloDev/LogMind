<script setup lang="ts">
withDefaults(
	defineProps<{
		type?: 'button' | 'submit' | 'reset'
		variant?: 'primary' | 'secondary'
		disabled?: boolean
		loading?: boolean
	}>(),
	{
		type: 'button',
		variant: 'primary',
		disabled: false,
		loading: false,
	},
)
</script>

<template>
	<button :type="type" :class="['base-button', `base-button--${variant}`]" :disabled="disabled || loading">
		<span v-if="loading" class="base-button__spinner" aria-hidden="true" />
		<slot />
	</button>
</template>

<style scoped>
.base-button {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	width: 100%;
	padding: 0.7rem 1rem;
	border-radius: var(--radius);
	border: 1px solid transparent;
	font-size: 0.95rem;
	font-weight: 600;
	transition: background-color 0.15s ease, opacity 0.15s ease;
}

.base-button:disabled {
	cursor: not-allowed;
	opacity: 0.6;
}

.base-button--primary {
	background-color: var(--accent);
	color: var(--accent-contrast);
}

.base-button--primary:not(:disabled):hover {
	background-color: var(--accent-hover);
}

.base-button--secondary {
	background-color: transparent;
	color: var(--text);
	border-color: var(--border);
}

.base-button--secondary:not(:disabled):hover {
	background-color: var(--surface-hover);
}

.base-button__spinner {
	width: 14px;
	height: 14px;
	border: 2px solid currentColor;
	border-right-color: transparent;
	border-radius: 50%;
	animation: base-button-spin 0.6s linear infinite;
}

@keyframes base-button-spin {
	to {
		transform: rotate(360deg);
	}
}
</style>
