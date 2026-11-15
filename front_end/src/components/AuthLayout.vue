<script setup lang="ts">
import BrandMark from './BrandMark.vue'

defineProps<{ title: string; subtitle: string }>()
</script>

<template>
	<main class="auth">
		<aside class="auth__panel">
			<p class="auth__brand">
				<BrandMark :size="34" class="auth__logo" /> LogMind
			</p>

			<div class="auth__pitch">
				<h2 class="auth__headline">Analise seus logs com I.A.</h2>
				<p class="auth__lead">Envie seus arquivos de log e entenda erros, alertas e causas prováveis.</p>

				<div class="auth__sample" aria-hidden="true">
					<div class="auth__log">
						<div class="log-line"><span class="log-time">12:04:11</span><span
								class="lvl lvl--info">INFO</span>server started on :5000</div>
						<div class="log-line"><span class="log-time">12:04:19</span><span
								class="lvl lvl--warn">WARN</span>slow query (1.8s) on users</div>
						<div class="log-line log-line--hit"><span class="log-time">12:04:23</span><span
								class="lvl lvl--error">ERROR</span>payment timeout after 30s</div>
						<div class="log-line"><span class="log-time">12:04:23</span><span
								class="lvl lvl--info">INFO</span>retry 1/3 scheduled</div>
					</div>
					<p class="auth__insight">
						<BrandMark :size="22" class="auth__logo" /><span><strong>Causa provável:</strong> timeout no
							serviço de pagamentos.</span>
					</p>
					<p class="auth__sample-note">Exemplo ilustrativo</p>
				</div>
			</div>
		</aside>

		<section class="auth__form">
			<div class="auth__card">
				<p class="auth__mobile-brand">
					<BrandMark :size="28" /> LogMind
				</p>

				<header class="auth__header">
					<h1 class="auth__title">{{ title }}</h1>
					<p class="auth__subtitle">{{ subtitle }}</p>
				</header>

				<slot />

				<footer v-if="$slots.footer" class="auth__footer">
					<slot name="footer" />
				</footer>
			</div>
		</section>
	</main>
</template>

<style scoped>
.auth {
	min-height: 100vh;
	display: grid;
	grid-template-columns: minmax(0, 1fr);
}

/* ---- Painel de marca (só em telas largas) ---- */
.auth__panel {
	display: none;
	flex-direction: column;
	justify-content: space-between;
	gap: 2rem;
	padding: 3rem;
	color: #f3efff;
	background: linear-gradient(155deg, #241a47 0%, #3c2d7a 55%, #5a46a8 100%);
}

.auth__brand {
	display: flex;
	align-items: center;
	gap: 0.65rem;
	font-size: 1.15rem;
	font-weight: 700;
	letter-spacing: -0.01em;
}

.auth__pitch {
	max-width: 460px;
}

.auth__headline {
	font-size: 2rem;
	line-height: 1.15;
	letter-spacing: -0.02em;
}

.auth__lead {
	margin-top: 0.75rem;
	color: rgba(243, 239, 255, 0.78);
}

.auth__sample {
	margin-top: 2rem;
}

.auth__log {
	padding: 0.9rem 0.5rem;
	font-family: var(--font-mono);
	font-size: 0.8rem;
	line-height: 1.9;
	background-color: rgba(12, 8, 30, 0.45);
	border: 1px solid rgba(255, 255, 255, 0.12);
	border-radius: var(--radius-lg);
}

.log-line {
	display: flex;
	gap: 0.75rem;
	padding: 0 0.6rem;
	border-radius: var(--radius-sm);
	white-space: nowrap;
}

.log-line--hit {
	background-color: rgba(248, 113, 113, 0.16);
}

.log-time {
	color: rgba(243, 239, 255, 0.45);
}

.lvl {
	width: 3.2rem;
	font-weight: 700;
}

.lvl--info {
	color: #7dd3fc;
}

.lvl--warn {
	color: #fcd34d;
}

.lvl--error {
	color: #fca5a5;
}

.auth__insight {
	display: flex;
	align-items: center;
	gap: 0.65rem;
	margin-top: 0.85rem;
	padding: 0.7rem 0.9rem;
	font-size: 0.88rem;
	background-color: rgba(255, 255, 255, 0.08);
	border: 1px solid rgba(255, 255, 255, 0.14);
	border-radius: var(--radius);
}

/* Na faixa roxa, a marca usa cores fixas (independem do tema). */
.auth__panel .auth__logo :deep(.brand-mark__bg),
.auth__insight :deep(.brand-mark__bg) {
	fill: #e4d9ff;
}

.auth__panel .auth__logo :deep(.brand-mark__fg),
.auth__insight :deep(.brand-mark__fg) {
	fill: #2a1f52;
}

.auth__sample-note {
	margin-top: 0.6rem;
	font-size: 0.75rem;
	color: rgba(243, 239, 255, 0.5);
}

/* ---- Formulário ---- */
.auth__form {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 1.5rem;
}

.auth__card {
	width: 100%;
	max-width: 380px;
	display: flex;
	flex-direction: column;
	gap: 1.4rem;
}

.auth__mobile-brand {
	display: flex;
	align-items: center;
	gap: 0.6rem;
	font-size: 1.05rem;
	font-weight: 700;
}

.auth__header {
	display: flex;
	flex-direction: column;
	gap: 0.35rem;
}

.auth__title {
	font-size: 1.7rem;
	font-weight: 700;
	line-height: 1.15;
	letter-spacing: -0.02em;
}

.auth__subtitle {
	color: var(--muted);
}

.auth__footer {
	font-size: 0.875rem;
	color: var(--muted);
}

.auth__footer :deep(a) {
	color: var(--accent);
	font-weight: 600;
	text-decoration: none;
}

.auth__footer :deep(a:hover) {
	text-decoration: underline;
}

@media (min-width: 900px) {
	.auth {
		grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr);
	}

	.auth__panel {
		display: flex;
	}

	.auth__mobile-brand {
		display: none;
	}
}
</style>
