import type { APIRoute } from "astro";

export const prerender = true;

const pages = [
  { path: "/", priority: "1.0", changefreq: "weekly" },
  { path: "/regions", priority: "0.9", changefreq: "weekly" },
  { path: "/regions/normandie", priority: "0.9", changefreq: "weekly" },
  { path: "/regions/annecy-haute-savoie", priority: "0.9", changefreq: "weekly" },
  { path: "/generateur", priority: "0.9", changefreq: "weekly" },
  { path: "/telechargements", priority: "0.9", changefreq: "weekly" },
  { path: "/documentation", priority: "0.7", changefreq: "monthly" },
  { path: "/versions", priority: "0.7", changefreq: "weekly" },
  { path: "/a-propos", priority: "0.5", changefreq: "monthly" },
];

const escapeXML = (value: string) =>
  value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");

export const GET: APIRoute = ({ site }) => {
  const base = site ?? new URL("https://radiopack.b2tech.studio");
  const lastModified = "2026-08-08";

  const urls = pages
    .map(({ path, priority, changefreq }) => {
      const location = new URL(path, base).href;

      return [
        "  <url>",
        `    <loc>${escapeXML(location)}</loc>`,
        `    <lastmod>${lastModified}</lastmod>`,
        `    <changefreq>${changefreq}</changefreq>`,
        `    <priority>${priority}</priority>`,
        "  </url>",
      ].join("\n");
    })
    .join("\n");

  const body = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    urls,
    "</urlset>",
    "",
  ].join("\n");

  return new Response(body, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
    },
  });
};
