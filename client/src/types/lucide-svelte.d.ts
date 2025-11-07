import type { SvelteComponentTyped } from 'svelte';

declare module 'lucide-svelte' {
	import Loader from 'lucide-svelte/icons/loader.svelte';
	import AlertCircle from 'lucide-svelte/icons/alert-circle.svelte';
	export { Loader, AlertCircle };
}

declare module 'lucide-svelte/icons/*' {
	const Icon: SvelteComponentTyped<Record<string, any>>;
	export default Icon;
}

