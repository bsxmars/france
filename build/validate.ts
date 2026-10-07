// npm run validate: loads the whole course and renders all of its markdown.
import { compile } from './compile.ts';
import { load } from './content.ts';
import { dirFS } from './fs.ts';

const dir = process.argv[2] ?? 'content';
try {
  const course = load(dirFS(dir));
  const { index, lessons, cards } = compile(course);
  const exercises = [...lessons.values()].reduce((n, l) => n + l.exercises.length, 0);
  console.log(
    `ok: ${index.modules.length} modules, ${lessons.size} lessons, ${exercises} exercises, ${cards.length} cards`,
  );
} catch (e) {
  console.error((e as Error).message);
  process.exit(1);
}
