const durations = Object.freeze({
  '02:00:00': 120,
  '01:30:00': 90,
  '01:00:00': 60,
  '00:45:00': 45,
  '00:30:00': 30,
});
const duration_reverse = Object.freeze(
  Object.fromEntries(
    Object.entries(durations).map(([k,v]) => [v,k])
  )
);

const exclude_durations = Object.freeze({
  'Facial Massage': [120],
  'Body Scrub': [120],
});

function itemsTotal(items) {
  return items.reduce((sub, item) => +item.net_price + sub, 0).toFixed(2);
}

function purchase(data) {
  if (!data.items) return Promise.reject(new TypeError('Data invalid'));
  const body = JSON.stringify({
    ...data,
    items: data.items.map(i => ({
      ...i,
      duration: duration_reverse[i.duration],
    })),
  });
  return fetch(`${API_URL}/purchase`, { method: 'POST', body }).then(r => {
    if (r.ok) return r.json();
    if (r.status === 400) return r.json().then(d => { throw d });
    else return r.text().then(d => { throw d });
  }).then(d => ({
    ...d,
    items: d.items.map(i => ({
      ...i,
      duration: durations[i.duration],
    })),
  }));
}

function contact({ name, phone, email, message }) {
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
  return fetch(`${API_URL}/contact`, { method: 'POST', body }).then(r =>
    r.status == 200 ? Promise.resolve() : Promise.reject()
  );
}

module.exports = {
  durations,
  duration_reverse,
  exclude_durations,
  itemsTotal,
  api: { purchase, contact },
};
