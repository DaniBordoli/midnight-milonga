<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	const { Story } = defineMeta({
		title: 'MIDNIGHT_MILONGA/book',
	});
</script>

<script lang="ts">
	import {
		StoryGameTemplate,
		StoryLocale,
		type TemplateArgs,
		templateArgs,
	} from 'components-storybook';
	import { randomInteger } from 'utils-shared/random';
	import { stateBet } from 'state-shared';

	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';
	import { playBet } from '../game/utils';
	import baseBooks from './data/base_books';
	import bonusBooks from './data/bonus_books';
	import superBooks from './data/super_books';

	setContext();

	// Real rounds exported from the math (tools/export_front_data.py)
	type Book = (typeof baseBooks)[number];
	const has = (book: Book, type: string) => book.events.some((event: any) => event.type === type);
	// mode = bet mode the round belongs to (the game shows mode-specific art, e.g. La Última Tanda intro)
	const playRandom = async (books: Book[], mode = 'BASE') => {
		stateBet.activeBetModeKey = mode;
		const book = books[randomInteger({ min: 0, max: books.length - 1 })];
		console.log('Running book id', book.id, 'payout', book.payoutMultiplier / 100);
		await playBet({ ...book, state: book.events } as any);
	};
	const big = (books: Book[]) => books.filter((b) => b.criteria === 'freegame' && b.payoutMultiplier >= 100_000);

</script>

{#snippet template(args: TemplateArgs<any>)}
	<StoryGameTemplate
		skipLoadingScreen={args.skipLoadingScreen}
		action={async () => {
			await args.action?.(args.data);
		}}
	>
		<StoryLocale lang="en">
			<Game />
		</StoryLocale>
	</StoryGameTemplate>
{/snippet}

<Story
	name="base random"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => await playRandom(baseBooks),
	})}
	{template}
/>

<Story
	name="base abrazo"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => await playRandom(baseBooks.filter((b) => has(b, 'abrazo'))),
	})}
	{template}
/>

<Story
	name="base rosa roja"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => await playRandom(baseBooks.filter((b) => has(b, 'rosaRoja'))),
	})}
	{template}
/>

<Story
	name="base free spins"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => await playRandom(baseBooks.filter((b) => b.criteria === 'freegame')),
	})}
	{template}
/>

<Story
	name="base max win"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => await playRandom(baseBooks.filter((b) => b.criteria === 'wincap')),
	})}
	{template}
/>

<Story
	name="la pista"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => await playRandom(bonusBooks.filter((b) => b.criteria === 'freegame'), 'BONUS'),
	})}
	{template}
/>

<Story
	name="la pista grande"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => await playRandom(big(bonusBooks), 'BONUS'),
	})}
	{template}
/>

<Story
	name="la ultima tanda"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => await playRandom(superBooks.filter((b) => b.criteria === 'freegame'), 'SUPER'),
	})}
	{template}
/>

<Story
	name="la ultima tanda grande"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => await playRandom(big(superBooks), 'SUPER'),
	})}
	{template}
/>
