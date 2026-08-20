import type { APIRoute } from "astro";
import { buildChirpCsv } from "../../../lib/chirpPack";
import { buildCentreV03Pack, centreV03Filename } from "../../../lib/centrePack";

export const GET: APIRoute = () => {
  const csv = buildChirpCsv(buildCentreV03Pack());
  return new Response(csv, {
    status: 200,
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="${centreV03Filename}"`,
      "Cache-Control": "public, max-age=3600",
    },
  });
};
