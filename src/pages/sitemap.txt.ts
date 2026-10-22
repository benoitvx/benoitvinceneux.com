import { getCollection } from 'astro:content';

export async function GET() {
  const projects = (await getCollection('projects')).sort((a, b) => a.data.order - b.data.order);
  const paths = ['/', '/a-propos', ...projects.map((p) => `/${p.id}`)];
  return new Response(paths.map((p) => `https://benoitvinceneux.com${p}`).join('\n') + '\n');
}
