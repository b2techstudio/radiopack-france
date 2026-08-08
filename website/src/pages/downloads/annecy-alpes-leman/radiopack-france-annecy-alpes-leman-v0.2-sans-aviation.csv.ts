import type { APIRoute } from "astro";
import { annecyPublicFilename, buildAnnecyCsv } from "../../../lib/annecyPack";

export const prerender = true;

export const GET: APIRoute = () =>
  new Response(buildAnnecyCsv(false), {
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="${annecyPublicFilename(false)}"`,
      "Cache-Control": "public, max-age=3600",
    },
  });
