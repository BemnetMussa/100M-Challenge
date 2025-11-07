/// <reference types="svelte" />
/// <reference types="vite/client" />

declare module 'd3-array' {
	export function max<T>(
	  array: ArrayLike<T>,
	  accessor?: (d: T, i: number, arr: ArrayLike<T>) => number | null | undefined
	): number | undefined;
  }
  
  export {};