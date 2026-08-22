import type { APIRoute } from "astro";
import { buildAraV03Pack, araV03Filename } from "../../../lib/araPack";
import { buildChirpCsv } from "../../../lib/chirpPack";

export const GET: APIRoute = () => {
  const csv = buildChirpCsv(buildAraV03Pack());
  return new Response(csv, {
    status: 200,
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="${araV03Filename}"`,
      "Cache-Control": "public, max-age=3600",
    },
  });
};
