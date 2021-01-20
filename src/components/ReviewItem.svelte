<script>
  export let img;
  export let date;
</script>

<template>
  .col.profile-img
    img.mx-auto.rounded-circle(src=`{img}` alt='')
  .col.review-info
    h4 {date}
    slot(name='text')
</template>

<style>
  .profile-img {
    display: none;
    text-align: right;
    padding: 0.5rem 0.75rem;

    @media (min-width: 576px) {
      display: block;
      flex: 0 0 33.3333333333%;
      max-width: 33.3333333333%;
    }

    img {
      object-fit: cover;
      width: 6rem;
      height: 6rem;
      border-radius: 50%;
      margin: 0 auto;
    }
  }
  .review-info {
    padding: 0.5rem;
    @media (min-width: 576px) {
      flex: 0 0 66.6666666667%;
      max-width: 66.6666666667%;
    }
    h4 {
      margin: 0;
    }
  }
</style>
