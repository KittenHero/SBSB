<script context="module">
  import favicon from '../assets/img/favicon.ico';
</script>

<template>
  svelte:head
    meta(charset='utf-8')
    meta(name='viewport' content='width=device-widthinitial-scale=1shrink-to-fit=no')
    meta(name='description' content='Welcome to Sabai Sabai Thai Massage & Day Spa Located in the heart of Cronulla. We are the ultimate hub for health and well being offering the best range of quality health services.')
    meta(name='author' content='Naris R.')
    title Sabai Sabai Thai Massage &amp; Day Spa
    link(rel='icon' type='image/x-icon' href='{favicon}')

    link(href='https://fonts.googleapis.com/css?family=Droid+Serif:400700400italic700italic' rel='stylesheet' type='text/css')
    +if('GOOGLE_TAG_KEY != 0')
      script.
        (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});
          var f=d.getElementsByTagName(s)[0], j=d.createElement(s), dl=l!='dataLayer'?'&l='+l:'';
          j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer',GOOGLE_TAG_KEY);
  noscript
    +if('GOOGLE_TAG_KEY != 0')
      iframe(src=`https://www.googletagmanager.com/ns.html?id=${GOOGLE_TAG_KEY}`
        title="google-tag-manager" height="0" width="0" style="display:none;visibility:hidden")
    .alert.danger This site requires javascript to work properly.
</template>

<style>
  .alert {
    position: fixed;
    top: 10rem;
    left: 0;
    right: 0;
    z-index: 1;
  }
</style>
