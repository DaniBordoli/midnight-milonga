<script lang="ts">
	import { Sprite, Text } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { stateModal, stateBet, stateBetDerived } from 'state-shared';

	import { UI_BASE_FONT_SIZE, UI_BASE_SIZE, UI_GOLD, UI_FONT_FAMILY } from '../constants';
	import { getContext } from '../context';
	import { i18nDerived } from '../i18n/i18nDerived';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const { stateXstateDerived, eventEmitter } = getContext();
	const sizes = { width: UI_BASE_SIZE, height: UI_BASE_SIZE };
	const disabled = $derived(!stateXstateDerived.isIdle());
	const active = $derived(stateBetDerived.activeBetMode()?.type === 'activate');

	const openModal = () => (stateModal.modal = { name: 'buyBonus' });
	const disableActiveBetMode = () => (stateBet.activeBetModeKey = 'BASE');
	const onpress = () => {
		eventEmitter.broadcast({ type: 'soundPressGeneral' });

		if (active) {
			disableActiveBetMode();
		} else {
			openModal();
		}
	};

	const getState = (value: {
		active: boolean;
		disabled: boolean;
		hovered: boolean;
		pressed: boolean;
	}) => {
		if (value.disabled) return 'disabled' as const;
		if (value.pressed) return 'pressed' as const;
		if (value.hovered) return 'hovered' as const;
		if (value.active) return 'active' as const;
		return 'default' as const;
	};
</script>

<Button {...props} {sizes} {disabled} {onpress}>
	{#snippet children({ center, hovered, pressed })}
		{@const state = getState({
			active,
			disabled,
			hovered,
			pressed,
		})}

		{@const scale = state === 'pressed' ? 0.94 : state === 'hovered' ? 1.04 : 1}
		<!-- Midnight Milonga skin: crimson velvet plate (art ratio 251 / 768) -->
		<Sprite
			key="uiButtonBuy"
			{...center}
			anchor={0.5}
			width={sizes.width * 1.3 * scale}
			height={sizes.width * 1.3 * (251 / 768) * scale}
			tint={state === 'active' ? 0xfff2c2 : 0xffffff}
			alpha={disabled ? 0.45 : 1}
		/>

		<Text
			{...center}
			anchor={0.5}
			alpha={disabled ? 0.45 : 1}
			text={state === 'active' ? i18nDerived.disable() : i18nDerived.buyBonus()}
			style={{
				align: 'center',
				wordWrap: true,
				wordWrapWidth: sizes.width * 0.55, // two lines, so the plate stays within the layout slot
				fontFamily: UI_FONT_FAMILY,
				fontWeight: '400',
				fontSize: UI_BASE_FONT_SIZE * 0.42,
				lineHeight: UI_BASE_FONT_SIZE * 0.44,
				fill: UI_GOLD,
			}}
		/>
	{/snippet}
</Button>
