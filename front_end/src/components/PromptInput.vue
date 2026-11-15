<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue';

const props = defineProps<{ disabled?: boolean; modelValue: string }>();

const emit = defineEmits<{
	'update:modelValue': [value: string];
	submit: [];
}>();

const textarea = ref<HTMLTextAreaElement | null>(null);
const MAX_HEIGHT = 200;

function resize() {
	const el = textarea.value;
	if (!el) return;
	el.style.height = 'auto';
	el.style.height = `${Math.min(el.scrollHeight, MAX_HEIGHT)}px`;
}

function onInput(event: Event) {
	emit('update:modelValue', (event.target as HTMLTextAreaElement).value);
	resize();
}

function trySubmit() {
	if (props.disabled || !props.modelValue.trim()) return;
	emit('submit');
	nextTick(resize);
}

function onKeydown(event: KeyboardEvent) {
	// Enter envia; Shift+Enter quebra linha. Ignora Enter durante composição (IME).
	if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
		event.preventDefault();
		trySubmit();
	}
}

function focus() {
	textarea.value?.focus();
}

onMounted(focus);
defineExpose({ focus, resize });
</script>

<template>
	<form class="composer" @submit.prevent="trySubmit">
		<textarea ref="textarea" class="composer__field" rows="1"
			placeholder="Descreva o problema ou cole um trecho de log…" aria-label="Prompt" :value="modelValue"
			@input="onInput" @keydown="onKeydown" />

		<div class="composer__bar">
			<div class="composer__left">
				<button type="button" class="composer__attach" title="Anexar arquivo .log"
					aria-label="Anexar arquivo .log">
					<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
						stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
						<path
							d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48" />
					</svg>
				</button>

				<span class="composer__hint">
					<kbd>Enter</kbd> envia · <kbd>Shift</kbd> + <kbd>Enter</kbd> nova linha
				</span>
			</div>
			<button type="submit" class="composer__send" :disabled="disabled || !modelValue.trim()">
				Enviar
			</button>
		</div>
	</form>
</template>

<style scoped>
.composer {
	max-width: 760px;
	margin: 0 auto;
	padding: 0.65rem 0.65rem 0.55rem 0.9rem;
	background-color: var(--surface);
	border: 1px solid var(--border);
	border-radius: var(--radius-lg);
	transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.composer:focus-within {
	border-color: var(--accent);
	box-shadow: 0 0 0 3px var(--accent-soft);
}

.composer__field {
	display: block;
	width: 100%;
	max-height: 200px;
	padding: 0.2rem 0;
	border: none;
	background: none;
	resize: none;
	font-family: var(--font-mono);
	font-size: 0.9rem;
	line-height: 1.55;
}

.composer__field:focus {
	outline: none;
}

.composer__field::placeholder {
	color: var(--muted);
}

.composer__bar {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.75rem;
	margin-top: 0.4rem;
}

.composer__left {
	min-width: 0;
	display: flex;
	align-items: center;
	gap: 0.6rem;
}

.composer__attach {
	flex-shrink: 0;
	width: 2rem;
	height: 2rem;
	display: flex;
	align-items: center;
	justify-content: center;
	border: none;
	border-radius: var(--radius-sm);
	background: none;
	color: var(--muted);
	transition: background-color 0.15s ease, color 0.15s ease;
}

.composer__attach:hover {
	background-color: var(--surface-hover);
	color: var(--accent);
}

.composer__hint {
	font-size: 0.74rem;
	color: var(--muted);
}

.composer__hint kbd {
	padding: 0 0.3rem;
	font-family: var(--font-mono);
	font-size: 0.7rem;
	border: 1px solid var(--border);
	border-radius: 4px;
	background-color: var(--surface-hover);
}

.composer__send {
	flex-shrink: 0;
	padding: 0.4rem 1rem;
	border: none;
	border-radius: var(--radius);
	background-color: var(--accent);
	color: var(--accent-contrast);
	font-size: 0.85rem;
	font-weight: 600;
	transition: background-color 0.15s ease, opacity 0.15s ease;
}

.composer__send:not(:disabled):hover {
	background-color: var(--accent-hover);
}

.composer__send:disabled {
	opacity: 0.4;
	cursor: not-allowed;
}

@media (max-width: 480px) {
	.composer__hint {
		display: none;
	}
}
</style>
