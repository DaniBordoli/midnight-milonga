<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut, linear } from 'svelte/easing';

	import { Circle, Container, Sprite, SpriteSheet } from 'pixi-svelte';

	import { getSymbolInfo } from '../game/utils';
	import { SYMBOL_SIZE } from '../game/constants';

	// frames per tick at 60 fps: 16 frames in about a second (wins are shown one after another, so longer
	// animations drag out spins with several wins)
	const WIN_ANIMATION_SPEED = 16 / 60;
	// landing: a squash then a stretch that settles
	const LAND_MS = 350;
	const LAND_SQUASH = 0.14;
	// rest: a slow breath, each symbol on its own phase so the board never pulses in step
	const IDLE_PERIOD_MS = 2400;
	const IDLE_SCALE = 0.015;
	// win burst behind the animation: a golden sparkle ring opening up and glints flying out
	const BURST_MS = 700;
	const GLINTS = 8;

	type Props = {
		x?: number;
		y?: number;
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		oncomplete?: () => void;
	};

	const props: Props = $props();
	// a still is done as soon as it shows; the win animation reports when it has played through
	const animated = $derived(props.symbolInfo.type === 'spriteSheet');
	const motion = $derived('motion' in props.symbolInfo ? props.symbolInfo.motion : undefined);

	// landing bounce: the board hands the land state back to static as soon as the still reports complete, so
	// the bounce is started right before that and the tween runs on into the rest state
	const land = new Tween(1, { duration: LAND_MS, easing: linear });
	const wobble = $derived(Math.sin(land.current * Math.PI * 2) * (1 - land.current));
	const landScale = $derived({ x: 1 + wobble * LAND_SQUASH * 0.7, y: 1 - wobble * LAND_SQUASH });

	onMount(() => {
		if (!animated) props.oncomplete?.();
	});

	$effect(() => {
		props.symbolInfo;
		if (motion === 'land') {
			land.set(0, { duration: 0 });
			land.set(1);
		}
		if (!animated) props.oncomplete?.();
	});

	// the board waits on the win animation: if it never reports back (e.g. rewound by a prop change), report
	// after WIN_TIMEOUT_MS so the round keeps moving; cleared as soon as the symbol leaves the win state
	const WIN_TIMEOUT_MS = 2000;
	$effect(() => {
		if (!animated) return;
		const timer = setTimeout(() => props.oncomplete?.(), WIN_TIMEOUT_MS);
		return () => clearTimeout(timer);
	});

	const phase = Math.random() * Math.PI * 2;
	let now = $state(0);
	$effect(() => {
		if (motion !== 'idle') return;
		const timer = setInterval(() => (now = performance.now()), 50);
		return () => clearInterval(timer);
	});
	const breath = $derived(motion === 'idle' ? 1 + IDLE_SCALE * Math.sin((now / IDLE_PERIOD_MS) * Math.PI * 2 + phase) : 1);

	const burst = new Tween(0, { duration: BURST_MS, easing: cubicOut });
	$effect(() => {
		if (!animated) return;
		burst.set(0, { duration: 0 });
		burst.set(1);
	});

	const width = $derived(SYMBOL_SIZE * props.symbolInfo.sizeRatios.width);
	const height = $derived(SYMBOL_SIZE * props.symbolInfo.sizeRatios.height);
</script>

{#if animated}
	{#if burst.current < 1}
		<Container x={props.x} y={props.y} alpha={1 - burst.current}>
			<Sprite
				key="fxSparkles"
				anchor={0.5}
				blendMode="add"
				width={SYMBOL_SIZE * (0.5 + burst.current)}
				height={SYMBOL_SIZE * (0.5 + burst.current)}
				rotation={burst.current * 0.6}
			/>
			{#each { length: GLINTS } as _, i}
				{@const angle = (i / GLINTS) * Math.PI * 2 + phase}
				<Circle
					x={Math.cos(angle) * SYMBOL_SIZE * 0.75 * burst.current}
					y={Math.sin(angle) * SYMBOL_SIZE * 0.75 * burst.current}
					anchor={0.5}
					diameter={SYMBOL_SIZE * (i % 2 ? 0.05 : 0.08)}
					backgroundColor={0xffe08a}
					blendMode="add"
				/>
			{/each}
		</Container>
	{/if}
	<!-- win animation: 16 frames over about a second, played once while the win is shown; its props stay
	     constant, since any change re-applies the textures and rewinds it -->
	<SpriteSheet
		x={props.x}
		y={props.y}
		anchor={0.5}
		key={props.symbolInfo.assetKey}
		{width}
		{height}
		animationSpeed={WIN_ANIMATION_SPEED}
		loop={false}
		onComplete={() => props.oncomplete?.()}
		play
	/>
{:else}
	<!-- scaled around the symbol's base, so the landing squash sits on the reel instead of shrinking mid-air -->
	<Container x={props.x} y={(props.y ?? 0) + height / 2} scale={{ x: landScale.x * breath, y: landScale.y * breath }}>
		<Sprite anchor={{ x: 0.5, y: 1 }} key={props.symbolInfo.assetKey} {width} {height} />
	</Container>
{/if}
