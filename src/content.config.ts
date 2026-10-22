import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const image = z.object({ src: z.string(), srcset: z.string() });

export const collections = {
  projects: defineCollection({
    loader: glob({ pattern: '*.md', base: './src/content/projects' }),
    schema: z.object({
      title: z.string(),
      order: z.number().int(),
      description: z.string().min(1),
      role: z.string().optional(),
      client: z.string().optional(),
      date: z.string().optional(),
      website: z.string().optional(),
      textposition: z.string().optional(),
      cover: image,
      images: z.array(image.extend({ width: z.number(), height: z.number() })),
    }),
  }),
};
