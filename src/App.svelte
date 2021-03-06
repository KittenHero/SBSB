<script>
  import { onMount, setContext } from 'svelte';
  import { writable } from 'svelte/store';
  import { Router, Route } from 'svelte-routing';

  import Head from './components/Head.svelte';
  import Navigation from './components/Navigation.svelte';
  import Footer from './components/Footer.svelte';
  import Home from './components/Home.svelte';
  import TreatmentInfo from './components/TreatmentInfo.svelte';
  import Cart from './components/Cart.svelte';
  import Checkout from './components/Checkout.svelte';
  import Privacy from './components/Privacy.svelte';

  import '@fontsource/roboto-slab/latin.css';
  import '@fontsource/montserrat/latin.css';

  export let treatments;
  let cart = writable([]);
  let user = writable({});
  let token = writable(undefined);
  setContext('cart', cart);
  setContext('user', user);
  setContext('token', token);
  onMount(() => {
    $cart = JSON.parse(localStorage.cart || '[]');
    $user = JSON.parse(localStorage.user || '{}');
    $token = localStorage.token;
    const unsub = Object.entries({ cart, user })
      .map(([name, store]) => store.subscribe(v => localStorage.setItem(name, JSON.stringify(v))));
    unsub.push(token.subscribe(v => v ? localStorage.setItem('token', v) : localStorage.removeItem('token')));
    return () => unsub.forEach(u => u());
  });
</script>

<template>
  Head
  Router(let:location)
    Navigation(location=`{location}`)
    +each('treatments as t (t.id)')
      Route(path=`/{t.id}`)
        TreatmentInfo(treatment=`{t}`)
    Route(path='/cart')
      Cart(treatments=`{treatments}`)
    Route(path='/checkout')
      Checkout
    Route(path='/privacy')
      Privacy
    Route(path='/')
      Home(location=`{location}` treatments=`{treatments}`)
  Footer
</template>

<style>
  :global {
    :root {
      --primary: #470A42;
      --secondary: #fed136;
      --secondary-2: #fec810;
      --tertiary: #fff;
      --tertiary-2: #f8f9fa;
      --error: #dc3545;
      --text: #212529;
      --text-muted: #6c757d;
      --text-muted-2: #c6c3c3;
      --link-dark: #e6b301;
      --fallback-fonts: Roboto, Arial, sans-serif;
    }
    *, ::before, ::after {
      box-sizing: border-box;
    }
    ::selection {
      background: var(--secondary);
      text-shadow: none;
    }
    ::placeholder {
      font-family: Montserrat, var(--fallback-fonts);
      font-weight: 700;
      color: var(--text-muted-2);
    }
    html {
      font-family: "Roboto Slab", var(--fallback-fonts);
      color: var(--text);
      font-size: 1rem;
      font-weight: 400;
      line-height: 1.5;
      text-align: left;
      scroll-behavior: smooth;
    }
    body {
      margin: 0;
    }
    section {
      padding: 6rem 0;
      &:nth-of-type(2n+1) {
        background: var(--tertiary-2);
      }
    }
    iframe {
      border: 0;
    }
    img {
      vertical-align: middle;
      border-style: none;
    }
    a {
      color: var(--secondary);
      text-decoration: none;
      &:hover {
        text-decoration: underline;
        color: var(--link-dark);
      }
    }
    ul, ol {
      list-style: none;
    }
    h2,h3,h4 {
      font-family: Montserrat, var(--fallback-fonts);
      margin-top: 0;
      line-height: 1.2;
    }
    h2 {
      font-size: 2.5rem;
      text-align: center;
      text-transform: uppercase;
      margin-bottom: 1rem;
    }
    h3 {
      text-align: center;
      font-size: 1rem;
      font-weight: 400;
      font-style: italic;
      font-family: "Droid Serif", var(--fallback-fonts);
      color: var(--text-muted);
      margin-bottom: 4rem;
    }
    h4 {
      font-size: 1.5rem;
    }
    p {
      line-height: 1.75;
      margin: 0 0 1rem;
    }
    .collapse {
      overflow: hidden;
      max-height: 0;
      transition: max-height 0.35s ease-in-out;
      &.show {
        max-height: 100vh;
      }
    }
    .container {
      width: 100%;
      padding: 0 0.75rem;
      margin: 0 auto;
      @media (min-width: 576px) {
        max-width: 540px;
      }
      @media (min-width: 768px) {
        max-width: 720px;
      }
      @media (min-width: 992px) {
        max-width: 960px;
      }
      @media (min-width: 1200px) {
        max-width: 1140px;
      }
    }
    .row {
      display: flex;
      flex-wrap: wrap;
      margin: 0 -0.75rem;
    }
    .col {
      position: relative;
      width: 100%;
      padding: 0 0.75rem;
    }
    .btn {
      display: inline-block;
      padding: 0.75rem;
      background: var(--secondary);
      border: 0;
      border-radius: 0.25rem;

      font-size: 0.75rem;
      font-weight: 600;
      font-family: Montserrat, var(--fallback-fonts);
      line-height: 1;
      color: var(--tertiary);
      text-transform: uppercase;
      text-align: center;
      vertical-align: middle;
      user-select: none;

      &:not(:disabled) {
        cursor: pointer;
      }
      transition:
        color 0.15s ease-in-out,
        background-color 0.15s ease-in-out,
        border-color 0.15s ease-in-out,
        box-shadow 0.15s ease-in-out;
    }
    .btn-xl {
      padding: 1.25rem 2.5rem;
      font-size: 1.125rem;
      font-weight: 700;
      line-height: 1.5;
    }
    .alert {
      position: relative;
      padding: 1rem;
      margin-bottom: 1rem;
      color: var(--alert-color, inherit);
      background: var(--alert-background, transparent);
      border: 1px solid var(--alert-border, transparent);
      border-radius: .25rem;
      button {
        background: transparent;
        padding: .75rem 1.25rem;
        border: 0;
        position: absolute;
        top: 0;
        right: 0;
        &:focus, &:hover {
          color: #000;
          text-decoration: none;
          opacity: .75;
        }
      }
      &.success {
        --alert-background: #155724;
        --alert-color: #d4edda;
        --alert-color: #c3e6cb;
      }
      &.danger {
        --alert-color: #721c24;
        --alert-background: #f8d7da;
        --alert-border: #f5c6cb;
      }
    }
    .form-group {
      margin-bottom: 1.5rem;
      &:last-child {
        margin-bottom: 0;
      }
      &.textarea {
        height: 100%;
        textarea {
          height: 100%;
          min-height: 10rem;
          resize: vertical;
          overflow: auto;
        }
      }
      .input-group {
        position: relative;
        display: flex;
        flex-wrap: wrap;
        align-items: stretch;
        width: 100%;
        input {
          position: relative;
          flex: 1 1 auto;
          width: 1%;
        }
      }
      .input-group-append, .input-group-prepend {
        display: flex;
      }
    }
    input, textarea {
      display: block;
      width: 100%;
      height: 40px;
      padding: 7px 10px;
      border: 1px solid #e2dfda;
      border-radius: 0.25rem;
      font-size: 1rem;
      line-height: 1.5;
      color: var(--text);
      background: var(--tertiary);
      background-clip: padding-box;
      transition:
        border-collor 0.15s ease-in-out,
        box-shadow 0.15s ease-in-out;
        &.empty {
          box-shadow: none;
        }
    }
    .text-center {
      text-align: center;
    }
  }
</style>
