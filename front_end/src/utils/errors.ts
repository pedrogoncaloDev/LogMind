type ApiErrorBody = { detail?: string | { msg?: string }[] };

/** Extrai uma mensagem legível de um erro do axios/FastAPI. */
export function extractErrorMessage(error: unknown, fallback: string): string {
	if (typeof error === 'object' && error !== null && 'response' in error) {
		const detail = (error as { response?: { data?: ApiErrorBody } }).response?.data?.detail;
		if (typeof detail === 'string') return detail;
		if (Array.isArray(detail) && detail[0]?.msg) return detail[0].msg;
	}
	return fallback;
}
