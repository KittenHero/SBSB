<script context="module">
  import ReviewItem from './ReviewItem.svelte';

  import img1 from '../assets/img/treatments/hot-stone-small.jpg';
  import img2 from '../assets/img/treatments/facial-massage-small.jpg';
  import img3 from '../assets/img/treatments/thai-massage-small.jpg';
  import img4 from '../assets/img/treatments/remedial-massage-small.jpg';
</script>

<template>
  section#reviews
    .container
      h2 Reviews
      h3 Leave a review for us on 
        a(href='https://g.page/saibaithai/review?rc') Google 
        |  or 
        a(href='https://www.facebook.com/pg/Sabaisabaithai/reviews/') Facebook
      .row
        ReviewItem(img=`{img1}` date=2019)
          p(slot='text')
            | Walked past with my partner and decided we wanted a massage. They fit us in no worries right away and put us in a room together for a couples massage. 
            | It smelt nice inside, the music was calming and the massage was wonderful. The bonus was that it\'s wasn\'t too expensive 
            | and we could claim it back from health insurance at the end. Would definitely recommend this place.
        ReviewItem(img=`{img2}` date=2019)
          p(slot='text')
            | Me and my boyfriend visited for the first time. I wasn’t expected much as it in tourist center. 
            | But we were so impressed of how much effort they gave to the massage. 
            | Pressure was on point and hit all the spots. Truly professional authentic Thai massage. 
            | Highly recommend this place.
        ReviewItem(img=`{img3}` date=2019)
          p(slot='text') Fantastic massage very professional & lovely staff.
        ReviewItem(img=`{img4}` date=2002)
          p(slot='text') Amazing massage experience every time. Very professional and lovely staff.
</template>

<style>
  p {
    color: var(--text-muted);
  }
</style>
