<script>
  import {Link} from 'svelte-routing';

  export let to;
  let active = false;

  $: getProps = () => ({ class: `link ${active ? 'active' : ''}` });
  function onScroll() {
    active = false;
    const hash = new URL(to, location.origin).hash;
    if (!hash) return;
    const target = document.querySelector(hash);
    if (!target) return;
    const rect = target.getBoundingClientRect();
    active = rect.y <= 74 && rect.y + rect.height > 74;
  }
</script>

<template>
  svelte:window(on:scroll=`{onScroll}`)
  li
    Link(to=`{to}` getProps=`{getProps}`)
      slot
</template>

<style>
  li {
    margin-right: 1rem;
  }
  :global(a.link) {
    display: block;
    padding: 0.5rem 0;
    font-size: 0.95rem;
    letter-spacing: 0.0625rem;
    text-decoration: none;
    font-family: Montserrat, var(--fallback-fonts);
    color: var(--tertiary);
    &:hover, &.active {
      color: var(--secondary);
    }
  }
</style>
