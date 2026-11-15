<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { Chat } from '@/types/chat'

defineProps<{
	chats: Chat[]
	activeChatId?: string
	userEmail: string
	open: boolean
}>()

const emit = defineEmits<{
	newChat: []
	deleteChat: [id: string]
	logout: []
	close: []
}>()

function confirmDelete(chat: Chat) {
	if (window.confirm(`Excluir o chat "${chat.title}"?`)) emit('deleteChat', chat.id)
}
</script>

<template>
	<div v-if="open" class="sidebar-backdrop" @click="emit('close')" />

	<aside class="sidebar" :class="{ 'sidebar--open': open }" aria-label="Seus chats">
		<header class="sidebar__header">
			<p class="sidebar__brand"><span class="sidebar__prompt">&gt;</span> LogMind</p>
			<button type="button" class="sidebar__new" @click="emit('newChat')">
				<span aria-hidden="true">+</span> Novo chat
			</button>
		</header>

		<nav class="sidebar__list" aria-label="Histórico de chats">
			<p v-if="chats.length === 0" class="sidebar__empty">Nenhum chat ainda.</p>

			<ul v-else>
				<li v-for="chat in chats" :key="chat.id" class="sidebar__item">
					<RouterLink :to="`/chat/${chat.id}`" class="sidebar__link"
						:class="{ 'sidebar__link--active': chat.id === activeChatId }" :title="chat.title"
						@click="emit('close')">
						{{ chat.title }}
					</RouterLink>
					<button type="button" class="sidebar__delete" :aria-label="`Excluir o chat ${chat.title}`"
						@click="confirmDelete(chat)">
						×
					</button>
				</li>
			</ul>
		</nav>

		<footer class="sidebar__footer">
			<span class="sidebar__user" :title="userEmail">{{ userEmail }}</span>
			<button type="button" class="sidebar__logout" @click="emit('logout')">Sair</button>
		</footer>
	</aside>
</template>

<style scoped>
.sidebar {
	width: 280px;
	flex-shrink: 0;
	display: flex;
	flex-direction: column;
	background-color: var(--sidebar);
	border-right: 1px solid var(--border);
}

.sidebar__header {
	display: flex;
	flex-direction: column;
	gap: 0.9rem;
	padding: 1rem 0.9rem 0.75rem;
}

.sidebar__brand {
	font-family: var(--font-mono);
	font-weight: 600;
	padding-left: 0.25rem;
}

.sidebar__prompt {
	color: var(--accent);
}

.sidebar__new {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0.55rem 0.75rem;
	border: 1px solid var(--border);
	border-radius: var(--radius);
	background-color: var(--surface);
	font-weight: 600;
	font-size: 0.9rem;
	transition: background-color 0.15s ease;
}

.sidebar__new:hover {
	background-color: var(--surface-hover);
}

.sidebar__new span {
	color: var(--accent);
	font-size: 1.1rem;
	line-height: 1;
}

.sidebar__list {
	flex: 1;
	min-height: 0;
	overflow-y: auto;
	padding: 0.25rem 0.5rem;
}

.sidebar__list ul {
	list-style: none;
	display: flex;
	flex-direction: column;
	gap: 2px;
}

.sidebar__empty {
	padding: 0.75rem;
	font-size: 0.85rem;
	color: var(--muted);
}

.sidebar__item {
	position: relative;
	display: flex;
	align-items: center;
}

.sidebar__link {
	flex: 1;
	min-width: 0;
	padding: 0.5rem 2rem 0.5rem 0.75rem;
	border-radius: 8px;
	font-size: 0.9rem;
	color: var(--text);
	text-decoration: none;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.sidebar__link:hover {
	background-color: var(--sidebar-hover);
}

.sidebar__link--active,
.sidebar__link--active:hover {
	background-color: var(--sidebar-active);
	font-weight: 600;
}

.sidebar__delete {
	position: absolute;
	right: 0.35rem;
	width: 1.5rem;
	height: 1.5rem;
	display: flex;
	align-items: center;
	justify-content: center;
	border: none;
	border-radius: 6px;
	background: none;
	color: var(--muted);
	font-size: 1.1rem;
	line-height: 1;
	opacity: 0;
	transition: opacity 0.15s ease;
}

.sidebar__item:hover .sidebar__delete,
.sidebar__delete:focus-visible {
	opacity: 1;
}

.sidebar__delete:hover {
	color: var(--danger);
	background-color: var(--sidebar-active);
}

.sidebar__footer {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.5rem;
	padding: 0.75rem 0.9rem;
	border-top: 1px solid var(--border);
}

.sidebar__user {
	min-width: 0;
	font-size: 0.8rem;
	color: var(--muted);
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.sidebar__logout {
	flex-shrink: 0;
	padding: 0.3rem 0.6rem;
	border: 1px solid var(--border);
	border-radius: 8px;
	background: none;
	font-size: 0.8rem;
	font-weight: 600;
}

.sidebar__logout:hover {
	background-color: var(--sidebar-hover);
}

.sidebar-backdrop {
	display: none;
}

@media (max-width: 768px) {
	.sidebar {
		position: fixed;
		inset: 0 auto 0 0;
		z-index: 20;
		transform: translateX(-100%);
		transition: transform 0.2s ease;
	}

	.sidebar--open {
		transform: translateX(0);
	}

	.sidebar-backdrop {
		display: block;
		position: fixed;
		inset: 0;
		z-index: 10;
		background-color: rgba(0, 0, 0, 0.4);
	}

	/* Em telas sem hover não existe como "passar o mouse": o botão fica sempre visível. */
	.sidebar__delete {
		opacity: 1;
	}
}
</style>
