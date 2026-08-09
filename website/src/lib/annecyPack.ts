import {
  assemblePack,
  buildChirpCsv,
  CHIRP_COLUMNS,
  type PackSource,
  type PlacedChannel,
} from "./chirpPack";

export { CHIRP_COLUMNS };
export type { PlacedChannel };

const SOURCES: PackSource[] = [
  { path: "data/national/pmr446.json", start: 0, block: "PMR446 national RX" },
  { path: "data/national/amateur-listening-rx.json", start: 20, block: "APRS / ISS RX" },
  { path: "research/annecy-alpes-leman-v0.2/satellites-fm-inventory.json", start: 26, block: "Satellites FM RX" },
  { path: "data/national/amateur-calls-rx.json", start: 30, block: "Canaux d'appel RX" },
  { path: "research/annecy-alpes-leman-v0.2/radioamateur-france-inventory.json", start: 40, block: "Radioamateur France RX" },
  {
    path: "research/annecy-alpes-leman-v0.2/radioamateur-switzerland-candidates.json",
    start: 90,
    block: "Radioamateur Suisse RX",
    verificationAllowList: ["verified_current"],
  },
  {
    path: "research/annecy-alpes-leman-v0.2/aviation-france-airac-08.json",
    start: 125,
    block: "Aviation France RX",
    group: "aviation",
  },
  {
    path: "research/annecy-alpes-leman-v0.2/aviation-switzerland-airac-08.json",
    start: 155,
    block: "Aviation Suisse RX",
    group: "aviation",
  },
];

export const getAnnecyPack = (includeAviation = true): PlacedChannel[] => {
  const disabledGroups = includeAviation ? new Set<string>() : new Set(["aviation"]);
  const placed = assemblePack(SOURCES, disabledGroups);

  const expected = includeAviation ? 65 : 48;
  if (placed.length !== expected) {
    throw new Error(`Nombre de mémoires inattendu: ${placed.length}, attendu ${expected}`);
  }

  return placed;
};

export const buildAnnecyCsv = (includeAviation = true) =>
  buildChirpCsv(getAnnecyPack(includeAviation));

export const annecyPublicFilename = (includeAviation = true) =>
  includeAviation
    ? "radiopack-france-annecy-alpes-leman-v0.2.csv"
    : "radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv";
