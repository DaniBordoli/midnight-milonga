<script lang="ts" module>
	import { stateBet, stateBetDerived, stateModal, stateUi } from 'state-shared';
</script>

<script lang="ts">
	import OnHotkey from './OnHotkey.svelte';

	const spaceHoldOn = () => {
		stateBet.autoSpinsCounter = 0;
		stateBet.isSpaceHold = true;
		stateBetDerived.updateIsTurbo(true, { persistent: true });
	};

	const spaceHoldOff = () => {
		stateBet.isSpaceHold = false;
		stateBetDerived.updateIsTurbo(false, { persistent: true });
	};
</script>

<!-- holding space never auto-bets behind an open panel or menu -->
<OnHotkey hotkey="Space" disabled={!!stateModal.modal || stateUi.menuOpen} onhold={spaceHoldOn} onholdend={spaceHoldOff} />
