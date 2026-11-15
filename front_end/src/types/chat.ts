export type MessageRole = 'user' | 'assistant'

export interface ChatMessage {
	id: string
	role: MessageRole
	content: string
	createdAt: string
}

export interface Chat {
	id: string
	title: string
	messages: ChatMessage[]
	createdAt: string
	updatedAt: string
}
