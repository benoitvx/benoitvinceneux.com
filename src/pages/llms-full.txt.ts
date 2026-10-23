import { getCollection } from 'astro:content';
import llms from '../../public/llms.txt?raw';
import about from '../content/a-propos.md?raw';

const SITE = 'https://benoitvinceneux.com';

export async function GET() {
  const projects = (await getCollection('projects')).sort((a, b) => a.data.order - b.data.order);
  const pages = [
    { title: 'À propos', slug: 'a-propos', body: about },
    ...projects.map((p) => ({ title: p.data.title, slug: p.id, body: p.body ?? '' })),
  ];
  // Le résumé vient de public/llms.txt : une seule source pour les deux fichiers.
  const summary = llms.match(/^> .*$/m)![0];
  const head = `# Benoit Vinceneux\n\n${summary}\n\nSite : ${SITE}\nEmail : benoitvinceneux@gmail.com\nLinkedIn : https://www.linkedin.com/in/benoitvinceneux/\nGitHub : https://github.com/benoitvx\n\n---`;
  // Retire les blocs HTML bruts (ex. l'iframe de sigfox.md) : une balise en début de ligne jusqu'à sa fermeture en fin de ligne.
  const sections = pages.map((p) => `## ${p.title}\n\nURL : ${SITE}/${p.slug}\n\n${p.body.replace(/^<(\w+)[\s\S]*?<\/\1>$/gm, '').trim()}`);
  return new Response([head, ...sections].join('\n\n') + '\n');
}
