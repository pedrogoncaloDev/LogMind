<script setup lang="ts">
import { computed } from 'vue';
import BrandMark from './BrandMark.vue';
import type { ChatMessage } from '@/types/chat';

const props = defineProps<{ message: ChatMessage }>();

const isUser = computed(() => props.message.role === 'user');
const time = computed(() =>
	new Date(props.message.createdAt).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
);
</script>

<template>
	<article class="message" :class="isUser ? 'message--user' : 'message--assistant'">
		<BrandMark v-if="!isUser" :size="28" class="message__avatar" />

		<div class="message__main">
			<p class="message__bubble">{{ message.content }}</p>
			<time class="message__time" :datetime="message.createdAt">{{ isUser ? 'Você' : 'LogMind' }} · {{ time
				}}</time>
		</div>
	</article>
</template>

<style scoped>
.message {
	display: flex;
	gap: 0.75rem;
	align-items: flex-start;
}

.message--user {
	justify-content: flex-end;
}

.message__avatar {
	margin-top: 2px;
}

.message__main {
	min-width: 0;
	max-width: min(100%, 640px);
	display: flex;
	flex-direction: column;
	gap: 0.3rem;
}

.message--user .message__main {
	align-items: flex-end;
	max-width: min(85%, 560px);
}

.message__bubble {
	padding: 0.7rem 0.95rem;
	white-space: pre-wrap;
	overflow-wrap: anywhere;
	border: 1px solid var(--border);
	border-radius: var(--radius-lg);
	background-color: var(--surface);
}

.message--assistant .message__bubble {
	border-top-left-radius: var(--radius-sm);
}

.message--user .message__bubble {
	border-color: color-mix(in srgb, var(--accent) 35%, transparent);
	border-top-right-radius: var(--radius-sm);
	background-color: var(--accent-soft);
}

.message__time {
	font-size: 0.72rem;
	color: var(--muted);
}
</style>
