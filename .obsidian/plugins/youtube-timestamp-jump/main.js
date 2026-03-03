const obsidian = require("obsidian");
const TIMESTAMP_REGEX = /\((\d+):(\d+)(?::(\d+))?\)/g;

function parseTimestampToSeconds(match, g1, g2, g3) {
  const h = g3 != null ? parseInt(g1, 10) : 0;
  const m = g3 != null ? parseInt(g2, 10) : parseInt(g1, 10);
  const s = g3 != null ? parseInt(g3, 10) : parseInt(g2, 10);
  return h * 3600 + m * 60 + s;
}

function setIframeStartTime(iframe, seconds) {
  const src = iframe.getAttribute("src") || "";
  if (!src.includes("youtube.com/embed")) return;
  const url = new URL(src);
  url.searchParams.set("start", String(seconds));
  url.searchParams.set("autoplay", "1");
  iframe.setAttribute("src", url.toString());
}

function findFirstYoutubeIframe(container) {
  const view =
    container.closest(".markdown-preview-view") ||
    container.closest(".cm-s-obsidian");
  if (!view) return null;
  return view.querySelector('iframe[src*="youtube.com/embed"]');
}

function processElement(el) {
  const walker = document.createTreeWalker(
    el,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );
  const textNodes = [];
  let n;
  while ((n = walker.nextNode())) textNodes.push(n);
  textNodes.forEach((textNode) => {
    const text = textNode.textContent;
    if (!TIMESTAMP_REGEX.test(text)) return;
    TIMESTAMP_REGEX.lastIndex = 0;
    const parts = [];
    let lastIndex = 0;
    let match;
    TIMESTAMP_REGEX.lastIndex = 0;
    while ((match = TIMESTAMP_REGEX.exec(text)) !== null) {
      const seconds = parseTimestampToSeconds(
        match[0],
        match[1],
        match[2],
        match[3]
      );
      parts.push(
        document.createTextNode(text.slice(lastIndex, match.index))
      );
      const span = document.createElement("span");
      span.className = "yt-timestamp-jump";
      span.setAttribute("data-seconds", String(seconds));
      span.textContent = match[0];
      span.setAttribute("title", "Click to seek video to " + match[0]);
      parts.push(span);
      lastIndex = match.index + match[0].length;
    }
    if (parts.length === 0) return;
    parts.push(document.createTextNode(text.slice(lastIndex)));
    const parent = textNode.parentNode;
    const frag = document.createDocumentFragment();
    parts.forEach((p) => frag.appendChild(p));
    parent.replaceChild(frag, textNode);
  });
}

function handleClick(ev) {
  const span = ev.target.closest(".yt-timestamp-jump");
  if (!span) return;
  const seconds = parseInt(span.getAttribute("data-seconds"), 10);
  if (Number.isNaN(seconds)) return;
  const iframe = findFirstYoutubeIframe(span);
  if (iframe) {
    ev.preventDefault();
    setIframeStartTime(iframe, seconds);
  }
}

module.exports = class YoutubeTimestampJumpPlugin extends obsidian.Plugin {
  onload() {
    this.registerDomEvent(document.body, "click", handleClick);
    this.registerMarkdownPostProcessor((el) => processElement(el));
  }
};
