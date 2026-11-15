<script setup lang="ts">
defineOptions({ inheritAttrs: false });

withDefaults(
	defineProps<{
		modelValue?: string;
		label?: string;
		type?: string;
		error?: string;
		id?: string;
	}>(),
	{
		modelValue: '',
		type: 'text',
	},
);

defineEmits<{ 'update:modelValue': [value: string] }>();
</script>

<template>
	<div class="base-input">
		<label v-if="label" :for="id" class="base-input__label">{{ label }}</label>

		<div class="base-input__control">
			<input :id="id" :type="type" :value="modelValue" class="base-input__field" :class="{
				'base-input__field--error': !!error,
				'base-input__field--with-suffix': !!$slots.suffix,
			}" :aria-invalid="!!error" v-bind="$attrs"
				@input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)" />
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
	color: var(--text);
}

.base-input__control {
	position: relative;
	display: flex;
	align-items: center;
}

.base-input__field {
	width: 100%;
	padding: 0.65rem 0.8rem;
	border: 1px solid var(--border);
	border-radius: var(--radius);
	font-size: 0.95rem;
	color: var(--text);
	background-color: var(--surface);
	transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.base-input__field::placeholder {
	color: var(--muted);
}

.base-input__field--with-suffix {
	padding-right: 5rem;
}

.base-input__field:focus {
	outline: none;
	border-color: var(--accent);
	box-shadow: 0 0 0 3px var(--accent-soft);
}

.base-input__field--error {
	border-color: var(--danger);
}

.base-input__suffix {
	position: absolute;
	right: 0.5rem;
	display: flex;
	align-items: center;
}

.base-input__error {
	font-size: 0.8rem;
	color: var(--danger);
}
</style>
