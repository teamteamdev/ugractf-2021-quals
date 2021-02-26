// helper
function debounce(a,b,c){var d;return function(){var e=this,f=arguments;clearTimeout(d),d=setTimeout(function(){d=null,c||a.apply(e,f)},b),c&&!d&&a.apply(e,f)}};

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

[sequencer, tracks, grid, play, randomize, bounce, info, infoHeader] = [
    'sequencer',
    'tracks',
    'grid',
    'play',
    'randomize',
    'bounce',
    'info',
    'infoHeader',
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

const rndBool = () =>
      Math.random() > 0.9;

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

const readBar = bar => {
    nodes = [...bar.children];
    return nodes
        .map((node, idx) => node.dataset.on === 'true' ? idx : -1)
        .filter(node => node >= 0);
}

const exportGrid = () => {
    bars = [...grid.children];
    return bars.map(readBar);
}

const serializeGrid = exportedGrid =>
      btoa(exportedGrid.map(bar => bar.join()).join(';'));

const randomizeGrid = () => {
    bars = [...grid.children];
    bars.map(bar => {
        nodes = [...bar.children];
        nodes.forEach(node => rndBool() && toggleNode(node));
    });
}

document.onload = initialize();

// info panel

infoText = {
    track: ["All enabled grid nodes on a track line will trigger the corresponding sound.", "Track Name"],
    node: ["Click to toggle a grid node on or off. Enabled grid node produces a sound when the locator is on a node’s bar.", "Grid Node"],
    bounce: ["Use the Export/Bounce panel to download audio version of this file.", "Export/Bounce Panel"],
    play: ["Click to start playback.", "Play Button"],
    stop: ["Click to stop playback.", "Stop Button"],
    randomize: ["Click to fill the grid with random notes.", "Randomize Button"],
    sequencer: ["Sequencer area contains the grid of current project. You can draw a pattern here.", "Sequencer Area"],
    default: [info.innerHTML, infoHeader.innerHTML]
};

const showInfo = e => {
    target = e.target.id || e.target.classList;
    [text, header] = infoText[target] || infoText['default'];
    info.innerHTML = text;
    infoHeader.innerHTML = header;
}

document.body.addEventListener("mouseover", debounce(e => showInfo(e), 25));
