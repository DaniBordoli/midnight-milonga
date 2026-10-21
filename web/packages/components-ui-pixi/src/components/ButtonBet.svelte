<script lang="ts">
	import { Container, Sprite, Text } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { OnHotkey } from 'components-shared';

	import ButtonBetProvider from './ButtonBetProvider.svelte';
	import { UI_BASE_FONT_SIZE, UI_BASE_SIZE, UI_GOLD, UI_FONT_FAMILY } from '../constants';
	import { i18nDerived } from '../i18n/i18nDerived';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const sizes = { width: UI_BASE_SIZE, height: UI_BASE_SIZE };
</script>

<ButtonBetProvider>
	{#snippet children({ key, onpress })}
		<!-- no 'disabled': without enough balance the button only looks dimmed and answers with the insufficient-funds notice -->
		<OnHotkey hotkey="Space" {onpress} />
		<Button {...props} {sizes} {onpress}>
			{#snippet children({ center, hovered, pressed })}
				{@const stopping = !['spin_default', 'spin_disabled'].includes(key)}
				{@const dimmed = ['spin_disabled', 'stop_disabled'].includes(key)}
				{@const scale = pressed ? 0.94 : hovered ? 1.04 : 1}
				<!-- Midnight Milonga skin: the rose medallion is the spin button; it only spells out STOP -->
				<Container {...center} {scale}>
					<Sprite key="uiButtonSpin" width={sizes.width * 1.15} height={sizes.height * 1.15} anchor={0.5} alpha={dimmed ? 0.5 : 1} />
					{#if stopping}
						<Sprite key="uiButtonSmall" width={sizes.width * 0.62} height={sizes.height * 0.62} anchor={0.5} />
						<Text
							anchor={0.5}
							text={i18nDerived.stop()}
							style={{
								fontFamily: UI_FONT_FAMILY,
								fontWeight: '400',
								fontSize: UI_BASE_FONT_SIZE * 0.6,
								fill: UI_GOLD,
							}}
						/>
					{/if}
				</Container>
			{/snippet}
		</Button>
	{/snippet}
</ButtonBetProvider>
