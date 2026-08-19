import type { APIRoute } from "astro";
import { buildBfcV03Pack, bfcV03Filename } from "../../../lib/bfcPack";
import { buildChirpCsv } from "../../../lib/chirpPack";

export const GET: APIRoute = () => {
  const csv = buildChirpCsv(buildBfcV03Pack());
  return new Response(csv, {
    status: 200,
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="${bfcV03Filename}"`,
      "Cache-Control": "public, max-age=3600",
    },
  });
};
