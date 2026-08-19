import type { APIRoute } from "astro";
import {
  buildMetropolitanPackCsv,
  metropolitanPackDefinitions,
} from "../../../lib/metropolitanPack";

export function getStaticPaths() {
  return metropolitanPackDefinitions.map((pack) => ({
    params: {
      slug: pack.id,
      file: pack.filename.replace(/\.csv$/, ""),
    },
    props: { packId: pack.id, filename: pack.filename },
  }));
}

export const GET: APIRoute = ({ props }) => {
  const { packId, filename } = props as { packId: string; filename: string };
  return new Response(buildMetropolitanPackCsv(packId), {
    status: 200,
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="${filename}"`,
      "Cache-Control": "public, max-age=3600",
    },
  });
};
