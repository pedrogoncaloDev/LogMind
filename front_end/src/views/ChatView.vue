<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ChatSidebar from '@/components/ChatSidebar.vue'
import ChatMessageItem from '@/components/ChatMessageItem.vue'
import PromptInput from '@/components/PromptInput.vue'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

if (authStore.user) {
	chatStore.init(authStore.user.id)
} else {
	// Token ilegível: sessão inválida.
	authStore.logout()
	router.replace('/login')
}

const SUGGESTIONS = [
	'Explique o que significa este erro: ',
	'Resuma os principais warnings deste log: ',
	'Como investigar picos de latência nos logs?',
]

const draft = ref('')
const sidebarOpen = ref(false)
const scroller = ref<HTMLElement | null>(null)
const promptInput = ref<InstanceType<typeof PromptInput> | null>(null)

const chatId = computed(() => (typeof route.params.chatId === 'string' ? route.params.chatId : undefined))
const chat = computed(() => chatStore.getChat(chatId.value))
const isWaitingReply = computed(() => !!chat.value && chatStore.sendingChatId === chat.value.id)

// Link para um chat que não existe (apagado, ou de outro usuário): volta ao início.
watch(
	chatId,
	(id) => {
		if (id && !chatStore.getChat(id)) router.replace({ name: 'chat' })
	},
	{ immediate: true },
)

function scrollToBottom() {
	nextTick(() => {
		scroller.value?.scrollTo({ top: scroller.value.scrollHeight, behavior: 'smooth' })
	})
}

watch(() => [chat.value?.id, chat.value?.messages.length, isWaitingReply.value], scrollToBottom, {
	flush: 'post',
})

async function handleSubmit() {
	const text = draft.value.trim()
	if (!text) return

	const { chatId: usedId, reply } = chatStore.sendPrompt(text, chat.value?.id)
	draft.value = ''
	if (usedId !== chatId.value) router.push({ name: 'chat', params: { chatId: usedId } })
	await reply
}

function useSuggestion(text: string) {
	draft.value = text
	nextTick(() => {
		promptInput.value?.resize()
		promptInput.value?.focus()
	})
}

function newChat() {
	sidebarOpen.value = false
	draft.value = ''
	router.push({ name: 'chat' })
	nextTick(() => promptInput.value?.focus())
}

function handleDelete(id: string) {
	chatStore.deleteChat(id)
	if (id === chatId.value) router.replace({ name: 'chat' })
}

function handleLogout() {
	authStore.logout()
	chatStore.reset()
	router.push('/login')
}
</script>

<template>
	<div class="chat-view">
		<ChatSidebar :chats="chatStore.sortedChats" :active-chat-id="chat?.id" :user-email="authStore.user?.email ?? ''"
			:open="sidebarOpen" @new-chat="newChat" @delete-chat="handleDelete" @logout="handleLogout"
			@close="sidebarOpen = false" />

		<main class="chat-main">
			<header class="chat-main__bar">
				<button type="button" class="chat-main__menu" aria-label="Abrir lista de chats"
					@click="sidebarOpen = true">
					☰
				</button>
				<h1 class="chat-main__title">{{ chat?.title ?? 'Novo chat' }}</h1>
			</header>

			<div ref="scroller" class="chat-main__scroll">
				<section v-if="!chat" class="empty">
					<p class="empty__mark" aria-hidden="true">&gt;_</p>
					<h2 class="empty__title">O que vamos analisar hoje?</h2>
					<p class="empty__text">Escreva um prompt abaixo para começar uma nova conversa.</p>
					<div class="empty__suggestions">
						<button v-for="suggestion in SUGGESTIONS" :key="suggestion" type="button" class="empty__chip"
							@click="useSuggestion(suggestion)">
							{{ suggestion.trim() }}
						</button>
					</div>
				</section>

				<section v-else class="messages" aria-live="polite">
					<ChatMessageItem v-for="message in chat.messages" :key="message.id" :message="message" />

					<div v-if="isWaitingReply" class="thinking" role="status">
						<span class="thinking__marker" aria-hidden="true">●</span>
						<span class="thinking__dots" aria-hidden="true"><i /><i /><i /></span>
						<span class="thinking__sr">LogMind está respondendo…</span>
					</div>
				</section>
			</div>

			<footer class="chat-main__footer">
				<PromptInput ref="promptInput" v-model="draft" :disabled="isWaitingReply" @submit="handleSubmit" />
			</footer>
		</main>
	</div>
</template>

<style scoped>
.chat-view {
	display: flex;
	height: 100%;
}

.chat-main {
	flex: 1;
	min-width: 0;
	display: flex;
	flex-direction: column;
}

.chat-main__bar {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	padding: 0.75rem 1.25rem;
	border-bottom: 1px solid var(--border);
}

.chat-main__menu {
	display: none;
	padding: 0.25rem 0.55rem;
	border: 1px solid var(--border);
	border-radius: 8px;
	background: none;
	font-size: 1.1rem;
	line-height: 1.2;
}

.chat-main__title {
	font-size: 0.95rem;
	font-weight: 600;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.chat-main__scroll {
	flex: 1;
	min-height: 0;
	overflow-y: auto;
	padding: 1.5rem 1.25rem;
}

.chat-main__footer {
	width: 100%;
	max-width: 800px;
	margin: 0 auto;
	padding: 0.5rem 1.25rem 1rem;
}

.messages {
	max-width: 760px;
	margin: 0 auto;
	display: flex;
	flex-direction: column;
	gap: 1.5rem;
}

.empty {
	max-width: 560px;
	min-height: 100%;
	margin: 0 auto;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 0.6rem;
	text-align: center;
}

.empty__mark {
	font-family: var(--font-mono);
	font-size: 2rem;
	font-weight: 700;
	color: var(--accent);
}

.empty__title {
	font-size: 1.6rem;
	line-height: 1.2;
}

.empty__text {
	color: var(--muted);
}

.empty__suggestions {
	margin-top: 1rem;
	display: flex;
	flex-wrap: wrap;
	justify-content: center;
	gap: 0.5rem;
}

.empty__chip {
	padding: 0.45rem 0.85rem;
	border: 1px solid var(--border);
	border-radius: 999px;
	background-color: var(--surface);
	font-size: 0.85rem;
	transition: background-color 0.15s ease;
}

.empty__chip:hover {
	background-color: var(--accent-soft);
}

.thinking {
	display: flex;
	align-items: center;
	gap: 0.75rem;
}

.thinking__marker {
	width: 1.25rem;
	font-family: var(--font-mono);
	font-weight: 700;
	color: var(--accent);
}

.thinking__dots {
	display: inline-flex;
	gap: 4px;
}

.thinking__dots i {
	width: 6px;
	height: 6px;
	border-radius: 50%;
	background-color: var(--muted);
	animation: thinking-bounce 1s ease-in-out infinite;
}

.thinking__dots i:nth-child(2) {
	animation-delay: 0.15s;
}

.thinking__dots i:nth-child(3) {
	animation-delay: 0.3s;
}

.thinking__sr {
	position: absolute;
	width: 1px;
	height: 1px;
	overflow: hidden;
	clip: rect(0 0 0 0);
}

@keyframes thinking-bounce {

	0%,
	80%,
	100% {
		opacity: 0.3;
		transform: translateY(0);
	}

	40% {
		opacity: 1;
		transform: translateY(-3px);
	}
}

@media (max-width: 768px) {
	.chat-main__menu {
		display: block;
	}
}

@media (prefers-reduced-motion: reduce) {
	.thinking__dots i {
		animation: none;
		opacity: 0.6;
	}
}
</style>
