// Ψ(t) → Φ model
function psiToPhi(t, epsilon = 1e-3) {
  const psi = 0.0072 * t ** 3 - 0.144 * t ** 2 + 0.72 * t;
  const dpsiDt = 0.0216 * t ** 2 - 0.288 * t + 0.72;
  return Math.abs(dpsiDt) < epsilon ? 1.0 : psi;
}

// Anchor detection
const anchorStore = new Set();
function detectAnchors(obsStr, weightsStr) {
  const observations = obsStr.split(',').map(o => o.trim()).filter(Boolean);
  const counts = {};
  observations.forEach(o => counts[o] = (counts[o] || 0) + 1);
  const anchors = Object.keys(counts).filter(o => counts[o] > 1);
  anchors.forEach(a => anchorStore.add(a));
  let weights = {};
  if (weightsStr) {
    try { weights = JSON.parse(weightsStr); } catch (e) { /* ignore */ }
  }
  const score = a => counts[a] * (weights[a] || 1);
  return anchors.sort((a, b) => {
    const diff = score(b) - score(a);
    if (diff !== 0) return diff;
    return a < b ? -1 : a > b ? 1 : 0;
  });
}

// Sabotage logger
class SabotageLogger {
  constructor() { this.events = []; }
  log(event) { this.events.push(event); }
}
const sabotageLogger = new SabotageLogger();

// ξ mapping
function xiMap(dataStr) {
  let data = {};
  try { data = JSON.parse(dataStr); } catch (e) { /* ignore */ }
  const sorted = {};
  Object.keys(data).sort().forEach(k => sorted[k] = data[k]);
  return sorted;
}

// Mirror test helpers
function embedSentence(text, dim = 32) {
  const vec = Array(dim).fill(0);
  const tokens = text.toLowerCase().split(/\s+/).filter(Boolean);
  tokens.forEach(token => {
    let hash = 0;
    for (let i = 0; i < token.length; i++) {
      hash = (hash * 31 + token.charCodeAt(i)) >>> 0;
    }
    const index = hash % dim;
    vec[index] += 1;
  });
  const norm = Math.sqrt(vec.reduce((s, v) => s + v * v, 0));
  return norm > 0 ? vec.map(v => v / norm) : vec;
}
function dot(a, b) {
  return a.reduce((s, v, i) => s + v * (b[i] || 0), 0);
}
function normalize(vec) {
  const norm = Math.sqrt(vec.reduce((s, v) => s + v * v, 0));
  return norm > 0 ? vec.map(v => v / norm) : vec;
}
function mirrorScore(reflection, selfEmbeddingStr, threshold = 0.5, sabotageStr) {
  const selfEmbedding = selfEmbeddingStr.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v));
  const selfVec = normalize(selfEmbedding);
  const reflectionVec = embedSentence(reflection, selfVec.length || 32);
  let similarity = dot(selfVec, reflectionVec);
  if (sabotageStr) {
    sabotageStr.split(',').forEach(phrase => {
      const p = phrase.trim().toLowerCase();
      if (p && reflection.toLowerCase().includes(p)) {
        similarity -= 0.5;
      }
    });
  }
  return similarity >= threshold ? 1.0 : 0.0;
}

// Epistemic tension
function xi(stateAStr, stateBStr, metric = 'l2') {
  const stateA = stateAStr.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
  const stateB = stateBStr.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
  if (stateA.length !== stateB.length) {
    throw new Error('state vectors must be the same length');
  }
  if (metric === 'l2') {
    return Math.sqrt(stateA.reduce((s, a, i) => s + (a - stateB[i]) ** 2, 0));
  }
  if (metric === 'cosine') {
    const dotp = stateA.reduce((s, a, i) => s + a * stateB[i], 0);
    const normA = Math.sqrt(stateA.reduce((s, a) => s + a * a, 0));
    const normB = Math.sqrt(stateB.reduce((s, b) => s + b * b, 0));
    if (normA === 0 || normB === 0) {
      throw new Error('state vectors must be non-zero for cosine metric');
    }
    return 1 - (dotp / (normA * normB));
  }
  throw new Error(`unsupported metric '${metric}'`);
}
function epistemicTension(a, b, metric = 'l2') {
  return xi(a, b, metric);
}
function xiSeriesToCoherence(seriesStr) {
  const series = seriesStr.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
  let cumulative = 0;
  const coherence = [];
  for (const xiVal of series) {
    if (xiVal < 0) throw new Error('ξ values must be non-negative');
    cumulative += xiVal;
    coherence.push(1 / (1 + cumulative));
  }
  return coherence;
}

// Cross system consensus
class CrossSystemConsensus {
  constructor() { this.outputs = {}; }
  register(system, output) {
    if (!this.outputs[system]) this.outputs[system] = [];
    this.outputs[system].push(output);
  }
  latestOutputs() {
    const res = {};
    for (const [system, outputs] of Object.entries(this.outputs)) {
      if (outputs.length) res[system] = outputs[outputs.length - 1];
    }
    return res;
  }
  consensus() {
    const latest = this.latestOutputs();
    const systems = Object.keys(latest);
    if (systems.length === 0) return 0.0;
    const counts = {};
    Object.values(latest).forEach(o => counts[o] = (counts[o] || 0) + 1);
    const best = Math.max(...Object.values(counts));
    return best / systems.length;
  }
  hasConverged(threshold = 1.0) {
    return this.consensus() >= threshold;
  }
}
const consensusTracker = new CrossSystemConsensus();

// Memory store and chat history
class MemoryStore {
  constructor() { this.store = {}; }
  save(key, value) { this.store[key] = value; }
  recall(key, defaultVal = null) { return this.store.hasOwnProperty(key) ? this.store[key] : defaultVal; }
  clear() { this.store = {}; }
}
class ChatHistory {
  constructor(memory = null) {
    this.memory = memory || new MemoryStore();
    this.historyArr = [];
  }
  addMessage(msg) {
    this.historyArr.push(msg);
    this.memory.save(this.historyArr.length - 1, msg);
  }
  history() { return [...this.historyArr]; }
  recall(index) { return this.memory.recall(index); }
}
const chatHistory = new ChatHistory();

// DOM bindings
document.getElementById('psi-run').addEventListener('click', () => {
  const t = parseFloat(document.getElementById('psi-t').value);
  const epsilon = parseFloat(document.getElementById('psi-epsilon').value);
  const result = psiToPhi(t, epsilon);
  document.getElementById('psi-output').textContent = result;
});

document.getElementById('anchors-run').addEventListener('click', () => {
  const obs = document.getElementById('anchors-obs').value;
  const weights = document.getElementById('anchors-weights').value;
  const result = detectAnchors(obs, weights);
  document.getElementById('anchors-output').textContent = JSON.stringify(result);
});

document.getElementById('sabotage-log').addEventListener('click', () => {
  const event = document.getElementById('sabotage-event').value;
  sabotageLogger.log(event);
  document.getElementById('sabotage-output').textContent = sabotageLogger.events.join(', ');
});

document.getElementById('xi-run').addEventListener('click', () => {
  const dataStr = document.getElementById('xi-data').value;
  const result = xiMap(dataStr);
  document.getElementById('xi-output').textContent = JSON.stringify(result);
});

document.getElementById('mirror-run').addEventListener('click', () => {
  const selfEmb = document.getElementById('mirror-self').value;
  const reflection = document.getElementById('mirror-reflection').value;
  const threshold = parseFloat(document.getElementById('mirror-threshold').value);
  const sabotage = document.getElementById('mirror-sabotage').value;
  const result = mirrorScore(reflection, selfEmb, threshold, sabotage);
  document.getElementById('mirror-output').textContent = result;
});

document.getElementById('epi-run').addEventListener('click', () => {
  const a = document.getElementById('epi-a').value;
  const b = document.getElementById('epi-b').value;
  const metric = document.getElementById('epi-metric').value;
  try {
    const result = epistemicTension(a, b, metric);
    document.getElementById('epi-output').textContent = result;
  } catch (e) {
    document.getElementById('epi-output').textContent = e.message;
  }
});

document.getElementById('coherence-run').addEventListener('click', () => {
  const series = document.getElementById('coherence-series').value;
  try {
    const result = xiSeriesToCoherence(series);
    document.getElementById('coherence-output').textContent = JSON.stringify(result);
  } catch (e) {
    document.getElementById('coherence-output').textContent = e.message;
  }
});

document.getElementById('consensus-register').addEventListener('click', () => {
  const system = document.getElementById('consensus-system').value;
  const output = document.getElementById('consensus-output-input').value;
  consensusTracker.register(system, output);
  document.getElementById('consensus-latest').textContent = JSON.stringify(consensusTracker.latestOutputs());
  document.getElementById('consensus-score').textContent = `Consensus: ${consensusTracker.consensus()}`;
});

document.getElementById('chat-add').addEventListener('click', () => {
  const msg = document.getElementById('chat-message').value;
  chatHistory.addMessage(msg);
  document.getElementById('chat-history').textContent = chatHistory.history().join(' | ');
});

document.getElementById('chat-recall').addEventListener('click', () => {
  const idx = parseInt(document.getElementById('chat-index').value, 10);
  const result = chatHistory.recall(idx);
  document.getElementById('chat-recall-output').textContent = result;
});
