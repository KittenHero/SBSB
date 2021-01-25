const https = require('https');
const fs = require('fs');
const { durations, exclude_durations } = require('./src/utils.js');

const treatments = [
  {
    title: 'Thai Massage',
    description:
    'Enjoy this oil-free massage with stretching and acupressure techniques.  '
    + 'Your body will be positioned in a veriety of yoga like poses while we apply deep and rhythmic pressure.',
    id: 'thai-massage',
    img: '$imgThai',
    small: '$imgThaiSmall',
  },
  {
    title: 'Foot Massage',
    description:
    'Relieve pain by stimulating pressure points on your feet.'
    + '  Reflexology encourages flow of blood and promotes healing,'
    + ' relieving pain at the root level.',
    id: 'foot-massage',
    img: '$imgFoot',
    small: '$imgFootSmall',
  },
  {
    title: 'Aroma Oil Massage',
    description:
    'This gentle and relaxing massage with aromatic herb balm and essential oils will stimulate various systems'
    + ' in your body to help you rejuvenate, relax, promote sleep and relieve pain througout your body.',
    id: 'aroma-oil',
    img: '$imgOil',
    small: '$imgOilSmall',
  },
  {
    title: 'Hot Stone Massage',
    description:
    'Relax your muscles and mind using acient techniques of placing smooth heated stones on key points of your body.'
    + '  The heat if the stones will warm your body, releasing all stress and tension.',
    id: 'stone-massage',
    img: '$imgStone',
    small: '$imgStoneSmall',
  },
  {
    title: 'Deep Tissue Massage',
    description:
    'This massage will work on your deep muscle to balance your body structure and remove tension.',
    id: 'deep-tissue',
    img: '$imgTissue',
    small: '$imgTissueSmall',
  },
  {
    title: 'Remedial Massage',
    description:
    'We test your muscles to determine the cause your pain and tailor the treatment to suit.'
    + '  Great for stiff necks, headaches and sport injuries.',
    id: 'remedial-massage',
    img: '$imgRemedial',
    small: '$imgRemedialSmall',
  },
  {
    title: 'Body Scrub',
    description:
    'Full body exfoliation treatment to remove dead skin cells and stimulate cell renewal.'
    + 'This treatment will leave your body smooth and silky soft.',
    id: 'body-scrub',
    img: '$imgScrub',
    small: '$imgScrubSmall',
  },
  {
    title: 'Facial Massage',
    description:
    'Give your skin a youthful glow with this anti-aging treatment, helping prevent wrinkles and increase circulation.'
    + '  Can also relieve allergy symptoms and congestion by improving drainage.',
    id: 'facial-massage',
    img: '$imgFacial',
    small: '$imgFacialSmall',
  },
];

const customer = {
  name: 'api',
  email: 'test@sabaisabaithaimassage.com.au',
  phone: '000 0000 000',
}

const items = treatments
  .map(
    t => Object.keys(durations)
    .map(d => ({ massage_type: t.title, duration: d }))
  ).flat()
  .filter(
    i => !(i.massage_type in exclude_durations)
    || !exclude_durations[i.massage_type].includes(durations[i.duration])
  );


const promise = new Promise((resolve, reject) => {
  if (process.env.NODE_ENV !== 'production') return reject('NODE_ENV is not production');
  const req = https.request(
    {
      hostname: 'api.sabaisabaithaimassage.com.au',
      path: '/purchase',
      method: 'POST'
    },
    req => req.on('data',
      d => req.statusCode === 200 ? resolve(JSON.parse(d.toString())) : reject(d.toString()),
    )
  );
  req.write(JSON.stringify({ customer, items }))
  req.end();
}).then(
  parsed => treatments.map(t => Object.assign(
    t,
    {
      prices: Object.fromEntries(
        parsed.items
        .filter(i => i.massage_type == t.title)
        .map(i => [durations[i.duration], i.price])
      )
    }
  ))
).then(t => JSON.stringify(t).replaceAll(/"\$([^"]+)"/g, '$1'))
  .then(t =>
`import imgThai from './assets/img/treatments/thai-massage.jpg';
import imgFoot from './assets/img/treatments/foot-massage.jpg';
import imgOil from './assets/img/treatments/oil-massage.jpg';
import imgStone from './assets/img/treatments/hot-stone.jpg';
import imgTissue from './assets/img/treatments/deep-tissue-massage.jpg';
import imgRemedial from './assets/img/treatments/remedial-massage.jpg';
import imgScrub from './assets/img/treatments/body-scrub.jpg';
import imgFacial from './assets/img/treatments/facial-massage.jpg';

import imgThaiSmall from './assets/img/treatments/thai-massage-small.jpg';
import imgFootSmall from './assets/img/treatments/foot-massage-small.jpg';
import imgOilSmall from './assets/img/treatments/oil-massage-small.jpg';
import imgStoneSmall from './assets/img/treatments/hot-stone-small.jpg';
import imgTissueSmall from './assets/img/treatments/deep-tissue-massage-small.jpg';
import imgRemedialSmall from './assets/img/treatments/remedial-massage-small.jpg';
import imgScrubSmall from './assets/img/treatments/body-scrub-small.jpg';
import imgFacialSmall from './assets/img/treatments/facial-massage-small.jpg';

export default ${t};
`)
 .then(str => fs.writeFile('src/data.js', str, err => err ? console.warn(err) : console.log(str)))
 .catch(err => console.warn(err));
