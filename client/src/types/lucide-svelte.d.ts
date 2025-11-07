import type { SvelteComponentTyped } from 'svelte';

declare module 'lucide-svelte' {
	import Loader from 'lucide-svelte/icons/loader.svelte';
	import AlertCircle from 'lucide-svelte/icons/alert-circle.svelte';
	import CheckCircle from 'lucide-svelte/icons/check-circle.svelte';
	export { Loader, AlertCircle, CheckCircle };
}

declare module 'lucide-svelte/icons/*' {
	const Icon: SvelteComponentTyped<Record<string, any>>;
	export default Icon;
}

