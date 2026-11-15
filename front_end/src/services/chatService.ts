import type { Chat } from '@/types/chat';

/**
 * Camada de acesso aos chats.
 *
 * A API ainda não possui endpoints de chat/IA, então:
 *  - o histórico de chats é persistido no localStorage, separado por usuário;
 *  - `requestReply` devolve uma resposta provisória.
 *
 * Quando o back-end expuser esses recursos, basta trocar as implementações
 * desta camada por chamadas ao `httpClient` — store e telas não mudam.
 */

const storageKey = (userId: string) => `logmind:chats:${userId}`;

export function loadChats(userId: string): Chat[] {
	try {
		const raw = localStorage.getItem(storageKey(userId));
		return raw ? (JSON.parse(raw) as Chat[]) : [];
	} catch {
		return [];
	}
}

export function saveChats(userId: string, chats: Chat[]): void {
	try {
		localStorage.setItem(storageKey(userId), JSON.stringify(chats));
	} catch {
		// Quota cheia ou storage indisponível: o chat segue funcionando em memória.
	}
}

export async function requestReply(_chat: Chat, _prompt: string): Promise<string> {
	await new Promise((resolve) => setTimeout(resolve, 700));
	return (
		'O serviço de IA ainda não está conectado ao back-end do LogMind, ' +
		'então não consigo analisar este prompt por enquanto. ' +
		'Sua mensagem foi salva neste chat.'
	);
}
