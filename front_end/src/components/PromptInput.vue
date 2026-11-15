<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'

const props = defineProps<{ disabled?: boolean; modelValue: string }>()

const emit = defineEmits<{
	'update:modelValue': [value: string]
	submit: []
}>()

const textarea = ref<HTMLTextAreaElement | null>(null)
const MAX_HEIGHT = 200

function resize() {
	const el = textarea.value
	if (!el) return
	el.style.height = 'auto'
	el.style.height = `${Math.min(el.scrollHeight, MAX_HEIGHT)}px`
}

function onInput(event: Event) {
	emit('update:modelValue', (event.target as HTMLTextAreaElement).value)
	resize()
}

function trySubmit() {
	if (props.disabled || !props.modelValue.trim()) return
	emit('submit')
	nextTick(resize)
}

function onKeydown(event: KeyboardEvent) {
	// Enter envia; Shift+Enter quebra linha. Ignora Enter durante composição (IME).
	if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
		event.preventDefault()
		trySubmit()
	}
}

function focus() {
	textarea.value?.focus()
}

onMounted(focus)
defineExpose({ focus, resize })
</script>

<template>
	<form class="prompt" @submit.prevent="trySubmit">
		<span class="prompt__marker" aria-hidden="true">&gt;</span>
		<textarea ref="textarea" class="prompt__field" rows="1" placeholder="Escreva seu prompt…" aria-label="Prompt"
			:value="modelValue" @input="onInput" @keydown="onKeydown" />
		<button type="submit" class="prompt__send" :disabled="disabled || !modelValue.trim()"
			aria-label="Enviar prompt">
			↑
		</button>
	</form>
	<p class="prompt__hint">Enter para enviar · Shift+Enter para nova linha</p>
</template>

<style scoped>
.prompt {
	display: flex;
	align-items: flex-end;
	gap: 0.6rem;
	padding: 0.65rem 0.65rem 0.65rem 1rem;
	background-color: var(--surface);
	border: 1px solid var(--border);
	border-radius: 14px;
	box-shadow: var(--shadow);
	transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.prompt:focus-within {
	border-color: var(--accent);
}

.prompt__marker {
	padding-bottom: 0.3rem;
	font-family: var(--font-mono);
	font-weight: 700;
	color: var(--accent);
}

.prompt__field {
	flex: 1;
	min-width: 0;
	max-height: 200px;
	padding: 0.3rem 0;
	border: none;
	background: none;
	resize: none;
	font-family: var(--font-mono);
	font-size: 0.95rem;
	line-height: 1.5;
}

.prompt__field:focus {
	outline: none;
}

.prompt__field::placeholder {
	color: var(--muted);
}

.prompt__send {
	flex-shrink: 0;
	width: 2.25rem;
	height: 2.25rem;
	border: none;
	border-radius: 10px;
	background-color: var(--accent);
	color: var(--accent-contrast);
	font-size: 1.1rem;
	font-weight: 700;
	transition: background-color 0.15s ease, opacity 0.15s ease;
}

.prompt__send:not(:disabled):hover {
	background-color: var(--accent-hover);
}

.prompt__send:disabled {
	opacity: 0.4;
	cursor: not-allowed;
}

.prompt__hint {
	margin-top: 0.5rem;
	text-align: center;
	font-size: 0.75rem;
	color: var(--muted);
}
</style>
