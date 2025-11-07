<script lang="ts">
	import { onMount } from 'svelte';

	interface EventDatum {
		event_name?: string;
		count?: number;
	}

	interface AnalyticsSnapshot {
		data?: EventDatum[];
		query_time_ms?: number;
	}

	interface StoredMetrics {
		totalEvents: number;
		maxFrequency: number;
		bestQueryTime: number;
		recordedAt: string;
	}

	interface Props {
		current?: AnalyticsSnapshot;
		previous?: AnalyticsSnapshot;
	}

	const STORAGE_KEY = 'analyticsBestMetrics';

	let { current = {}, previous: _previous = {} }: Props = $props();
	let bestMetrics = $state<StoredMetrics | null>(null);

	let currentTotal = $derived(
		current.data?.reduce((sum, e) => sum + (e.count ?? 0), 0) ?? 0
	);
	let currentTime = $derived(current.query_time_ms ?? 0);
	let currentMax = $derived(
		Math.max(...(current.data?.map((e) => e.count ?? 0) ?? [0]))
	);

	function loadBestMetrics(): StoredMetrics | null {
		if (typeof localStorage === 'undefined') return null;
		try {
			const raw = localStorage.getItem(STORAGE_KEY);
			return raw ? (JSON.parse(raw) as StoredMetrics) : null;
		} catch (err) {
			console.error('[ComparisonMetrics] Failed to parse stored metrics:', err);
			return null;
		}
	}

	function saveBestMetrics(metrics: StoredMetrics) {
		if (typeof localStorage === 'undefined') return;
		try {
			localStorage.setItem(STORAGE_KEY, JSON.stringify(metrics));
		} catch (err) {
			console.error('[ComparisonMetrics] Failed to persist best metrics:', err);
		}
	}

	onMount(() => {
		bestMetrics = loadBestMetrics();
	});

	$effect(() => {
		if (!current || !current.data || current.data.length === 0) return;

		const candidate: StoredMetrics = {
			totalEvents: currentTotal,
			maxFrequency: currentMax,
			bestQueryTime: currentTime > 0 ? currentTime : Number.POSITIVE_INFINITY,
			recordedAt: new Date().toISOString()
		};

		if (!bestMetrics) {
			bestMetrics = candidate;
			saveBestMetrics(candidate);
			return;
		}

		let updated = { ...bestMetrics };
		let changed = false;

		if (candidate.totalEvents > bestMetrics.totalEvents) {
			updated.totalEvents = candidate.totalEvents;
			changed = true;
		}

		if (candidate.maxFrequency > bestMetrics.maxFrequency) {
			updated.maxFrequency = candidate.maxFrequency;
			changed = true;
		}

		if (
			candidate.bestQueryTime > 0 &&
			(candidate.bestQueryTime < bestMetrics.bestQueryTime || bestMetrics.bestQueryTime <= 0)
		) {
			updated.bestQueryTime = candidate.bestQueryTime;
			changed = true;
		}

		if (changed) {
			updated.recordedAt = candidate.recordedAt;
			bestMetrics = updated;
			saveBestMetrics(updated);
		}
	});

	let baselineTotal = $derived(bestMetrics?.totalEvents ?? currentTotal);
	let baselineTime = $derived(bestMetrics?.bestQueryTime ?? currentTime);
	let baselineMax = $derived(bestMetrics?.maxFrequency ?? currentMax);

	function getPercentageChange(currentValue: number, baselineValue: number): string {
		if (baselineValue === 0 || !Number.isFinite(baselineValue)) return '0.00';
		return (((currentValue - baselineValue) / baselineValue) * 100).toFixed(2);
	}

	function getIndicatorColor(change: string | number, isTimeMetric = false): string {
		const num = typeof change === 'number' ? change : parseFloat(change);
		if (Number.isNaN(num)) return 'text-gray-400';
		if (isTimeMetric) {
			return num <= 0 ? 'text-green-400' : 'text-red-400';
		}
		return num >= 0 ? 'text-green-400' : 'text-red-400';
	}

	function getIndicatorSymbol(change: string | number): string {
		const num = typeof change === 'number' ? change : parseFloat(change);
		if (Number.isNaN(num) || num === 0) return '';
		return num > 0 ? '+' : '';
	}

	let totalEventsChange = $derived(getPercentageChange(currentTotal, baselineTotal));
	let queryTimeChange = $derived(getPercentageChange(currentTime, baselineTime));
	let maxFreqChange = $derived(getPercentageChange(currentMax, baselineMax));
</script>

<!-- Improved background contrast: bg-gray-900 instead of bg-gray-950, border-gray-600 for visibility -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
	<!-- Total Events Metric -->
	<div class="p-6 bg-gray-900 border border-gray-600 rounded-lg shadow-sm hover:shadow-md transition-shadow">
		<p class="text-xs text-gray-400 uppercase tracking-wide font-medium">Total Events</p>
		<div class="flex items-baseline gap-3 mt-4">
			<p class="text-3xl font-light text-white">{currentTotal.toLocaleString()}</p>
			<span class={`text-sm font-mono font-semibold ${getIndicatorColor(totalEventsChange)}`}>
				{getIndicatorSymbol(totalEventsChange)}{totalEventsChange}%
			</span>
		</div>
		<p class="text-xs text-gray-500 mt-2">vs best: {baselineTotal.toLocaleString()}</p>
	</div>

	<!-- Query Time Metric -->
	<div class="p-6 bg-gray-900 border border-gray-600 rounded-lg shadow-sm hover:shadow-md transition-shadow">
		<p class="text-xs text-gray-400 uppercase tracking-wide font-medium">Query Time</p>
		<div class="flex items-baseline gap-3 mt-4">
			<p class="text-3xl font-light text-white">{(currentTime / 1000).toFixed(2)}s</p>
			<span class={`text-sm font-mono font-semibold ${getIndicatorColor(queryTimeChange, true)}`}>
				{getIndicatorSymbol(queryTimeChange)}{queryTimeChange}%
			</span>
		</div>
		<p class="text-xs text-gray-500 mt-2">
			vs best: {Number.isFinite(baselineTime) ? (baselineTime / 1000).toFixed(2) + 's' : '—'}
		</p>
	</div>

	<!-- Max Frequency Metric -->
	<div class="p-6 bg-gray-900 border border-gray-600 rounded-lg shadow-sm hover:shadow-md transition-shadow">
		<p class="text-xs text-gray-400 uppercase tracking-wide font-medium">Max Frequency</p>
		<div class="flex items-baseline gap-3 mt-4">
			<p class="text-3xl font-light text-white">{currentMax.toLocaleString()}</p>
			<span class={`text-sm font-mono font-semibold ${getIndicatorColor(maxFreqChange)}`}>
				{getIndicatorSymbol(maxFreqChange)}{maxFreqChange}%
			</span>
		</div>
		<p class="text-xs text-gray-500 mt-2">vs best: {baselineMax.toLocaleString()}</p>
	</div>
</div>
