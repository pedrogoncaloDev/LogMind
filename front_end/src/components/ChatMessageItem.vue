<script setup lang="ts">
import type { ChatMessage } from '@/types/chat'

defineProps<{ message: ChatMessage }>()
</script>

<template>
	<article class="message" :class="`message--${message.role}`">
		<span class="message__marker" aria-hidden="true">{{ message.role === 'user' ? '>' : '●' }}</span>
		<div class="message__body">
			<span class="message__author">{{ message.role === 'user' ? 'Você' : 'LogMind' }}</span>
			<p class="message__content">{{ message.content }}</p>
		</div>
	</article>
</template>

<style scoped>
.message {
	display: flex;
	gap: 0.75rem;
	align-items: flex-start;
}

.message__marker {
	flex-shrink: 0;
	width: 1.25rem;
	font-family: var(--font-mono);
	font-weight: 700;
	line-height: 1.5;
	color: var(--accent);
}

.message--user .message__marker {
	color: var(--muted);
}

.message__body {
	min-width: 0;
	display: flex;
	flex-direction: column;
	gap: 0.15rem;
}

.message__author {
	font-size: 0.75rem;
	font-weight: 600;
	text-transform: uppercase;
	letter-spacing: 0.04em;
	color: var(--muted);
}

.message__content {
	white-space: pre-wrap;
	overflow-wrap: anywhere;
}

.message--user .message__content {
	font-family: var(--font-mono);
	font-size: 0.92rem;
}
</style>
