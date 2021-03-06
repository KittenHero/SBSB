<script>
  import { onMount, getContext } from 'svelte';
  import { Link } from 'svelte-routing';
  import { api, itemsTotal } from '../utils';
  export let treatments = [];
  let cart = getContext('cart');
  let token = getContext('token');
  let codeInput = '', submitting = 0;

  $: infoCart = $cart.map(item => {
    const treatment = treatments.filter(t => t.title === item.massage_type)[0];
    const net_price = item.net_price || (treatment || { prices: {} }).prices[item.duration];
    if (!treatment || !net_price) return { massage_type: 'item does not exist' };
    return { net_price, small: treatment.small, ...item };
  });
  $: total = itemsTotal(infoCart);

  function remove(e) {
    const copy = $cart.slice();
    copy.splice(e.target.dataset.index, 1);
    $cart = copy;
  };
  function getProps() {
    return { class: 'btn' };
  }
  function applyCode() {
    submitting = 1;
    return api.purchase({
      items: !codeInput ? $cart : $cart.map(i => ({ ...i, discount: codeInput })),
      token: $token,
    }).then(d => {
      $token = d.token;
      $cart = d.items.map((i, j) =>
        i.net_price < ($cart[j].net_price || Infinity)
        ? i : $cart[j]
      );
    }).catch(e => console.log(e))
      .finally(() => {
        submitting = 0;
        codeInput = '';
    });
  }
  onMount(applyCode); // get idempotency token
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
            .col.time {item.duration} minutes
            .col.price
              +if('item.discount')
                s ${item.price}
                br
                | ${item.discount}:
                br
              | ${item.net_price}
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
