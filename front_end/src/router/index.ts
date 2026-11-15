import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

declare module 'vue-router' {
	interface RouteMeta {
		/** Só usuários autenticados. */
		requiresAuth?: boolean
		/** Só visitantes (login/cadastro): autenticados são enviados ao chat. */
		guestOnly?: boolean
	}
}

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/',
			redirect: { name: 'chat' },
		},
		{
			// Uma única rota (id opcional) para o componente ser reaproveitado ao
			// sair de "novo chat" para o chat recém-criado, sem remontar a tela.
			path: '/chat/:chatId?',
			name: 'chat',
			component: () => import('@/views/ChatView.vue'),
			meta: { requiresAuth: true },
		},
		{
			path: '/login',
			name: 'login',
			component: () => import('@/views/LoginView.vue'),
			meta: { guestOnly: true },
		},
		{
			path: '/register',
			name: 'register',
			component: () => import('@/views/RegisterView.vue'),
			meta: { guestOnly: true },
		},
		{
			path: '/:pathMatch(.*)*',
			redirect: '/',
		},
	],
})

router.beforeEach((to) => {
	const auth = useAuthStore()
	if (to.meta.requiresAuth && !auth.isAuthenticated) return { name: 'login' }
	if (to.meta.guestOnly && auth.isAuthenticated) return { name: 'chat' }
})

export default router
