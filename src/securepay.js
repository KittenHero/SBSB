import SecurePayUI from 'securepay';

const ui = new SecurePayUI.init({
  containerId: 'securepay-container',
  scriptId: 'securepay-js',
  clientId: SECUREPAY_CLIENT,
  merchantCode: SECUREPAY_MERCHANT,
  card: {
    onTokeniseSuccess: (card) => {
      console.log(card);
    },
    onTokeniseError: (err) => console.log(err),
  }
})
