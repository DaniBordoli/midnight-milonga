import type { EmitterEventBoard } from '../components/Board.svelte';
import type { EmitterEventBoardFrame } from '../components/BoardFrame.svelte';
import type { EmitterEventFreeSpinIntro } from '../components/FreeSpinIntro.svelte';
import type { EmitterEventFreeSpinCounter } from '../components/FreeSpinCounter.svelte';
import type { EmitterEventFreeSpinOutro } from '../components/FreeSpinOutro.svelte';
import type { EmitterEventWin } from '../components/Win.svelte';
import type { EmitterEventSound } from '../components/Sound.svelte';
import type { EmitterEventTransition } from '../components/Transition.svelte';
import type { EmitterEventFeatureBanner } from '../components/FeatureBanner.svelte';
import type { EmitterEventCompas } from '../components/Compas.svelte';
import type { EmitterEventAbrazoDance } from '../components/AbrazoDance.svelte';
import type { EmitterEventRosaThrow } from '../components/RosaThrow.svelte';

export type EmitterEventGame =
	| EmitterEventFeatureBanner
	| EmitterEventCompas
	| EmitterEventAbrazoDance
	| EmitterEventRosaThrow
	| EmitterEventBoard
	| EmitterEventBoardFrame
	| EmitterEventWin
	| EmitterEventFreeSpinIntro
	| EmitterEventFreeSpinCounter
	| EmitterEventFreeSpinOutro
	| EmitterEventSound
	| EmitterEventTransition;
