<script>
  import { getContext } from 'svelte';
  import { Link } from 'svelte-routing';
  export let treatments = [];
  let cart = getContext('cart');
  let codeInput = '', submitting = 0;

  $: infoCart = $cart.map(item => {
    const treatment = treatments.filter(t => t.title === item.massage_type)[0];
    const price = item.price || (treatment || { prices: {} }).prices[item.duration];
    if (!treatment || !price) return { massage_type: 'item does not exist' };
    return { price, small: treatment.small, ...item };
  });
  $: total = infoCart.reduce((sub, item) => +item.price + sub, 0).toFixed(2);

  function remove(e) {
    const copy = $cart.slice();
    copy.splice(e.target.dataset.index, 1);
    $cart = copy;
  };
  function getProps() {
    return { class: 'btn' };
  }
  function applyCode() {
    if (!codeInput) return;
    submitting = 1;
    fetch(`${API_URL}/purchase`, {
      method: 'POST',
      body: JSON.stringify({ items: $cart.map(i => ({ ...i, code: codeInput })) }),
    }).then(r => r.json())
      .then(d => console.log(d))
      .catch(() => console.log(API_URL))
      .finally(() => { submitting = 0; });
  }
</script>

<template>
  section
    h2 Cart
    .container
      .row
        .col.right
          .form-group
            label(for='code') Code
            .input-group
              input(id='code' bind:value=`{codeInput}`)
              .input-group-append
                button.btn(on:click=`{applyCode}` class:loading=`{submitting}`) apply
      +each('infoCart as item, i')
        .row.cart-item
          .col.img
            img(src=`{item.small}` alt=`{item.massage_type}`)
          .col.inner
            .col.type {item.massage_type}
            .col.time {item.duration}m
            .col.price ${item.price}
          .col.action
            button.btn(on:click=`{remove}` data-index=`{i}`) remove
      .row.cart-item
        .col.img
          Link(to='/#treatments' getProps=`{getProps}`) continue shopping
        .col.inner
          .col.type
          .col.time Total:
          .col.price ${total}
        .col.action
          Link(to='/checkout' getProps=`{getProps}`) checkout
</template>

<style>
  .row:not(.inner) {
    padding: 1rem 0;
  }
  .cart-item {
    text-align: end;
    &:nth-child(2n) {
      background: var(--tertiary);
    }
  }
  img {
    object-fit: cover;
    width: 6rem;
    height: 6rem;
  }
  .col {
    &.right {
      flex: 0 0 100%;
      max-width: 100%;
      margin-left: auto;
      @media (min-width: 576px) {
        flex: 0 0 50%;
        max-width: 50%;
      }
      @media (min-width: 992px) {
        flex: 0 0 33.333333%;
        max-width: 33.333333%;
      }
    }
    &.img, &.action {
      flex: 0 0 7.5rem;
      max-width: 7.5rem;
    }
    &.inner {
      flex: 0 0 calc(100% - 15rem);
      max-width: calc(100% - 15rem);
      display: flex;
      flex-wrap: wrap;
    }
    @media (min-width: 576px) {
      &.type {
        text-align: left;
      }
      &.type, &.time, &.price {
        flex: 1 1 5.5rem;
      }
    }
    @media (min-width: 992px) {
      &.type {
        flex: 0 0 50%;
        max-width: 50%;
        text-align: left;
      }
      &.time, &.price {
        flex: 0 0 25%;
        max-width: 25%;
      }
    }
  }
</style>
