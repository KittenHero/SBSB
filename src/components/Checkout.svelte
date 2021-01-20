<script>
  import { onMount, getContext } from 'svelte';
  import { Link } from 'svelte-routing';
  let cart = getContext('cart');
  let user = { name: '', email: '', phone: '' };
  let card = {};
  let loaded = false;
  let ui;

  function securePay() {
    ui = new securePayUI.init({
      containerId: 'securepay-container',
      scriptId: 'securepay-js',
      clientId: SECUREPAY_CLIENT,
      merchantCode: SECUREPAY_MERCHANT,
      card: {
        onTokeniseSuccess: data => { card = data; },
        onTokeniseError: err => { card = { error: err }; },
      },
      onLoadComplete: () => { loaded = true; },
    });
  };
  function submit() {
    if (!ui) return;
    ui.tokenise();
  };
</script>

<template>
  section
    h2 Checkout
    .container
      form
        fieldset
          legend Items
        fieldset
          legend Billing
          .form-group
            label(for='name') Your name
            input#name(bind:value=`{user.name}` class:empty=`{!user.name}` type='text' title='Enter your name' autocomplete='name' required)
          .form-group
            label(for='email') Email
            input#email(bind:value=`{user.email}` class:empty=`{!user.email}` type='email' title='Enter your email' autocomplete='email' required)
          .form-group
            label(for='phone') Phone
            input#phone(bind:value=`{user.phone}` class:empty=`{!user.phone}` type='tel' title='Enter your phone number' autocomplete='tel' required)
        fieldset
          legend Payment
          #securepay-container
        button.btn(on:click=`{submit}`, disabled=`{!loaded}`) submit
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
  input {
    margin-top: 10px;
  }
</style>
