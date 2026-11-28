const max = Number.MAX_SAFE_INTEGER;
export const integerRangeMessage = `Use a whole number between -${max} and ${max}.`;

export function unsafeInteger(value) {
  return Number.isInteger(value) && !Number.isSafeInteger(value);
}

export function compactProjectInput(text) {
  JSON.parse(text);
  return text.replace(/"(?:[^"\\]|\\[\s\S])*"|\s+/g, match => match.startsWith('"') ? match : '');
}

const jsonToken = /"(?:[^"\\]|\\[\s\S])*"|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/g;

export function parseProjectOutput(text) {
  let hasLargeInteger = false;
  // Preserve digits that could not survive conversion to a JavaScript Number.
  // Quoted strings are matched as a unit so their contents are left alone.
  const displayText = text.replace(jsonToken, token => {
    if (!/^-?\d+$/.test(token)) return token;
    if (Number.isSafeInteger(Number(token))) return token;
    hasLargeInteger = true;
    return JSON.stringify(token);
  });
  const value = JSON.parse(displayText);
  return { value, json: hasLargeInteger ? text.trim() : JSON.stringify(value, null, 2) };
}
