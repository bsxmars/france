// Compares a learner's typed answer with the accepted answers of an exercise
// item. Comparison is forgiving about things that are not the point of a
// grammar exercise: case, extra spaces (including the non-breaking spaces of
// French typography before ? ! : ;), curly apostrophes, commas, final
// punctuation and the ligatures œ and æ. Accents are compared strictly: a
// missing accent is a spelling mistake, but nearMiss tells the learner that
// only accents were wrong.

const QUOTES: Record<string, string> = {
  '’': "'", '‘': "'", '`': "'", '´': "'", 'ʼ': "'",
  '“': '"', '”': '"', '«': '"', '»': '"',
  'œ': 'oe', 'æ': 'ae',
  ' ': ' ', ' ': ' ', ' ': ' ',
};
const QUOTES_RE = new RegExp(`[${Object.keys(QUOTES).join('')}]`, 'g');

const ACCENTS: Record<string, string> = {
  à: 'a', â: 'a', ä: 'a',
  é: 'e', è: 'e', ê: 'e', ë: 'e',
  î: 'i', ï: 'i',
  ô: 'o', ö: 'o',
  ù: 'u', û: 'u', ü: 'u',
  ÿ: 'y', ç: 'c',
};
const ACCENTS_RE = new RegExp(`[${Object.keys(ACCENTS).join('')}]`, 'g');
const stripAccents = (s: string) => s.replace(ACCENTS_RE, (c) => ACCENTS[c]!);

const EDGE = /^[".!?;:…\s]+|[".!?;:…\s]+$/g;

/** normalize lowercases s, unifies quotes, spaces and ligatures, glues an
 * elided word to the next one ("l' homme" → "l'homme") and drops commas,
 * surrounding quotes and final punctuation. */
export function normalize(s: string): string {
  s = s.toLowerCase().replace(QUOTES_RE, (c) => QUOTES[c]!);
  s = s.replaceAll(',', ' ');
  s = s.split(/\s+/).filter(Boolean).join(' ');
  s = s.replaceAll("' ", "'");
  return s.replace(EDGE, '');
}

/** text reports whether given matches any of the accepted answers. */
export function text(given: string, answers: string[]): boolean {
  const got = normalize(given);
  return answers.some((a) => normalize(a) === got);
}

/** nearMiss reports whether given matches an accepted answer once accents are
 * ignored, while text rejects it: "ecole" for "école", "a" for "à". */
export function nearMiss(given: string, answers: string[]): boolean {
  if (text(given, answers)) return false;
  const got = stripAccents(normalize(given));
  if (got === '') return false;
  return answers.some((a) => stripAccents(normalize(a)) === got);
}

/** choice reports whether given (an option index) is answer. */
export function choice(given: string, answer: number): boolean {
  const t = given.trim();
  return /^[-+]?\d+$/.test(t) && Number(t) === answer;
}
