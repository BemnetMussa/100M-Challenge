<script lang="ts">
	interface Props {
		data?: { event_name: string; count: number }[];
		queryTime?: number;
	}

	const EVENT_NAME_MAP: Record<string, string> = {
		user_signup: 'New User Signups',
		checkout: 'Completed Checkouts',
		page_view: 'Page Views',
		add_to_cart: 'Items Added to Cart'
	};

	let { data = [], queryTime = 0 }: Props = $props();

	let hoveredEvent: string | null = $state(null);

	let maxCount = $derived(data.length ? Math.max(...data.map((d) => d.count)) : 0);

	function getBarHeight(count: number) {
		return (count / maxCount) * 100;
	}

	function barColor(count: number) {
		const ratio = maxCount ? count / maxCount : 0;
		if (ratio >= 0.75) return 'bg-green-600';
		if (ratio >= 0.4) return 'bg-yellow-400';
		return 'bg-red-400';
	}
</script>

<div class="border border-gray-600 rounded-lg p-6 bg-gray-900 shadow-sm">
	<div class="flex justify-between items-end mb-6">
		<div>
			<h2 class="text-lg font-light text-white">Top Events by Frequency</h2>
			<p class="text-xs text-gray-500 mt-1">Normalized to peak signal</p>
		</div>
		<span class="text-xs text-gray-400 font-mono">Query: {queryTime.toFixed(1)}ms</span>
	</div>

	<div
		class="flex items-end justify-between gap-4 h-80 p-4 bg-gray-950 rounded border border-gray-700"
	>
		{#if !data?.length}
			<p class="mx-auto text-sm text-gray-500">No events available</p>
		{:else}
			{#each data as event (event.event_name)}
				<div class="flex flex-col items-center gap-2 flex-1 group cursor-pointer h-full">
					<div class="w-full flex flex-col items-center justify-end h-full relative">
						<button
							type="button"
							class={`w-full block transition-all duration-200 rounded-t hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-black ${barColor(event.count)}`}
							style="height: {getBarHeight(event.count)}%; min-height: 5%;"
							onmouseenter={() => (hoveredEvent = event.event_name)}
							onmouseleave={() => (hoveredEvent = null)}
							aria-label="Event {event.event_name} with {event.count.toLocaleString()} occurrences"
						>
							{#if hoveredEvent === event.event_name}
								<div
									class="absolute -top-10 left-1/2 transform -translate-x-1/2 bg-gray-800 border border-gray-600 text-white text-xs px-2 py-1 rounded whitespace-nowrap z-10 pointer-events-none font-mono"
								>
									{event.count.toLocaleString()}
								</div>
							{/if}
						</button>
					</div>

					<div class="text-xs text-gray-400 text-center truncate w-full px-1">
						{EVENT_NAME_MAP[event.event_name] || event.event_name}
					</div>
				</div>
			{/each}
		{/if}
	</div>
</div>
