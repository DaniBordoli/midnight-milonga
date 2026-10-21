<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';
	import { MainContainer } from 'components-layout';
	import { stateBet, stateBetDerived, stateUrlDerived } from 'state-shared';
	import { numberToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import { stateXstateDerived } from '../game/stateXstate';
	import { GAME_FONT, headerScale } from '../game/constants';
	import { REM } from 'pixi-svelte';

	// Replay mode (Stake "Game replay" requirements): the round waits for PLAY, can be watched again with
	// PLAY AGAIN, and the bet's mode, cost, real cost and payout stay on screen. There is no way from here
	// into normal play: the replay UI has no bet controls.
	const context = getContext();

	type ReplayBet = NonNullable<typeof stateBet.betToResume> & { costMultiplier?: number; payoutMultiplier?: number };
	let replayBet = $state<ReplayBet | null>(null);
	let phase = $state<'ready' | 'playing' | 'done'>('ready');
	let sawBusy = false;

	onMount(() => {
		// keep a copy: resuming consumes stateBet.betToResume
		if (stateBet.betToResume) replayBet = $state.snapshot(stateBet.betToResume) as ReplayBet;
	});

	const play = () => {
		if (!replayBet || phase === 'playing') return;
		stateBet.betToResume = structuredClone($state.snapshot(replayBet)) as typeof stateBet.betToResume;
		stateBet.winBookEventAmount = 0;
		sawBusy = false;
		phase = 'playing';
		context.eventEmitter.broadcast({ type: 'soundPressBet' });
		context.eventEmitter.broadcast({ type: 'resumeBet' });
	};

	// the round is over once the game actor has been busy and is idle again
	$effect(() => {
		const idle = stateXstateDerived.isIdle();
		if (phase !== 'playing') return;
		if (!idle) sawBusy = true;
		else if (sawBusy) phase = 'done';
	});

	// social casinos may not show "cost": the real price reads as a total there
	const modeName = $derived(stateBetDerived.activeBetMode()?.text?.title || (stateUrlDerived.mode() || 'BASE').toUpperCase());
	const costMultiplier = $derived(replayBet?.costMultiplier ?? 1);
	const costLine = $derived(
		`${modeName === 'BASE' ? 'BASE GAME' : modeName}: ${numberToCurrencyString(stateBet.betAmount)}` +
			(costMultiplier !== 1
				? `  ·  ${stateUrlDerived.social() ? 'TOTAL' : 'REAL COST'}: ${numberToCurrencyString(stateBet.betAmount * costMultiplier)}`
				: ''),
	);
	const payoutLine = $derived(
		replayBet?.payoutMultiplier !== undefined && phase === 'done' ? `PAYOUT x${Number(replayBet.payoutMultiplier.toFixed(2))}` : '',
	);

	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	// wide screens: on the header line between game name and provider; otherwise on its own row below
	const infoY = $derived(
		context.stateLayoutDerived.layoutType() === 'portrait'
			? REM * 4 * headerScale() + 4
			: canvas.width < 1100
				? REM * 2 * headerScale() + 2
				: 8,
	);
	const BUTTON = 150;
</script>

{#if replayBet}
	{#if phase === 'ready'}
		<Rectangle width={canvas.width} height={canvas.height} backgroundColor={0x000000} alpha={0.55} eventMode="static" onpointerup={play} />
	{/if}

	<!-- bet info on the header line, between the game name and the provider (below them in portrait) -->
	<Text
		anchor={{ x: 0.5, y: 0 }}
		x={canvas.width / 2}
		y={infoY}
		text={[phase === 'ready' ? 'REPLAY' : '', costLine, payoutLine].filter(Boolean).join('  ·  ')}
		style={{ fontFamily: GAME_FONT, fontSize: Math.max(13, Math.min(22, canvas.width / 46)), fill: 0xf2d692, stroke: { color: 0x000000, width: 4 } }}
	/>

	{#if phase === 'ready'}
		<!-- first watch: big PLAY in the middle of the dimmed screen -->
		<Container x={canvas.width / 2} y={canvas.height * 0.45} scale={Math.min(1.2, canvas.height / 600)}>
			<Sprite key="uiButtonSpin" anchor={0.5} width={BUTTON} height={BUTTON} eventMode="static" cursor="pointer" onpointerup={play} />
			<Text anchor={0.5} y={BUTTON * 0.66} text="PLAY" style={{ fontFamily: GAME_FONT, fontSize: 34, fill: 0xf2d692, stroke: { color: 0x000000, width: 5 } }} />
		</Container>
	{:else if phase === 'done'}
		<MainContainer standard alignVertical="bottom">
			<!-- the spin button's slot, right of the win / bet labels; the results stay visible -->
			<Container
				x={context.stateLayoutDerived.mainLayoutStandard().width * 0.5 + 350}
				y={context.stateLayoutDerived.mainLayoutStandard().height - 210}
				scale={0.9}
			>
				<Sprite key="uiButtonSpin" anchor={0.5} width={BUTTON} height={BUTTON} eventMode="static" cursor="pointer" onpointerup={play} />
				<Text anchor={0.5} y={BUTTON * 0.62} text="PLAY AGAIN" style={{ fontFamily: GAME_FONT, fontSize: 30, fill: 0xf2d692, stroke: { color: 0x000000, width: 5 } }} />
			</Container>
		</MainContainer>
	{/if}
{/if}
