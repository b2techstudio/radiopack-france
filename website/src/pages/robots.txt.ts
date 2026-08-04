import type { APIRoute } from "astro";

export const prerender = true;

export const GET: APIRoute = ({ site }) => {
  const base = site ?? new URL("https://radiopack.b2tech.studio");
  const sitemapURL = new URL("/sitemap.xml", base);

  const body = [
    "User-agent: *",
    "Allow: /",
    "",
    `Sitemap: ${sitemapURL.href}`,
    "",
  ].join("\n");

  return new Response(body, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
    },
  });
};
