import { buildMetropolitanPack } from "./metropolitanPack";
import { assemblePack, validatePlacedChannels, type PlacedChannel } from "./chirpPack";

export const araV03Version = "v0.3";
export const araV03MemoryCount = 71;
export const araV03Filename = "radiopack-france-auvergne-rhone-alpes-v0.3.csv";

export const buildAraV03Pack = (): PlacedChannel[] => {
  const base = buildMetropolitanPack("auvergne-rhone-alpes", "v0.2");
  const inland = assemblePack([
    {
      path: "data/regional/auvergne-rhone-alpes-inland-vhf-rx.json",
      start: 120,
      block: "INLAND_VHF_V03",
    },
  ]);
  const placed = [...base, ...inland].sort((a, b) => a.location - b.location);
  validatePlacedChannels(placed);
  if (placed.length !== araV03MemoryCount) {
    throw new Error(`ARA ${araV03Version}: ${placed.length} memories, expected ${araV03MemoryCount}`);
  }
  return placed;
};
