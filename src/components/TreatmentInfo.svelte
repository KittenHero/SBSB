<script>
  import { onMount, getContext } from 'svelte';
  import { navigate } from 'svelte-routing';

  export let treatment;
  let cart = getContext('cart');
  onMount(() => scroll({ top: 1 }))
  function onClick(e) {
    alert('Online shop is under construction');
    return;
    $cart = [...$cart, { massage_type: treatment.title, duration: e.target.dataset.duration }];
    navigate('/cart');
  }
</script>

<template>
  section(id=`{treatment.id}`)
    h2 {treatment.title}
    .container
      .row
        .col
          img.img-fluid.d-block.mx-auto(src=`{treatment.img}` alt=`{treatment.title}`)
        .col
          +each('Object.entries(treatment.prices) as [duration, price]')
            button(on:click=`{onClick}` data-duration=`{duration}`) {duration} minutes for 
              strong ${price}
        .col
          p {treatment.description}
</template>

<style>
  h2 {
    font-size: 3rem;
    line-height: 3rem;
    text-transform: uppercase;
    margin: 3rem auto;
  }
  button {
    width: 100%;
    margin-bottom: .25rem;
    padding: .25rem 1rem;
    border: solid 1px var(--secondary);
    border-radius: .25rem;
    background: var(--secondary);
    &:hover {
      background: var(--secondary-2);
    }
  }
  img {
    display: block;
    max-width: 100%;
    height: auto;
  }
  .row {
    justify-content: center;
    text-align: center;
    .col {
      margin-bottom: 2rem;
      @media (min-width: 576px) {
        flex: 0 0 50%;
        max-width: 50%;
        &:last-child {
          flex: 0 0 100%;
          max-width: 100%;
        }
      }
      @media (min-width: 768px) {
        flex: 0 0 37.5%;
        max-width: 37.5%;

        &:first-child {
          flex: 0 0 25%;
          max-width: 25%;
        }
        &:nth-child(2) {
          order: 1;
        }
        &:last-child {
          flex: 0 0 37.5%;
          max-width: 37.5%;
        }
      }
    }
  }
</style>
