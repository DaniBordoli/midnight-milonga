<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';

	import { Container, Text, type TextProps } from 'pixi-svelte';

	type Props = {
		text: string;
		style: TextProps['style'];
		// true once the count-up has reached the amount
		completed: boolean;
	};

	// Win amount: swells slightly while counting up, then lands with a "pop" when the count-up ends.
	const COUNTING_SCALE = 1.08;
	const POP_SCALE = 1.35;
	const props: Props = $props();
	const scale = new Tween(1, { duration: 450, easing: backOut });
	$effect(() => {
		if (props.completed) {
			scale.set(POP_SCALE, { duration: 0 });
			scale.set(1);
		} else {
			scale.set(COUNTING_SCALE, { duration: 600 });
		}
	});
</script>

<Container scale={scale.current}>
	<Text anchor={0.5} text={props.text} style={props.style} />
</Container>
