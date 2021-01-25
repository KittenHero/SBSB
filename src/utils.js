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

module.exports = { durations, duration_reverse, exclude_durations };
