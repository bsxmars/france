import { describe, expect, it } from 'vitest';
import { choice, nearMiss, text } from './check.ts';

describe('text', () => {
  const cases: [string, string[], boolean][] = [
    ['avais vécu', ['avais vécu'], true],
    ['  Avais   Vécu ', ['avais vécu'], true],
    ['J’ai mangé.', ["J'ai mangé"], true],
    ["l' homme", ["l'homme"], true],
    ['Est-ce que tu viens ?', ['est-ce que tu viens'], true],
    ['Tu viens ?', ['Tu viens ?'], true],
    ["Bien qu'il pleuve nous sortons", ["Bien qu'il pleuve, nous sortons."], true],
    ['un oeuf', ['un œuf'], true],
    ['« Oui »', ['oui'], true],
    ['je ne sais pas', ['je ne sais pas'], true],
    ['je sais pas', ['je ne sais pas'], false],
    ['ecole', ['école'], false],
    ['a', ['à'], false],
    ['mange', ['mangé'], false],
    ['', ['oui'], false],
    ["qu'il vienne", ["qu'il vienne", "qu'il soit venu"], true],
    ["que il vienne", ["qu'il vienne"], false],
    ['Tu viens ?', ['tu viens'], true],
  ];
  for (const [given, answers, want] of cases) {
    it(`${JSON.stringify(given)} vs ${JSON.stringify(answers)}`, () => expect(text(given, answers)).toBe(want));
  }
});

describe('nearMiss', () => {
  const cases: [string, string[], boolean][] = [
    ['ecole', ['école'], true],
    ['Il a ete', ['il a été'], true],
    ['francais', ['français'], true],
    ['école', ['école'], false], // right, not a near miss
    ['maison', ['école'], false],
    ['', ['à'], false],
  ];
  for (const [given, answers, want] of cases) {
    it(`${JSON.stringify(given)} vs ${JSON.stringify(answers)}`, () => expect(nearMiss(given, answers)).toBe(want));
  }
});

it('choice', () => {
  expect(choice('2', 2) && choice(' 0 ', 0)).toBe(true);
  expect(choice('1', 2) || choice('', 0) || choice('x', 0)).toBe(false);
});
