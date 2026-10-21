import type { paths } from './schema';
import { fetcher } from 'utils-fetcher';

// Engine always passes rgs_url without a scheme. Only the local dev server may point at a mock RGS with an
// explicit http:// URL (used to test replays); the published build always calls https.
const rgsBase = (rgsUrl: string) =>
	(import.meta as unknown as { env?: { DEV?: boolean } }).env?.DEV && /^https?:\/\//.test(rgsUrl)
		? rgsUrl
		: `https://${rgsUrl}`;

export const rgsFetcher = {
	post: async function post<
		T extends keyof paths,
		TResponse = paths[T]['post']['responses'][200]['content']['application/json'],
	>(options: {
		url: T;
		rgsUrl: string;
		variables?: paths[T]['post']['requestBody']['content']['application/json'];
	}): Promise<TResponse> {
		const response = await fetcher({
			method: 'POST',
			variables: options.variables,
			endpoint: `${rgsBase(options.rgsUrl)}${options.url}`,
		});

		if (response.status !== 200) console.error('error', response);
		const data = await response.json();
		return data as TResponse;
	},
	get: async function get<
		T extends keyof paths,
		TResponse = paths[T]['get']['responses'][200]['content']['application/json'],
	>(options: { url: T; rgsUrl: string }): Promise<TResponse> {
		const response = await fetcher({
			method: 'GET',
			endpoint: `${rgsBase(options.rgsUrl)}${options.url}`,
		});

		if (response.status !== 200) console.error('error', response);
		const data = await response.json();
		return data as TResponse;
	},
};
