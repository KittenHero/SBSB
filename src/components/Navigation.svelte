<script>
  import { getContext } from 'svelte';
  import { Link } from 'svelte-routing';

  import NavLink from './NavLink.svelte';
  import navLogo from '../assets/img/navbar-logo.png';

  export let location = { pathname: '/' };
  let cart = getContext('cart');
  let menu = false;
  let scroll = (typeof window === 'undefined') ? 0 : scrollY;
  $: hasCart = !!$cart.length;
  $: shrink = location.pathname != '/' || scroll > 100;

  function toggleMenu() {
    menu = !menu;
  }
  function hideMenu() {
    menu = false;
  }
  function onScroll() {
    scroll = scrollY;
  }
  function getProps() {
    return { class: 'navbar-brand' };
  }
</script>

<template>
  svelte:window(on:scroll=`{onScroll}`)
  nav(class:shrink)
    .container
      Link(to='/#page-top' getProps=`{getProps}`)
        img(src=`{navLogo}` alt='')
      button.btn(type='button' on:click='{toggleMenu}' aria-controls='navbarResponsive' aria-expanded=`{menu}` aria-label='Toggle navigation')
        | Menu
        i.fas.fa-bars
      #navbarResponsive.collapse(class:show=`{menu}` on:click=`{hideMenu}`)
        ul
          NavLink(to='/#treatments') Treatments
          NavLink(to='/#about') About
          NavLink(to='/#reviews') Reviews
          NavLink(to='/#contact') Contact
          +if('hasCart')
            NavLink(to='/cart') Cart
</template>

<style>
  nav {
    display: flex;
    padding: 1rem;
    background: var(--primary);

    position: fixed;
    top: 0;
    right: 0;
    left: 0;
    z-index: 999;

    color: var(--tertiary);
    align-items: center;
    flex-flow: row nowrap;
    transition:
      padding-top 0.3s ease-in-out,
      padding-bottom 0.3s ease-in-out;

    @media (min-width: 992px) {
      &:not(.shrink) {
        padding: 4rem 1rem 1.5rem;
        background: transparent;
      }
    }
  }
  .container {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    padding: 0;

    @media (min-width: 992px) {
      flex-wrap: nowrap;
      padding: 0 0.075rem;
    }
  }
  :global(.navbar-brand) {
    display: inline-block;
    margin-right: 1rem;
    padding: 0.3125rem 0;

    img {
      height: 3rem;
    }
  }
  button {
    @media (min-width: 992px) {
      display: none;
    }
  }
  #navbarResponsive {
    flex-basis: 100%;
    flex-grow: 1;
    align-items: center;

    @media(min-width: 992px) {
      display: flex;
      max-height: initial;
    }
    ul {
      display: flex;
      flex-basis: auto;
      flex-direction: column;

      padding: 0;
      margin: 0;
      text-transform: uppercase;

      @media(min-width: 992px) {
        flex-direction: row;
        margin-left: auto;
      }
    }
  }
</style>
