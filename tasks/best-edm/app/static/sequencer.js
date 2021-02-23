samples = [
    '2kicks_1.mp3',
    'bass_a_1.mp3',
    'bass_b_1.mp3',
    'bass_d_1.mp3',
    'bass_f_1.mp3',
    'chord_a_1.mp3',
    'chord_b_1.mp3',
    'chord_d_1.mp3',
    'chord_f_1.mp3',
    'hats_1.mp3',
    'hats_fast_1.mp3',
    'kick_1.mp3',
    'kick_and_snare_1.mp3',
    'single_hat_1.mp3',
    'snare_1.mp3',
    'snare_fill_1.mp3'
].map(x => ({
    name: x,
    audio: new Audio(`/static/samples/${x}`)
}));

[sequencer, tracks, grid, play, stop] = [
    'sequencer',
    'tracks',
    'grid',
    'play',
    'stop'
].map(x => document.getElementById(x));

const generateTrack = (sample, idx) => {
    return `
<div class="track" data-sample="${idx}">
${stripExtension(sample.name)}
</div>
`;
};

const stripExtension = s => s.split('.')[0];
const range = n => [...Array(n).keys()];

const generateBar = (samples, id) => {
    return samples.map((sample, idx) =>
        `<div class="node" data-bar="${id}" data-sample="${idx}" data-on="false" onclick="toggleNode(this)"></div>`
    );
};

const generateGrid = (samples, nBars) =>
      range(nBars).map(bar =>
          `
<div class="bar" data-bar="${bar}">
  ${generateBar(samples, bar).join('  \n')}
</div>`
      ).join('\n');

const initialize = async () => {
    tracks.innerHTML = samples.map(generateTrack).join('\n');
    grid.innerHTML = generateGrid(samples, 16);
};

toggleNode = el => {
    data = el.dataset;
    isOn = data.on === 'true';    
    data.on = !isOn;
    el.classList.toggle('node--on');
};

const sleep = (ms) =>
  new Promise(resolve => setTimeout(resolve, ms));

const playBar = bar => {
    nodes = [...bar.children];
    nodes.filter(node => node.dataset.on === 'true')
        .map(x => {
            tmp = samples[x.dataset.sample].audio.cloneNode();
            tmp.play();
        });
};

const playGrid = async () => {
    bars = [...grid.children];
    for await (let bar of bars) {
        bar.classList.toggle('bar--on');
        playBar(bar);
        await sleep(620);
        bar.classList.toggle('bar--on');
    };
};

document.onload = initialize();
