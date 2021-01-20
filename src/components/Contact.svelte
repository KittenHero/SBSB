<script>
  import ContactForm from './ContactForm.svelte';
</script>
<template>
  section#contact
    .container
      h2 Contact Us
      h3 Call us to make a booking
      .row.justify-content-around
        .col
          #location
            h4 Location
            p.card-text 13/2 Surf Road, Cronulla, NSW 2230
            p.card-text Open: 10:00 am - 9:00 pm
            p.card-text Call: 
              a(href='tel:0295277087') 02 9527 7087
              | , 
              a(href='tel:0401807691') 0401 807 691
            .embed-responsive.embed-responsive-16by9
              +if('GOOGLE_API_KEY != 0')
                iframe#map(frameborder="0" allowfullscreen referrerpolicy="strict-origin" title="map"
                    src=`https://www.google.com/maps/embed/v1/place?key=${GOOGLE_API_KEY}&q=13/2+Surf+RoadCronullaNSW`
                )
        ContactForm
</template>
<style>
  section { background: var(--primary); }
  section, h3 { color: var(--tertiary) }
  .col{
    @media (min-width: 768px) {
      flex: 0 0 50%;
      max-width: 50%;
    }
    &:first-child {
      margin: 0 0 0.75rem;
    }
  }
  .embed-responsive{
    position: relative;
    overflow: hidden;
    &::before {
      content: "";
      display: block;
      width: 100%;
      padding: 56.25% 0 0 0;
    }
    iframe {
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border: 0;
    }
  }
</style>
