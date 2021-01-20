import App from './App.svelte';
import treatments from './data.js';

const { html, head, css } = App.render({ treatments });

export default `
<!DOCTYPE html>
<html lang="en">
  <head>
    ${head}
    <style>
      ${css && css.code}
    </style>
  </head>
  <body id="page-top">
    ${html}
  </body>
</html>`;
