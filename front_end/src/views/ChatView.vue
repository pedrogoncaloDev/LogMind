<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ChatSidebar from '@/components/ChatSidebar.vue'
import ChatMessageItem from '@/components/ChatMessageItem.vue'
import BrandMark from '@/components/BrandMark.vue'
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

const STARTERS = [
	{
		level: 'ERROR',
		title: 'Explicar um erro',
		description: 'Cole a mensagem ou o stack trace.',
		prompt: 'Explique o que significa este erro e qual a causa provável:\n',
	},
	{
		level: 'WARN',
		title: 'Resumir warnings',
		description: 'Veja o que merece atenção no log.',
		prompt: 'Resuma os principais warnings deste log:\n',
	},
	{
		level: 'INFO',
		title: 'Investigar lentidão',
		description: 'Procure picos de latência.',
		prompt: 'Como investigar picos de latência nestes logs?\n',
	},
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
				<section v-if="!chat" class="welcome">
					<BrandMark :size="48" />
					<h2 class="welcome__title">Analise seus logs com I.A.</h2>
					<p class="welcome__text">
						Descreva o problema ou cole um trecho de log. Para começar, escolha um exemplo:
					</p>

					<div class="welcome__cards">
						<button v-for="starter in STARTERS" :key="starter.title" type="button" class="starter"
							:class="`starter--${starter.level.toLowerCase()}`" @click="useSuggestion(starter.prompt)">
							<span class="starter__level">{{ starter.level }}</span>
							<strong class="starter__title">{{ starter.title }}</strong>
							<span class="starter__desc">{{ starter.description }}</span>
						</button>
					</div>
				</section>

				<section v-else class="messages" aria-live="polite">
					<ChatMessageItem v-for="message in chat.messages" :key="message.id" :message="message" />

					<div v-if="isWaitingReply" class="thinking" role="status">
						<BrandMark :size="28" />
						<div class="thinking__card" aria-hidden="true">
							<i /><i /><i />
						</div>
						<span class="thinking__sr">LogMind está analisando…</span>
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
	border-radius: var(--radius-sm);
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
	padding: 0.85rem 1.25rem 1rem;
	border-top: 1px solid var(--border);
}

.messages {
	max-width: 760px;
	margin: 0 auto;
	display: flex;
	flex-direction: column;
	gap: 1.25rem;
}

.welcome {
	max-width: 720px;
	min-height: 100%;
	margin: 0 auto;
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	justify-content: center;
	gap: 0.6rem;
}

.welcome__title {
	margin-top: 0.4rem;
	font-size: 1.9rem;
	line-height: 1.15;
	letter-spacing: -0.02em;
}

.welcome__text {
	color: var(--muted);
}

.welcome__cards {
	width: 100%;
	margin-top: 1.1rem;
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
	gap: 0.75rem;
}

.starter {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	gap: 0.25rem;
	padding: 0.85rem 1rem;
	text-align: left;
	border: 1px solid var(--border);
	border-radius: var(--radius-lg);
	background-color: var(--surface);
	transition: border-color 0.15s ease, background-color 0.15s ease;
}

.starter:hover {
	border-color: var(--accent);
	background-color: var(--accent-soft);
}

.starter__level {
	font-family: var(--font-mono);
	font-size: 0.68rem;
	font-weight: 700;
	letter-spacing: 0.08em;
}

.starter--error .starter__level {
	color: var(--danger);
}

.starter--warn .starter__level {
	color: #b7791f;
}

.starter--info .starter__level {
	color: var(--accent);
}

.starter__title {
	font-size: 0.95rem;
}

.starter__desc {
	font-size: 0.82rem;
	color: var(--muted);
}

.thinking {
	display: flex;
	align-items: flex-start;
	gap: 0.75rem;
}

.thinking__card {
	width: min(100%, 280px);
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
	padding: 0.85rem 0.95rem;
	border: 1px solid var(--border);
	border-radius: var(--radius-lg);
	border-top-left-radius: var(--radius-sm);
	background-color: var(--surface);
}

.thinking__card i {
	height: 8px;
	border-radius: 4px;
	background-color: var(--border);
	animation: thinking-pulse 1.2s ease-in-out infinite;
}

.thinking__card i:nth-child(1) {
	width: 100%;
}

.thinking__card i:nth-child(2) {
	width: 78%;
	animation-delay: 0.15s;
}

.thinking__card i:nth-child(3) {
	width: 52%;
	animation-delay: 0.3s;
}

.thinking__sr {
	position: absolute;
	width: 1px;
	height: 1px;
	overflow: hidden;
	clip: rect(0 0 0 0);
}

@keyframes thinking-pulse {

	0%,
	100% {
		opacity: 0.45;
	}

	50% {
		opacity: 1;
	}
}

@media (max-width: 768px) {
	.chat-main__menu {
		display: block;
	}
}

@media (prefers-reduced-motion: reduce) {
	.thinking__card i {
		animation: none;
		opacity: 0.7;
	}
}
</style>
