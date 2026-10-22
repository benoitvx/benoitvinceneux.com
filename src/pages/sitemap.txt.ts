import { getCollection } from 'astro:content';

export async function GET() {
  const projects = await getCollection('projects'); // [] tant que #5 n'a pas créé la collection
  const paths = ['/', '/a-propos', ...projects.map((p) => `/${p.id}`)];
  return new Response(paths.map((p) => `https://benoitvinceneux.com${p}`).join('\n') + '\n');
}
