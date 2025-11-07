<script lang="ts">
	import { onMount } from 'svelte';
	import AnalyticsChart from '$lib/components/AnalyticsChart.svelte';
	import ComparisonMetrics from '$lib/components/ComparisonMatrics.svelte';
	import { Loader, AlertCircle } from 'lucide-svelte';

	let analyticsData: any = $state(null);
	let previousData: any = $state(null);
	let loading = $state(false);
	let error: string | null = $state(null);
	let fetchTime: number | null = $state(null);
	let lastFetchTime: string | null = $state(null);

	onMount(() => {
		const cached = localStorage.getItem('previousAnalyticsData');
		if (cached) {
			try {
				previousData = JSON.parse(cached);
			} catch (e) {
				console.error('[v0] Failed to parse cached data:', e);
			}
		}
		fetchData();
	});

	async function fetchData() {
		try {
			loading = true;
			error = null;
			fetchTime = null;
			const startTime = performance.now();

			const analyticsResponse = await fetch('http://localhost:8000/analytics/events/summary');
			if (!analyticsResponse.ok) throw new Error('Failed to fetch analytics data');

			const newData = await analyticsResponse.json();

			const endTime = performance.now();
			fetchTime = Math.round(endTime - startTime);
			lastFetchTime = new Date().toLocaleTimeString();

			if (analyticsData) {
				localStorage.setItem('previousAnalyticsData', JSON.stringify(analyticsData));
				previousData = analyticsData;
			}

			analyticsData = newData;
		} catch (err: any) {
			error = err.message;
			console.error('[v0] Data fetch error:', err);
		} finally {
			loading = false;
		}
	}
</script>

<div class="min-h-screen bg-black text-white">
	<div class="max-w-7xl mx-auto px-6 py-16">
		<!-- Header -->
		<div class="mb-16">
			<h1 class="text-5xl font-light tracking-tight mb-2">100M Challenge Analytics Dashboard</h1>
			<p class="text-gray-400 text-sm">Database performance and query optimization results</p>
		</div>

		<!-- Fetch Controls -->
		<div class="mb-12 flex flex-wrap items-center gap-6">
			<button
				onclick={fetchData}
				disabled={loading}
				class="inline-flex items-center gap-2 px-6 py-3 bg-white text-black font-medium text-sm hover:bg-gray-100 active:bg-gray-200 disabled:opacity-60 disabled:cursor-not-allowed transition-all duration-200 rounded shadow-lg"
			>
				{#if loading}
					<Loader class="h-4 w-4 animate-spin text-black" />
					<span>Fetching…</span>
				{:else}
					<span>Fetch Data</span>
				{/if}
			</button>

			<!-- Metrics display with better formatting -->
			{#if fetchTime !== null}
				<div class="text-sm">
					<span class="text-gray-400">Query Time: </span>
					<span class="text-white font-mono">{(fetchTime / 1000).toFixed(2)}s</span>
				</div>
			{/if}

			{#if lastFetchTime}
				<div class="text-sm">
					<span class="text-gray-400">Last Fetch: </span>
					<span class="text-white font-mono">{lastFetchTime}</span>
				</div>
			{/if}
		</div>

		<!-- Error State -->
		{#if error}
			<div class="mb-8 p-4 bg-red-950/30 border border-red-700 rounded flex items-center gap-3">
				<AlertCircle class="w-5 h-5 text-red-500 flex-shrink-0" />
				<span class="text-red-300 text-sm">{error}</span>
			</div>
		{/if}

		<!-- Loading State -->
		<!-- Main Content -->
		{#if analyticsData}
			<div class="space-y-8">
				<!-- Comparison Metrics only shown after second fetch -->
				{#if previousData}
					<ComparisonMetrics current={analyticsData} previous={previousData} />
				{/if}

				<!-- Chart -->
				{#if analyticsData.data && analyticsData.data.length > 0}
					<div class="border border-gray-700 rounded-lg bg-gray-950 p-6">
						<AnalyticsChart data={analyticsData.data} queryTime={analyticsData.query_time_ms} />
					</div>
				{/if}

				<!-- Placeholder Sections - Blurred -->
				<div class="space-y-6 blur-sm pointer-events-none opacity-50">
					<div class="border border-gray-700 rounded-lg bg-gray-950 p-6">
						<h3 class="text-sm font-medium text-gray-300 mb-4">System Status (Coming Soon)</h3>
						<div class="grid grid-cols-3 gap-4">
							<div class="p-4 bg-gray-900 rounded border border-gray-700">
								<p class="text-xs text-gray-500 mb-2">Dataset Size</p>
								<p class="text-2xl font-light">—</p>
							</div>
							<div class="p-4 bg-gray-900 rounded border border-gray-700">
								<p class="text-xs text-gray-500 mb-2">Load Time</p>
								<p class="text-2xl font-light">—</p>
							</div>
							<div class="p-4 bg-gray-900 rounded border border-gray-700">
								<p class="text-xs text-gray-500 mb-2">Status</p>
								<p class="text-2xl font-light">—</p>
							</div>
						</div>
					</div>

					<div class="border border-gray-700 rounded-lg bg-gray-950 p-6">
						<h3 class="text-sm font-medium text-gray-300 mb-4">Performance Metrics (Coming Soon)</h3>
						<div class="space-y-3">
							{#each Array(3) as _}
								<div class="flex justify-between items-center p-3 bg-gray-900 rounded border border-gray-700">
									<span class="text-sm text-gray-500">Metric</span>
									<span class="text-sm font-mono text-gray-500">— ms</span>
								</div>
							{/each}
						</div>
					</div>
				</div>
			</div>
		{:else if !loading && !error}
			<div class="text-center py-12 border border-gray-700 rounded-lg bg-gray-950 p-8">
				<p class="text-gray-500 text-sm">Click "Fetch Data" to load analytics</p>
			</div>
		{/if}
	</div>
</div>
