import type { AuthUser } from '@/types/auth';

/** Lê o payload de um JWT (sem validar a assinatura — isso é papel da API). */
export function decodeAuthUser(token: string | null): AuthUser | null {
	if (!token) return null;
	try {
		const payload = token.split('.')[1];
		if (!payload) return null;
		const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
		const json = decodeURIComponent(
			atob(base64)
				.split('')
				.map((c) => '%' + c.charCodeAt(0).toString(16).padStart(2, '0'))
				.join(''),
		);
		const data = JSON.parse(json) as { sub?: string; email?: string };
		if (!data.sub) return null;
		return { id: data.sub, email: data.email ?? '' };
	} catch {
		return null;
	}
}
