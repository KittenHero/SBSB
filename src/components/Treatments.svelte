<script>
  import {link} from 'svelte-routing';

  export let treatments = [];
</script>

<template>
  section#treatments
    .container
      h2 Treatments
      h3 We offer a variety of massages to suit your needs.
      .row
        +each('treatments as t')
          .col
            .treatment-item
              a(href=`/{t.id}` use:link)
                .hover
                  .content see more
                img.img-fluid(src=`{t.small}` alt=`{t.title}`)
              .caption
                .heading {t.title}
                .subheading From ${Object.entries(t.prices).map(([k, v]) => v).reduce((v, m) => Math.min(v, m), Infinity)}
</template>

<style>
  .col {
    margin-bottom: 1.5rem;
    @media (min-width: 576px) {
      flex: 0 0 50%;
      max-width: 50%;
    }
    @media (min-width: 992px) {
      flex: 0 0 33.3333333333%;
      max-width: 33.3333333333%;
    }
  }
  .treatment-item {
    max-width: 25rem;
    margin: 0 auto;
    a {
      position: relative;
      display: block;
      margin: 0 auto;
      .hover {
        display: flex;
        position: absolute;
        width: 100%;
        height: 100%;
        align-items: center;
        justify-content: center;

        background: rgba(254, 209, 54, 0.9);
        opacity: 0;

        transition: opacity ease-in-out 0.25s;
        &:hover {
          opacity: 1;
        }

        .content {
          font-size: 1.25rem;
          color: var(--tertiary);
        }
      }
      img {
        max-width: 100%;
        height: auto;
      }
    }
    .caption {
      padding: 1.5rem;
      text-align: center;
      background: var(--tertiary);
      .heading {
        font-size: 1.5rem;
        font-family: Montserrat, var(--fallback-fonts);
        font-weight: 700;
      }
      .subheading {
        font-style: italic;
        font-family: "Droid Serif", var(--fallback-fonts);
        color: var(--text-muted);
      }
    }
  }
</style>
