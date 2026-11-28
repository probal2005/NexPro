const limit = 12000;
const marker = '#tool=';

export function shareUrl(source, modules) {
  const bytes = new TextEncoder().encode(JSON.stringify({ source, modules }));
  if (bytes.length > limit) throw new Error('This code and its modules are too large for a share link.');
  const encoded = btoa(String.fromCharCode(...bytes))
    .replaceAll('+', '-').replaceAll('/', '_').replace(/=+$/, '');
  const url = new URL(location.href);
  url.hash = marker + encoded;
  return url.href;
}

export function sharedTool() {
  if (!location.hash.startsWith(marker)) return;
  const encoded = location.hash.slice(marker.length);
  if (encoded.length > limit * 4 / 3 || !/^[A-Za-z0-9_-]+$/.test(encoded)) throw invalidLink();
  try {
    const bytes = Uint8Array.from(atob(encoded.replaceAll('-', '+').replaceAll('_', '/')), c => c.charCodeAt(0));
    const { source, modules } = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes));
    if (typeof source !== 'string' || !modules || typeof modules !== 'object' || Array.isArray(modules)) {
      throw invalidLink();
    }
    for (const [name, value] of Object.entries(modules)) {
      if (!name.endsWith('.pa') || name === 'playground.pa' || typeof value !== 'string') throw invalidLink();
    }
    return { source, modules };
  } catch {
    throw invalidLink();
  }
}

function invalidLink() {
  return new Error('This tool link is invalid or incomplete.');
}
