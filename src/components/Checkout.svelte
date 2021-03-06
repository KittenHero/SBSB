<script>
  import { onMount, getContext } from 'svelte';
  import { Link, navigate } from 'svelte-routing';
  import { api, itemsTotal } from '../utils.js';
  let cart = getContext('cart');
  let token = getContext('token');
  let user = getContext('user');
  let loaded = false;
  let ui;
  $: total = itemsTotal($cart);

  function submit(card) {
    if (!$user.name) {}
    if (!$user.email) {}
    if (!$user.phone) {}
    api.purchase({
      customer: $user,
      items: $cart,
      token: $token,
      payment_token: card.token,
    }).then(d => {
      $token = undefined;
      $cart = [];
    });
  };
  function securePay() {
    ui = new securePayUI.init({
      containerId: 'securepay-container',
      scriptId: 'securepay-js',
      clientId: SECUREPAY_CLIENT,
      merchantCode: SECUREPAY_MERCHANT,
      card: {
        onTokeniseSuccess: submit,
        onTokeniseError: err => console.log(err),
      },
      onLoadComplete: () => { loaded = true; },
    });
  };
  function click(e) {
    e.preventDefault();
    if (!!ui) ui.tokenise();
    return 0;
  }
  onMount(() => {
    if (!$token) navigate('/cart', { replace: true });
  });
</script>

<template>
  section
    h2 Checkout
    .container
      form
        .form-group
          label(for='total') Total
          .input-group
            span.input-group-prepend $
            input#total(value=`{total}` disabled=true)
        fieldset
          legend Billing
          .form-group
            label(for='name') Your name
            input#name(bind:value=`{$user.name}` class:empty=`{!$user.name}` type='text' title='Enter your name' autocomplete='name' required)
          .form-group
            label(for='email') Email
            input#email(bind:value=`{$user.email}` class:empty=`{!$user.email}` type='email' title='Enter your email' autocomplete='email' required)
          .form-group
            label(for='phone') Phone
            input#phone(bind:value=`{$user.phone}` class:empty=`{!$user.phone}` type='tel' title='Enter your phone number' autocomplete='tel' required)
        fieldset
          legend Payment
          #securepay-container
        button.btn(on:click=`{click}`, disabled=`{!loaded}`) submit
    script(id='securepay-js' src=`${SECUREPAY_UI}` on:load=`{securePay}`)
</template>

<style>
  section { background: #fff }
  form {
    margin: auto;
    width: 336px;
  }
  fieldset {
    border-radius: 4px;
  }
  label {
    font-family: Arial,Helvetica,sans-serif,var(--fallback-fonts);
    font-size: 14px;
    font-weight: 700;
    color: #161616;
  }
  input, .input-group-prepend {
    margin-top: 10px;
  }
  .input-group-prepend {
    padding: 7px 0;
  }
</style>
