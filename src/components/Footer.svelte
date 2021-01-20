<script>
  import {link} from 'svelte-routing';
  import facebook from '../assets/img/logo-facebook.svg';
</script>
<template>
  footer.footer.py-4
    .container
      .row
        .col
          p Open: 10:00 am - 9:00 pm
          p 13/2 Surf Road, Cronulla, NSW 2230
          a.mr-3(href='tel:0295277087') 02 9527 7087
          a(href='tel:0401807691') 0401 807 691
        .col.my-3.my-lg-0
          p © SABAI SABAI THAI MASSAGE &amp; DAY SPA 2020
          p ABN 51 311 967 595
          a(href='/privacy' use:link) privacy policy
        .col
          a.btn.mx-2(href='https://www.facebook.com/sabaisabaithai')
            img(src=`{facebook}` alt='facebook')
</template>
<style>
  footer {
    padding: 1.5rem 0;
    font-size: 0.9rem;
    font-family: Montserrat, var(--fallback-fonts);
    text-align: center;
  }
  .row {
    align-items: center;
  }
  @media (min-width: 992px) {
    .col {
      flex: 0 0 33.3333333333%;
      max-width: 33.3333333333%;
      &:first-child { text-align: left; }
      &:last-child { text-align: right; }
    }
  }
  .mr-3 { margin-right: 1rem; }
  .btn {
    padding: 0;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 100%;
    background: transparent;
  }
</style>
