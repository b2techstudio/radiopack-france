import type { APIRoute } from "astro";
import {
  buildMetropolitanPackCsv,
  metropolitanPackDefinitions,
  metropolitanV01PackDefinitions,
  type MetropolitanPackVersion,
} from "../../../lib/metropolitanPack";

export function getStaticPaths() {
  const current = metropolitanPackDefinitions.map((pack) => ({
    params: { slug: pack.id, file: pack.filename.replace(/\.csv$/, "") },
    props: { packId: pack.id, filename: pack.filename, version: pack.version },
  }));
  const historical = metropolitanV01PackDefinitions.map((pack) => ({
    params: { slug: pack.id, file: pack.filename.replace(/\.csv$/, "") },
    props: { packId: pack.id, filename: pack.filename, version: pack.version },
  }));
  return [...current, ...historical];
}

export const GET: APIRoute = ({ props }) => {
  const { packId, filename, version } = props as {
    packId: string;
    filename: string;
    version: MetropolitanPackVersion;
  };
  return new Response(buildMetropolitanPackCsv(packId, version), {
    status: 200,
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="${filename}"`,
      "Cache-Control": "public, max-age=3600",
    },
  });
};
