<script lang="ts">
	interface Props {
		title?: string;
		value?: string;
		subtitle?: string;
	}

	let { title = '', value = '', subtitle = '' }: Props = $props();
</script>

<!-- Minimal black design removed -->
<div class="border border-gray-800 rounded p-4">
	<p class="text-xs text-gray-600 mb-2">{title}</p>
	<p class="text-xl font-light text-white mb-1">{value}</p>
	<p class="text-xs text-gray-700">{subtitle}</p>
</div>
