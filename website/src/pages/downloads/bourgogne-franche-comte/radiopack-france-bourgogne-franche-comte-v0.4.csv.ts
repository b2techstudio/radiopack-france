import type { APIRoute } from "astro";
import { buildBfcV04Pack, bfcV04Filename } from "../../../lib/bfcPack";
import { buildChirpCsv } from "../../../lib/chirpPack";

export const GET: APIRoute = () => {
  const csv = buildChirpCsv(buildBfcV04Pack());
  return new Response(csv, {
    status: 200,
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="${bfcV04Filename}"`,
      "Cache-Control": "public, max-age=3600",
    },
  });
};
