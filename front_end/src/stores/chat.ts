import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { loadChats, requestReply, saveChats } from '@/services/chatService';
import type { Chat, ChatMessage, MessageRole } from '@/types/chat';

const TITLE_MAX_LENGTH = 48;

function uid(): string {
	return crypto.randomUUID();
}

function makeMessage(role: MessageRole, content: string): ChatMessage {
	return { id: uid(), role, content, createdAt: new Date().toISOString() };
}

function titleFrom(prompt: string): string {
	const oneLine = prompt.replace(/\s+/g, ' ').trim();
	return oneLine.length > TITLE_MAX_LENGTH ? `${oneLine.slice(0, TITLE_MAX_LENGTH).trimEnd()}…` : oneLine;
}

export const useChatStore = defineStore('chat', () => {
	const userId = ref<string | null>(null);
	const chats = ref<Chat[]>([]);
	const sendingChatId = ref<string | null>(null);

	/** Chats mais recentes primeiro. */
	const sortedChats = computed(() =>
		[...chats.value].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt)),
	);

	function persist() {
		if (userId.value) saveChats(userId.value, chats.value);
	}

	function init(forUserId: string) {
		if (userId.value === forUserId) return;
		userId.value = forUserId;
		chats.value = loadChats(forUserId);
		sendingChatId.value = null;
	}

	function reset() {
		userId.value = null;
		chats.value = [];
		sendingChatId.value = null;
	}

	function getChat(id: string | undefined): Chat | undefined {
		return id ? chats.value.find((chat) => chat.id === id) : undefined;
	}

	function deleteChat(id: string) {
		chats.value = chats.value.filter((chat) => chat.id !== id);
		persist();
	}

	async function fetchReply(target: Chat, text: string) {
		sendingChatId.value = target.id;
		try {
			const reply = await requestReply(target, text);
			target.messages.push(makeMessage('assistant', reply));
		} catch {
			target.messages.push(
				makeMessage('assistant', 'Não foi possível obter uma resposta agora. Tente novamente.'),
			);
		} finally {
			target.updatedAt = new Date().toISOString();
			sendingChatId.value = null;
			persist();
		}
	}

	/**
	 * Envia um prompt. Sem `chatId` (ou com id inexistente), cria um chat novo.
	 * `chatId` é devolvido na hora, para a tela já poder navegar até o chat;
	 * `reply` resolve quando a resposta chegar.
	 */
	function sendPrompt(prompt: string, chatId?: string): { chatId: string; reply: Promise<void> } {
		const text = prompt.trim();
		let target = getChat(chatId);

		if (!target) {
			const now = new Date().toISOString();
			chats.value.push({
				id: uid(),
				title: titleFrom(text),
				messages: [],
				createdAt: now,
				updatedAt: now,
			});
			// Pega o item pelo array reativo, para mutar sempre através do proxy.
			target = chats.value[chats.value.length - 1];
		}

		target.messages.push(makeMessage('user', text));
		target.updatedAt = new Date().toISOString();
		persist();

		return { chatId: target.id, reply: fetchReply(target, text) };
	}

	return { chats, sortedChats, sendingChatId, init, reset, getChat, deleteChat, sendPrompt };
});
