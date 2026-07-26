"use strict";

/**
 * Standalone, portable version of the "BFS shortest path" step-by-step
 * visualization. No dependency on any chat/host environment: plain
 * HTML + CSS + JS, works by simply opening index.html in a browser.
 *
 * It reuses the same seeded backtracker maze as the other stepper demo
 * (maze-stepper), then runs a BFS from START to END and records one
 * frame per step so the whole run can be replayed.
 */

const WIDTH = 5;
const HEIGHT = 4;
const CELL_SIZE = 44;
const START = [0, 0];
const END = [4, 3];

// Seeded PRNG (mulberry32) so the demo maze is reproducible.
function mulberry32(seed) {
  return function () {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// direction -> (dx, dy)
const DIRECTIONS = {
  N: [0, -1],
  E: [1, 0],
  S: [0, 1],
  W: [-1, 0],
};

const key = (cell) => `${cell[0]},${cell[1]}`;

/** Build the same maze walls as the backtracker stepper demo (seed 7). */
function buildMaze(width, height, seed) {
  const rng = mulberry32(seed);
  const openEast = Array.from({ length: height }, () =>
    Array(width).fill(false)
  );
  const openSouth = Array.from({ length: height }, () =>
    Array(width).fill(false)
  );
  const visited = new Set(["0,0"]);
  const stack = [[0, 0]];

  while (stack.length) {
    const [x, y] = stack[stack.length - 1];
    const candidates = [];
    for (const [dir, [dx, dy]] of Object.entries(DIRECTIONS)) {
      const nx = x + dx;
      const ny = y + dy;
      if (
        nx >= 0 &&
        nx < width &&
        ny >= 0 &&
        ny < height &&
        !visited.has(`${nx},${ny}`)
      ) {
        candidates.push([dir, nx, ny]);
      }
    }
    if (!candidates.length) {
      stack.pop();
      continue;
    }
    const [dir, nx, ny] = candidates[Math.floor(rng() * candidates.length)];
    if (dir === "E") openEast[y][x] = true;
    if (dir === "W") openEast[ny][nx] = true;
    if (dir === "S") openSouth[y][x] = true;
    if (dir === "N") openSouth[ny][nx] = true;
    visited.add(`${nx},${ny}`);
    stack.push([nx, ny]);
  }

  return { openEast, openSouth };
}

function wallOpen(maze, x, y, dir) {
  if (dir === "E") return maze.openEast[y][x];
  if (dir === "W") return x > 0 && maze.openEast[y][x - 1];
  if (dir === "S") return maze.openSouth[y][x];
  if (dir === "N") return y > 0 && maze.openSouth[y - 1][x];
  return false;
}

/** Run BFS from START to END, recording one frame per meaningful step. */
function buildFrames(maze) {
  const queue = [START];
  const visited = new Set([key(START)]);
  const prev = {};

  const frames = [
    {
      phase: "pop",
      action: null,
      current: null,
      queue: queue.map((c) => c.slice()),
      visited: new Set(visited),
      pathCells: new Set(),
      desc: `File initialisée avec le départ (${START}).`,
    },
  ];

  let found = false;
  while (queue.length && !found) {
    const cur = queue.shift();
    if (key(cur) === key(END)) {
      frames.push({
        phase: "found",
        action: "found",
        current: cur,
        queue: queue.map((c) => c.slice()),
        visited: new Set(visited),
        pathCells: new Set(),
        desc: `Sortie (${END}) dépilée : on arrête l'exploration.`,
      });
      found = true;
      break;
    }
    const discovered = [];
    for (const [dir, [dx, dy]] of Object.entries(DIRECTIONS)) {
      if (!wallOpen(maze, cur[0], cur[1], dir)) continue;
      const nxt = [cur[0] + dx, cur[1] + dy];
      if (visited.has(key(nxt))) continue;
      visited.add(key(nxt));
      prev[key(nxt)] = [cur, dir];
      queue.push(nxt);
      discovered.push(nxt);
    }
    frames.push({
      phase: "pop",
      action: "pop",
      current: cur,
      queue: queue.map((c) => c.slice()),
      visited: new Set(visited),
      pathCells: new Set(),
      desc: `(${cur}) dépilée. Voisines découvertes : ${
        discovered.length
          ? discovered.map((c) => `(${c})`).join(", ")
          : "aucune (déjà visitées ou mur fermé)"
      }.`,
    });
  }

  // Reconstruct the path frame by frame (walking backwards via prev).
  let node = END;
  const pathSoFar = new Set([key(END)]);
  frames.push({
    phase: "reconstruct",
    action: "reconstruct",
    current: node,
    queue: [],
    visited: new Set(visited),
    pathCells: new Set(pathSoFar),
    desc: `Reconstruction : on part de la sortie (${END}) et on remonte via prev.`,
  });
  while (key(node) !== key(START)) {
    const [parent, dir] = prev[key(node)];
    pathSoFar.add(key(parent));
    frames.push({
      phase: "reconstruct",
      action: "reconstruct",
      current: parent,
      queue: [],
      visited: new Set(visited),
      pathCells: new Set(pathSoFar),
      desc: `prev[(${node})] = (${parent}), direction ${dir}. On continue vers (${parent}).`,
    });
    node = parent;
  }
  frames.push({
    phase: "done",
    action: "done",
    current: null,
    queue: [],
    visited: new Set(visited),
    pathCells: new Set(pathSoFar),
    desc: "Chemin reconstruit en partant de la sortie ; path.reverse() le remet dans le bon sens (entrée -> sortie).",
  });

  return frames;
}

const CODE_LINES = [
  { text: "queue = [start]; visited = {start}", group: null },
  { text: "", group: null },
  { text: "while queue:", group: null },
  { text: "    cur = queue.popleft()", group: "pop" },
  { text: "    if cur == end:", group: "found" },
  { text: "        break", group: "found" },
  { text: "    for neighbor in open_neighbors(cur):", group: "pop" },
  { text: "        if neighbor not in visited:", group: "pop" },
  { text: "            prev[neighbor] = (cur, direction)", group: "pop" },
  { text: "            queue.append(neighbor)", group: "pop" },
  { text: "", group: null },
  { text: "node = end", group: "reconstruct" },
  { text: "while node != start:", group: "reconstruct" },
  { text: "    parent, direction = prev[node]", group: "reconstruct" },
  { text: "    path.append(direction)", group: "reconstruct" },
  { text: "    node = parent", group: "reconstruct" },
  { text: "path.reverse()", group: "done" },
];

function buildCodePanel(container) {
  container.innerHTML = "";
  const lineEls = [];
  for (const line of CODE_LINES) {
    const span = document.createElement("span");
    span.className = "code-line";
    span.dataset.group = line.group || "";
    span.textContent = line.text || "\u00a0";
    container.appendChild(span);
    lineEls.push(span);
  }
  return lineEls;
}

function buildGrid(container, width, height) {
  container.style.gridTemplateColumns = `repeat(${width}, ${CELL_SIZE}px)`;
  const cellEls = [];
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const cell = document.createElement("div");
      cell.className = "maze-cell";
      cell.style.width = `${CELL_SIZE}px`;
      cell.style.height = `${CELL_SIZE}px`;
      container.appendChild(cell);
      cellEls.push(cell);
    }
  }
  return cellEls;
}

function init() {
  const maze = buildMaze(WIDTH, HEIGHT, 7);
  const frames = buildFrames(maze);

  const gridEl = document.getElementById("grid");
  const descEl = document.getElementById("desc");
  const counterEl = document.getElementById("counter");
  const queueEl = document.getElementById("queue");
  const prevBtn = document.getElementById("prev");
  const nextBtn = document.getElementById("next");
  const codeEl = document.getElementById("code");

  const cellEls = buildGrid(gridEl, WIDTH, HEIGHT);
  const lineEls = buildCodePanel(codeEl);

  let idx = 0;

  function render() {
    const frame = frames[idx];
    const queueSet = new Set(frame.queue.map((c) => c.join(",")));

    for (let y = 0; y < HEIGHT; y++) {
      for (let x = 0; x < WIDTH; x++) {
        const el = cellEls[y * WIDTH + x];
        const closedEast = !maze.openEast[y][x];
        const closedSouth = !maze.openSouth[y][x];
        el.style.borderRight = closedEast
          ? "2px solid #33322f"
          : "2px solid transparent";
        el.style.borderBottom = closedSouth
          ? "2px solid #33322f"
          : "2px solid transparent";

        const k = `${x},${y}`;
        const isCurrent = frame.current && frame.current[0] === x && frame.current[1] === y;
        const inPath = frame.pathCells.has(k);
        const inQueue = queueSet.has(k);
        const isVisited = frame.visited.has(k);

        el.classList.remove(
          "cell-visited",
          "cell-queue",
          "cell-path",
          "cell-current"
        );
        if (isVisited) el.classList.add("cell-visited");
        if (inQueue) el.classList.add("cell-queue");
        if (inPath) el.classList.add("cell-path");
        if (isCurrent) el.classList.add("cell-current");

        let label = "";
        if (x === START[0] && y === START[1]) label = "D";
        if (x === END[0] && y === END[1]) label = "S";
        if (isCurrent) label = "\u25cf";
        el.textContent = label;
      }
    }

    descEl.textContent = frame.desc;
    counterEl.textContent = `${idx + 1} / ${frames.length}`;
    queueEl.innerHTML = frame.queue.length
      ? frame.queue
          .map((c) => `<span class="queue-chip">(${c[0]},${c[1]})</span>`)
          .join("")
      : `<span class="queue-empty">vide</span>`;

    for (const span of lineEls) {
      span.classList.toggle(
        "line-active",
        span.dataset.group !== "" && span.dataset.group === frame.action
      );
    }

    prevBtn.disabled = idx === 0;
    nextBtn.disabled = idx === frames.length - 1;
  }

  prevBtn.addEventListener("click", () => {
    if (idx > 0) {
      idx -= 1;
      render();
    }
  });
  nextBtn.addEventListener("click", () => {
    if (idx < frames.length - 1) {
      idx += 1;
      render();
    }
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") nextBtn.click();
    if (event.key === "ArrowLeft") prevBtn.click();
  });

  render();
}

document.addEventListener("DOMContentLoaded", init);
