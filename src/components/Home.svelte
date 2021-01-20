<script>
  import { onMount, afterUpdate } from 'svelte';
  import Header from './Header.svelte';
  import Treatments from './Treatments.svelte';
  import About from './About.svelte';
  import Reviews from './Reviews.svelte';
  import Contact from './Contact.svelte';

  export let location;
  export let treatments;
  function scrollToHash() {
    const hash = location.hash;
    if (!hash) return;
    const target = document.querySelector(hash);
    if (!target) return;
    scroll({
      behavior: 'smooth',
      top: scrollY + target.getBoundingClientRect().y - 72,
    });
  };
  onMount(scrollToHash);
  afterUpdate(scrollToHash);
</script>

<template>
  Header
  Treatments(treatments=`{treatments}`)
  About
  Reviews
  Contact
</template>
