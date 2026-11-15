<script setup lang="ts">
defineProps<{ title: string; subtitle: string }>()
</script>

<template>
	<main class="auth-layout">
		<div class="auth-card">
			<header class="auth-card__header">
				<p class="auth-card__brand"><span class="auth-card__prompt">&gt;</span> LogMind</p>
				<h1 class="auth-card__title">{{ title }}</h1>
				<p class="auth-card__subtitle">{{ subtitle }}</p>
			</header>

			<slot />

			<footer v-if="$slots.footer" class="auth-card__footer">
				<slot name="footer" />
			</footer>
		</div>
	</main>
</template>

<style scoped>
.auth-layout {
	min-height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 1.5rem;
}

.auth-card {
	width: 100%;
	max-width: 400px;
	display: flex;
	flex-direction: column;
	gap: 1.25rem;
	padding: 2rem;
	background-color: var(--surface);
	border: 1px solid var(--border);
	border-radius: 16px;
	box-shadow: var(--shadow);
}

.auth-card__header {
	display: flex;
	flex-direction: column;
	gap: 0.35rem;
}

.auth-card__brand {
	font-family: var(--font-mono);
	font-size: 0.9rem;
	font-weight: 600;
	color: var(--muted);
}

.auth-card__prompt {
	color: var(--accent);
}

.auth-card__title {
	font-size: 1.5rem;
	font-weight: 700;
	line-height: 1.2;
}

.auth-card__subtitle {
	font-size: 0.9rem;
	color: var(--muted);
}

.auth-card__footer {
	text-align: center;
	font-size: 0.875rem;
	color: var(--muted);
}

.auth-card__footer :deep(a) {
	color: var(--accent);
	font-weight: 600;
	text-decoration: none;
}

.auth-card__footer :deep(a:hover) {
	text-decoration: underline;
}
</style>
