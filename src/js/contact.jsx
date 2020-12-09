import React, { useReducer, useEffect } from 'react'

const FormInput = ({id, type, value, required, placeholder, error, onChange}) => {
  return pug`
.form-group
    input.form-control(id=id, value=value, required=required, placeholder=placeholder, onChange=onChange)
    if error
      p.help-block.text-danger= error`
}

const initialState = {
  name: '',
  email: '',
  phone: '',
  message: '',
  submitting: 0,
  success: 0,
  errors: {}
}

const formReducer = (state, action) => {
  switch (action.type) {
    case 'name':
      return { ...state, name: action.value, errors: {...state.errors, name: 0} }
    case 'email':
      return { ...state, email: action.value, errors: {...state.errors, email: 0} }
    case 'phone':
      return { ...state, phone: action.value, errors: {...state.errors, phone: 0} }
    case 'message':
      return { ...state, message: action.value, errors: {...state.errors, message: 0} }
    case 'submit':
      let errors = {};
      if (!state.name) { errors.name = 1 }
      if (!state.message) { errors.message = 1 }
      if (!state.phone) { errors.phone = 1 }
      if (!state.email || !state.email.includes('@')) { errors.email = 1 }
      if (errors.email | errors.phone | errors.name | errors.message) return { ...state, errors }
      else return { ...state, submitting: 1 }
    case 'fail':
      return { ...state, errors: { ...state.errors, submit: 1 } }
    case 'success':
      return { ...initialState, success: 1 }
    case 'close':
      return { ...state, success: 0 }
  }
  return state
}

const ContactForm = (props) => {
  const [{ name, email, phone, message, submitting, success, errors }, dispatch] = useReducer(formReducer, initialState)
  useEffect(() => {
    if (submitting) {
      fetch('https://api.sabaisabaithaimassage.com.au/contact', {
        method: 'POST',
        body: JSON.stringify({
          subject: `Message from ${name}`,
          text:
          `from: ${name}\n`
          + `phone: ${phone}\n`
          + `email: ${email}\n`
          + `message: ${message}`,
          html:
          `<ul><li>from: ${name}</li>`
          + `<li>phone: <a href="tel:${phone}>${phone}</a></li>`
          + `<li>email: <a href="mailto:${email}>${email}</a></li>`
          + `<li>message: <p>${message}</p></li></ul>`,
        })
      }).then(() => dispatch({ type: 'success' }))
        .catch(() => dispatch({ type: 'fail' }))
    }
  }, [submitting])

  return pug`
.row.align-items-stretch.mb-3
    .col-lg-6.mb-2
        FormInput(
          type='text',
          value=name,
          placeholder='Your Name *',
          required='required',
          onChange=(e) => dispatch({ type: 'name', value: e.target.value }),
          error=errors.name && 'Please enter your name.'
        )
        FormInput(
          type='email',
          value=email,
          placeholder='Your Email *',
          required='required',
          onChange=(e) => dispatch({ type: 'email', value: e.target.value }),
          error=errors.email && 'Please enter your email address.'
        )
        FormInput(
          type='tel',
          value=phone,
          placeholder='Your Phone *',
          required='required',
          onChange=(e) => dispatch({ type: 'phone', value: e.target.value }),
          error=errors.phone && 'Please enter your phone number.'
        )
    .col-lg-6.mb-2
        .form-group.form-group-textarea.mb-md-0
            textarea#message.form-control(
              value=message,
              placeholder='Your Message *',
              onChange=(e) => dispatch({ type: 'message', value: e.target.value }),
              required='required'
            )
            if errors.message
                p.help-block.text-danger Please enter a message.
.text-center
        if success
            .alert.alert-success
                strong Your message has been sent.
                button.close(aria-hidden=true) &times;
        button#sendMessageButton.btn.btn-primary.btn-xl.text-uppercase(onClick=() => dispatch({ type: 'submit' })) Send Message
        if errors.submit
            p.help-block.text-danger Unknown error occured.  Unable to contact the server.`
}

export default ContactForm;
