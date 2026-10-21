<script lang="ts">
	import { onMount } from 'svelte';

	import { EnablePixiExtension } from 'components-pixi';
	import { EnableHotkey } from 'components-shared';
	import { MainContainer } from 'components-layout';
	import { App, Container, Sprite, REM } from 'pixi-svelte';
	import { stateModal, stateUrlDerived } from 'state-shared';

	import { UI, UiGameName } from 'components-ui-pixi';
	import { GameVersion, Modals } from 'components-ui-html';

	import { getContext } from '../game/context';
	import { headerScale } from '../game/constants';
	import EnableSound from './EnableSound.svelte';
	import EnableGameActor from './EnableGameActor.svelte';
	import ResumeBet from './ResumeBet.svelte';
	import Sound from './Sound.svelte';
	import Background from './Background.svelte';
	import LoadingScreen from './LoadingScreen.svelte';
	import BoardFrame from './BoardFrame.svelte';
	import Board from './Board.svelte';
	import Anticipations from './Anticipations.svelte';
	import Win from './Win.svelte';
	import FreeSpinIntro from './FreeSpinIntro.svelte';
	import FreeSpinCounter from './FreeSpinCounter.svelte';
	import FreeSpinOutro from './FreeSpinOutro.svelte';
	import Transition from './Transition.svelte';
	import Compas from './Compas.svelte';
	import FeatureBanner from './FeatureBanner.svelte';
	import AbrazoDance from './AbrazoDance.svelte';
	import RosaThrow from './RosaThrow.svelte';
	import ReplayControls from './ReplayControls.svelte';
	import GameRulesContent from './GameRulesContent.svelte';
	import PayTableContent from './PayTableContent.svelte';

	const context = getContext();

	// header logos, sized from their sprite aspect ratios (title 1400 x 844, Pampa Play 512 x 115)
	const GAME_LOGO = { width: ((REM * 5) * 1400) / 844, height: REM * 5 };
	const BRAND_LOGO = { width: ((REM * 2.4) * 512) / 115, height: REM * 2.4 };

	onMount(() => (context.stateLayout.showLoadingScreen = true));

	context.eventEmitter.subscribeOnMount({
		buyBonusConfirm: () => {
			stateModal.modal = { name: 'buyBonusConfirm' };
		},
	});
</script>

<App>
	<EnableSound />
	<EnableHotkey />
	<EnableGameActor />
	<EnablePixiExtension />

	<Background />

	{#if context.stateLayout.showLoadingScreen}
		<LoadingScreen onloaded={() => (context.stateLayout.showLoadingScreen = false)} />
	{:else}
		<ResumeBet />
		<!--
			The reason why <Sound /> is rendered after clicking the loading screen:
			"Autoplay with sound is allowed if: The user has interacted with the domain (click, tap, etc.)."
			Ref: https://developer.chrome.com/blog/autoplay
		-->
		<Sound />

		<MainContainer>
			<BoardFrame />
		</MainContainer>

		<MainContainer>
			<Board />
			<Anticipations />
			<Compas />
		</MainContainer>

		<UI>
			{#snippet gameName()}
				<Container scale={headerScale()}>
					<UiGameName>
						<!-- the loading screen logo, already in memory -->
						<Sprite key="fxTitle" width={GAME_LOGO.width} height={GAME_LOGO.height} />
					</UiGameName>
				</Container>
			{/snippet}
			{#snippet logo()}
				<!-- in portrait the clock + game logo fill the top line, so the provider logo drops below the game logo -->
				<Sprite
					key="uiPampaPlayLogo"
					anchor={{ x: 1, y: 0 }}
					width={BRAND_LOGO.width * headerScale()}
					height={BRAND_LOGO.height * headerScale()}
					y={(context.stateLayoutDerived.layoutType() === 'portrait' ? GAME_LOGO.height + REM * 0.5 : REM * 0.25) *
						headerScale()}
				/>
			{/snippet}
		</UI>
		<AbrazoDance />
		<RosaThrow />
		<FeatureBanner />
		<Win />
		<FreeSpinIntro />
		{#if ['desktop', 'landscape'].includes(context.stateLayoutDerived.layoutType())}
			<FreeSpinCounter />
		{/if}
		<FreeSpinOutro />
		<Transition />
		{#if stateUrlDerived.replay()}
			<ReplayControls />
		{/if}
	{/if}
</App>

<Modals>
	{#snippet version()}
		<GameVersion version="0.1.0" />
	{/snippet}
	{#snippet gameRules()}
		<GameRulesContent />
	{/snippet}
	{#snippet payTable()}
		<PayTableContent />
	{/snippet}
</Modals>
