"use strict";

/**
 * Standalone, portable version of the "backtracker maze" step-by-step
 * visualization. No dependency on any chat/host environment: plain
 * HTML + CSS + JS, works by simply opening index.html in a browser.
 */

const WIDTH = 5;
const HEIGHT = 4;
const CELL_SIZE = 44;

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

/**
 * Runs the same recursive-backtracker algorithm as the Python
 * MazeGenerator, but records one "frame" per action (carve or
 * backtrack) so the whole run can be replayed step by step.
 */
function buildFrames(width, height, seed) {
  const rng = mulberry32(seed);

  const openEast = Array.from({ length: height }, () =>
    Array(width).fill(false)
  );
  const openSouth = Array.from({ length: height }, () =>
    Array(width).fill(false)
  );
  const visited = new Set(["0,0"]);
  const stack = [[0, 0]];

  const cloneGrids = () => ({
    openEast: openEast.map((row) => row.slice()),
    openSouth: openSouth.map((row) => row.slice()),
  });

  const frames = [
    {
      action: "start",
      cur: [0, 0],
      stack: [[0, 0]],
      ...cloneGrids(),
      desc: "Départ : (0,0) empilée et marquée visitée.",
    },
  ];

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
      frames.push({
        action: "backtrack",
        cur: stack.length ? stack[stack.length - 1] : [x, y],
        stack: stack.map((c) => c.slice()),
        ...cloneGrids(),
        desc: `Impasse en (${x},${y}) : plus de voisine libre. Retour (pop)${
          stack.length ? ` à (${stack[stack.length - 1]})` : " (pile vide)"
        }.`,
      });
      continue;
    }

    const [dir, nx, ny] = candidates[Math.floor(rng() * candidates.length)];
    if (dir === "E") openEast[y][x] = true;
    if (dir === "W") openEast[ny][nx] = true;
    if (dir === "S") openSouth[y][x] = true;
    if (dir === "N") openSouth[ny][nx] = true;
    visited.add(`${nx},${ny}`);
    stack.push([nx, ny]);
    frames.push({
      action: "carve",
      cur: [nx, ny],
      stack: stack.map((c) => c.slice()),
      ...cloneGrids(),
      desc: `(${x},${y}) → voisine (${nx},${ny}) choisie au hasard. Mur ${dir} ouvert.`,
    });
  }

  return { frames, visited };
}

const CODE_LINES = [
  { text: "stack = [start]", group: null },
  { text: "visited = {start}", group: null },
  { text: "", group: null },
  { text: "while stack:", group: null },
  { text: "    x, y = stack[-1]", group: null },
  { text: "    candidates = unvisited neighbors", group: null },
  { text: "", group: null },
  { text: "    if not candidates:", group: "backtrack" },
  { text: "        stack.pop()", group: "backtrack" },
  { text: "    else:", group: "carve" },
  { text: "        open_wall(x, y, direction)", group: "carve" },
  { text: "        stack.append(next_cell)", group: "carve" },
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
  const { frames, visited } = buildFrames(WIDTH, HEIGHT, 7);

  const gridEl = document.getElementById("grid");
  const descEl = document.getElementById("desc");
  const counterEl = document.getElementById("counter");
  const stackEl = document.getElementById("stack");
  const prevBtn = document.getElementById("prev");
  const nextBtn = document.getElementById("next");
  const codeEl = document.getElementById("code");

  const cellEls = buildGrid(gridEl, WIDTH, HEIGHT);
  const lineEls = buildCodePanel(codeEl);

  let idx = 0;

  function render() {
    const frame = frames[idx];
    const stackSet = new Set(frame.stack.map((c) => c.join(",")));

    for (let y = 0; y < HEIGHT; y++) {
      for (let x = 0; x < WIDTH; x++) {
        const el = cellEls[y * WIDTH + x];
        const closedEast = !frame.openEast[y][x];
        const closedSouth = !frame.openSouth[y][x];
        el.style.borderRight = closedEast
          ? "2px solid #33322f"
          : "2px solid transparent";
        el.style.borderBottom = closedSouth
          ? "2px solid #33322f"
          : "2px solid transparent";

        const key = `${x},${y}`;
        const isCurrent = frame.cur[0] === x && frame.cur[1] === y;
        const inStack = stackSet.has(key);

        el.classList.remove("cell-current", "cell-stack", "cell-visited");
        if (isCurrent) {
          el.classList.add("cell-current");
        } else if (inStack) {
          el.classList.add("cell-stack");
        } else if (visited.has(key)) {
          el.classList.add("cell-visited");
        }
        el.textContent = isCurrent ? "\u25cf" : "";
      }
    }

    descEl.textContent = frame.desc;
    counterEl.textContent = `${idx + 1} / ${frames.length}`;
    stackEl.innerHTML = frame.stack
      .map((c) => `<span class="stack-chip">(${c[0]},${c[1]})</span>`)
      .join("");

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
