import type { paths } from './schema';
import { fetcher } from 'utils-fetcher';

// rgs_url normally arrives as a bare host and gets https:// added; a URL that already carries https:// is used
// as is. Only the local dev server also accepts http:// (a mock RGS for testing replays).
const rgsBase = (rgsUrl: string) => {
	if (/^https:\/\//i.test(rgsUrl)) return rgsUrl.replace(/\/+$/, '');
	if ((import.meta as unknown as { env?: { DEV?: boolean } }).env?.DEV && /^http:\/\//i.test(rgsUrl)) return rgsUrl;
	return `https://${rgsUrl}`;
};

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
