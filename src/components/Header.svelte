<script>
  import {Link} from 'svelte-routing';

  import HeaderBG from '../assets/img/header-bg.jpg';
  const getProps = () => ({ class: 'btn btn-xl' });
</script>

<template>
  header(style="--header-bg: url({HeaderBG})")
    .container
      .subheading Relax you Body, Mind and Soul
      .heading Sabai Sabai Thai Massage &amp; Day Spa
      Link(getProps=`{getProps}` to='/#treatments') see our treatments
</template>

<style>
  header {
    padding: 17rem 0 12.5rem;
    text-align: center;
    color: #fff;
    background:
      radial-gradient(circle, #0008 45%, transparent 90%),
      linear-gradient(to right, #6c5768, #6c5768),
      var(--header-bg);
    background-repeat: no-repeat;
    background-attachment: scroll;
    background-position: center center;
    background-size: cover;
    background-blend-mode: luminosity, overlay, normal;
  }
  .subheading {
    font-size: 2.25rem;
    font-style: italic;
    line-height: 2.25rem;
    margin-bottom: 2rem;
    font-family: "Droid Serif", var(--fallback-fonts);
  }
  .heading {
    font-size: 4.5rem;
    font-weight: 700;
    line-height: 4.5rem;
    margin-bottom: 4rem;
    font-family: Montserrat, var(--fallback-fonts);
  }
</style>
