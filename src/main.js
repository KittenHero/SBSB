import App from './App.svelte';
import treatments from './data.js';

window.addEventListener('load', () => new App({
  target: document.body,
  hydrate: true,
  props: { treatments },
}));
