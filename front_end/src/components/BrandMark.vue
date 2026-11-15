<script setup lang="ts">
// Marca do LogMind: linhas de log, com uma linha em destaque e um ponto
// marcando o trecho que a I.A. apontou.
withDefaults(defineProps<{ size?: number }>(), { size: 28 })
</script>

<template>
	<svg :width="size" :height="size" viewBox="0 0 64 64" class="brand-mark" aria-hidden="true">
		<rect class="brand-mark__bg" width="64" height="64" rx="14" />
		<g class="brand-mark__fg">
			<rect x="12" y="15" width="36" height="7" rx="3.5" opacity="0.55" />
			<rect x="12" y="28.5" width="30" height="7" rx="3.5" />
			<circle cx="51" cy="32" r="5.5" />
			<rect x="12" y="42" width="22" height="7" rx="3.5" opacity="0.55" />
		</g>
	</svg>
</template>

<style scoped>
.brand-mark {
	flex-shrink: 0;
}

.brand-mark__bg {
	fill: var(--accent);
}

.brand-mark__fg {
	fill: var(--accent-contrast);
}
</style>
