<script>
  let name       = '',
      email      = '',
      phone      = '',
      message    = '',
      submitting = 0,
      success    = 0,
      error      = 0;

  function onClick() {
    if (!name || !message || !phone || !email) {
      error = 1;
      return 0;
    }
    submitting = 1;
    const body = JSON.stringify({
      subject: `Message from ${name}`,
      text:
      `from: ${name}\n`
      + `phone: ${phone}\n`
      + `email: ${email}\n`
      + `message: ${message}`,
      html:
      `<ul><li>from: ${name}</li>`
      + `<li>phone: <a href="tel:${phone}">${phone}</a></li>`
      + `<li>email: <a href="mailto:${email}">${email}</a></li>`
      + `<li>message: <p>${message}</p></li></ul>`,
    });
    fetch(`${API_URL}/contact`, { method: 'POST', body })
      .then(() => { success = 1;})
      .catch(() => { error = 2; })
      .finally(() => { submitting = 0; })
    return 0;
  }
  function close() {
    success = 0;
    return 0;
  }
</script>

<template>
  form.col
    .row
      .col
        .form-group
          input(bind:value=`{name}` class:empty!=`{!error && !name}` type='text' placeholder='Your Name *' title='Enter your name' required)
          +if('error && !name')
            p Please enter your name.
        .form-group
          input(bind:value=`{email}` class:empty!=`{!error && !email}` type='email' placeholder='Your Email *' title='Enter your email' required)
          +if('error && (!email || !email.includes("@"))')
            p Please enter your email address.
        .form-group
          input(bind:value=`{phone}` class:empty!=`{!error && !phone}` type='tel' placeholder='Your Phone *' title='Enter your phone number' required)
          +if('error && !phone')
            p Please enter your phone number.
      .col
        .form-group.textarea
          textarea(bind:value=`{message}` class:empty!=`{!error && !message}` placeholder='Your Message *' title='Enter your message' required)
          +if('error && !message')
            p Please enter a message.
    .text-center
       +if('success')
         .alert.success
           strong Your message has been sent.
           button.close(aria-label='Close' on:click=`{close}`) &times;
       button.btn.btn-xl(class:loading=`{submitting}` on:click=`{onClick}`) Send Message
       +if('error == 2')
         p Unknown error occured.  Unable to contact the server.
</template>

<style>
  form.col {
    margin-bottom: 0;
    @media (min-width: 768px) {
      flex: 0 0 50%;
      max-width: 50%;
    }
  }
  p {
    margin: 0;
    color: var(--error);
  }
  button {
    margin-top: 1rem;
  }
  .row {
    align-items: stretch;
    margin-bottom: 1rem;
  }
  .col {
    margin-bottom: 0.5rem;
    @media (min-width: 992px) {
      flex: 0 0 50%;
      max-width: 50%;
    }
  }
  input, textarea {
    height: auto;
    padding: 1.25rem;
  }
</style>
