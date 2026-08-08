import type { APIRoute } from "astro";
import { annecyPublicFilename, buildAnnecyCsv } from "../../../lib/annecyPack";

export const prerender = true;

export const GET: APIRoute = () =>
  new Response(buildAnnecyCsv(true), {
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="${annecyPublicFilename(true)}"`,
      "Cache-Control": "public, max-age=3600",
    },
  });
