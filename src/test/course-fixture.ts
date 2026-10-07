// A tiny course for component tests, standing in for `virtual:course`.
import { compile } from '../../build/compile.ts';
import { load } from '../../build/content.ts';
import { mapFS } from '../../build/fs.ts';

export const compiled = compile(
  load(
    mapFS({
      'm/module.yaml': 'title: M\nlevel: b1\n',
      'm/l/lesson.md': '---\ntitle: L\n---\nTheory.\n\n## Практика\n\n```exercise gap1\n```\n\n```exercise ord1\n```\n\n```exercise w1\n```\n',
      'm/l/gap1/exercise.yaml':
        'title: G\ntype: gap\nhints: [Think]\nitems:\n  - q: Nous ___ au cinéma.\n    answers: [sommes allés]\n    explain: "**être**"\n  - q: Je ___ au foot.\n    answers: [jouais]\n',
      'm/l/ord1/exercise.yaml': 'title: O\ntype: order\nitems:\n  - q: Собери\n    answers: ["Je suis à la gare."]\n',
      'm/l/w1/exercise.yaml':
        'title: W\ntype: writing\nprompt: Écris.\nwords: [4, 20]\nchecklist: [one, two]\nmodel_answer: Texte modèle.\n',
      'm/l2/lesson.md': '---\ntitle: L2\n---\nNext.\n',
      'cards/m.yaml': '- {id: c1, lesson: m/l, q: "Q?", a: "**A**"}\n',
    }),
  ),
);

export default compiled.index;
export const loadLesson = async (id: string) => compiled.lessons.get(id) ?? null;
export const loadCards = async () => compiled.cards;
