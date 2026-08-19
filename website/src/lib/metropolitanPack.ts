import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import {
  buildChirpCsv,
  repositoryRoot,
  validatePlacedChannels,
  type Channel,
  type PlacedChannel,
} from "./chirpPack";

type Repeater2m = { call: string; site: string; output: number };

export type MetropolitanPackDefinition = {
  id: string;
  regionSlug: string;
  name: string;
  version: "v0.1";
  memoryCount: number;
  repeaters: Repeater2m[];
  filename: string;
};

export const metropolitanSourceNotes = {
  checkedOn: "2026-08-19",
  refBandPlan: "https://www.r-e-f.org/index.php?option=com_content&view=article&id=94&Itemid=173",
  repeaterBook: "https://www.repeaterbook.com/row_repeaters/Display_SS.php?state_id=FR&band=14",
  f5aibRoster: "https://f5aib.net/index.php?option=com_content&view=article&id=20&Itemid=170",
  anfrOpenData: "https://data.anfr.fr/",
} as const;

export const metropolitanPackDefinitions: MetropolitanPackDefinition[] = [
  {
    id: "hauts-de-france",
    regionSlug: "hauts-de-france",
    name: "Hauts-de-France",
    version: "v0.1",
    memoryCount: 36,
    repeaters: [
      { call: "F1ZKY", site: "Capelle-la-Grande", output: 145.6125 },
      { call: "F1ZFM", site: "Bouvigny-Boyeffles", output: 145.6875 },
      { call: "F5ZTP", site: "Abbeville", output: 145.7125 },
      { call: "F5ZAG", site: "Raismes", output: 145.7250 },
      { call: "F1ZTK", site: "Lille", output: 145.7625 },
      { call: "F1ZGY", site: "Valenciennes", output: 145.7875 }
    ],
    filename: "radiopack-france-hauts-de-france-v0.1.csv",
  },
  {
    id: "ile-de-france",
    regionSlug: "ile-de-france",
    name: "Île-de-France",
    version: "v0.1",
    memoryCount: 34,
    repeaters: [
      { call: "F5ZNN", site: "Coulommiers", output: 145.6500 },
      { call: "F6ZEE", site: "Pontault-Combault", output: 145.7000 },
      { call: "F5ZMH", site: "Linas", output: 145.7375 },
      { call: "F5ZEQ", site: "Sartrouville", output: 145.7500 },
      { call: "F1ZHK", site: "Nangis", output: 145.7625 }
    ],
    filename: "radiopack-france-ile-de-france-v0.1.csv",
  },
  {
    id: "grand-est",
    regionSlug: "grand-est",
    name: "Grand Est",
    version: "v0.1",
    memoryCount: 36,
    repeaters: [
      { call: "F5ZAU", site: "Dabo / Col du Valsberg", output: 145.6125 },
      { call: "F1ZDG", site: "Sondernach / Petit Ballon", output: 145.6250 },
      { call: "F1ZAE", site: "Metz", output: 145.6750 },
      { call: "F5ZCQ", site: "Wissembourg", output: 145.7250 },
      { call: "F1ZPJ", site: "Saint-Avold", output: 145.7500 },
      { call: "F1ZAX", site: "Cosnes-et-Romain", output: 145.7625 }
    ],
    filename: "radiopack-france-grand-est-v0.1.csv",
  },
  {
    id: "centre-val-de-loire",
    regionSlug: "centre-val-de-loire",
    name: "Centre-Val de Loire",
    version: "v0.1",
    memoryCount: 32,
    repeaters: [
      { call: "F5ZHF", site: "Orléans", output: 145.6250 },
      { call: "F5ZDE", site: "Aigurande-sur-Bouzanne", output: 145.6375 },
      { call: "F5ZNX", site: "Chartres", output: 145.7125 },
      { call: "F5ZLP", site: "Mazières-de-Touraine", output: 145.7375 }
    ],
    filename: "radiopack-france-centre-val-de-loire-v0.1.csv",
  },
  {
    id: "pays-de-la-loire",
    regionSlug: "pays-de-la-loire",
    name: "Pays de la Loire",
    version: "v0.1",
    memoryCount: 30,
    repeaters: [
      { call: "F5ZKC", site: "Saint-Nazaire", output: 145.6375 },
      { call: "F1ZSM", site: "Pellouailles-les-Vignes", output: 145.6625 },
      { call: "F6ZCU", site: "Les Herbiers", output: 145.7750 }
    ],
    filename: "radiopack-france-pays-de-la-loire-v0.1.csv",
  },
  {
    id: "bourgogne-franche-comte",
    regionSlug: "bourgogne-franche-comte",
    name: "Bourgogne-Franche-Comté",
    version: "v0.1",
    memoryCount: 30,
    repeaters: [
      { call: "F5ZBP", site: "Salins / Mont Poupet", output: 145.7750 },
      { call: "F1ZDK", site: "Montceau", output: 145.7500 },
      { call: "F1ZCT", site: "Chitry", output: 145.7875 }
    ],
    filename: "radiopack-france-bourgogne-franche-comte-v0.1.csv",
  },
  {
    id: "nouvelle-aquitaine",
    regionSlug: "nouvelle-aquitaine",
    name: "Nouvelle-Aquitaine",
    version: "v0.1",
    memoryCount: 42,
    repeaters: [
      { call: "F5ZQF", site: "Guéret", output: 145.6000 },
      { call: "F5ZVE", site: "Sainte-Fortunade", output: 145.6125 },
      { call: "F5ZFX", site: "Domme", output: 145.6250 },
      { call: "F5ZGM", site: "Limoges", output: 145.6500 },
      { call: "F1ZWT", site: "Périgueux", output: 145.6625 },
      { call: "F1ZCW", site: "Bordeaux", output: 145.7250 },
      { call: "F1ZUI", site: "Irouléguy / Mont Jara", output: 145.7375 },
      { call: "F5ZZK", site: "Parthenay", output: 145.7625 },
      { call: "F5ZUL", site: "Labenne", output: 145.7750 }
    ],
    filename: "radiopack-france-nouvelle-aquitaine-v0.1.csv",
  },
  {
    id: "auvergne-rhone-alpes",
    regionSlug: "auvergne-rhone-alpes",
    name: "Auvergne-Rhône-Alpes",
    version: "v0.1",
    memoryCount: 38,
    repeaters: [
      { call: "F1ZBA", site: "Aubenas", output: 145.6250 },
      { call: "F1ZCQ", site: "Grenoble", output: 145.6500 },
      { call: "F1ZFD", site: "Le Puy-en-Velay", output: 145.6625 },
      { call: "F5ZDK", site: "Aurillac", output: 145.6750 },
      { call: "F5ZFH", site: "Lyon", output: 145.6875 },
      { call: "F1ZBS", site: "Clermont-Ferrand", output: 145.7625 },
      { call: "F1ZJV", site: "Viuz-en-Sallaz", output: 145.7875 }
    ],
    filename: "radiopack-france-auvergne-rhone-alpes-v0.1.csv",
  },
  {
    id: "occitanie",
    regionSlug: "occitanie",
    name: "Occitanie",
    version: "v0.1",
    memoryCount: 44,
    repeaters: [
      { call: "F1ZBM", site: "Alès", output: 145.6000 },
      { call: "F1ZCM", site: "Perpignan", output: 145.6125 },
      { call: "F1ZMQ", site: "Figeac", output: 145.6375 },
      { call: "F5ZTO", site: "Le Carla-Bayle", output: 145.6500 },
      { call: "F5ZKT", site: "Germs-sur-l'Oussouet", output: 145.6750 },
      { call: "F1ZGU", site: "Sète", output: 145.6875 },
      { call: "F5ZZR", site: "Millau", output: 145.7125 },
      { call: "F5ZCL", site: "Escoussens", output: 145.7500 },
      { call: "F1ZED", site: "Montastruc", output: 145.7750 },
      { call: "F1ZCZ", site: "Foix", output: 145.7875 }
    ],
    filename: "radiopack-france-occitanie-v0.1.csv",
  },
  {
    id: "provence-alpes-cote-d-azur",
    regionSlug: "provence-alpes-cote-d-azur",
    name: "Provence-Alpes-Côte d’Azur",
    version: "v0.1",
    memoryCount: 42,
    repeaters: [
      { call: "F5ZOO", site: "Sainte-Maxime", output: 145.6250 },
      { call: "F1ZVB", site: "Suzette", output: 145.6500 },
      { call: "F5ZAY", site: "Nice", output: 145.6750 },
      { call: "F1ZHI", site: "Ampus", output: 145.6875 },
      { call: "F1ZVH", site: "Digne", output: 145.7000 },
      { call: "F5ZVD", site: "Solliès-Toucas", output: 145.7250 },
      { call: "F5ZAX", site: "Nice", output: 145.7500 },
      { call: "F5ZTH", site: "Marseille", output: 145.7750 },
      { call: "F5ZAI", site: "Briançon", output: 145.7875 }
    ],
    filename: "radiopack-france-provence-alpes-cote-d-azur-v0.1.csv",
  },
  {
    id: "corse",
    regionSlug: "corse",
    name: "Corse",
    version: "v0.1",
    memoryCount: 28,
    repeaters: [
      { call: "TK5ZCF", site: "Alata", output: 145.6375 },
      { call: "TK5ZPS", site: "Bastia", output: 145.7375 }
    ],
    filename: "radiopack-france-corse-v0.1.csv",
  }
];

type Dataset = { channels: Channel[] };

const loadChannels = (relativePath: string): Channel[] => {
  const path = resolve(repositoryRoot(), relativePath);
  return (JSON.parse(readFileSync(path, "utf-8")) as Dataset).channels;
};

const addBlock = (
  placed: PlacedChannel[],
  channels: Channel[],
  start: number,
  block: string,
) => {
  channels.forEach((channel, index) => placed.push({ location: start + index, block, channel }));
};

const repeaterChannel = (
  repeater: Repeater2m,
  frequency: number,
  side: "sortie" | "entrée",
): Channel => ({
  name: `${repeater.call}-${side === "sortie" ? "O" : "I"}`,
  frequency_mhz: frequency,
  mode: "FM",
  step_khz: 12.5,
  verification: "verified_current",
  comment: `${repeater.call} · ${repeater.site} · ${side} RX · recoupé REF/F5AIB + RepeaterBook le 2026-08-19`,
});

export const getMetropolitanPackDefinition = (id: string) =>
  metropolitanPackDefinitions.find((pack) => pack.id === id);

export const buildMetropolitanPack = (id: string): PlacedChannel[] => {
  const definition = getMetropolitanPackDefinition(id);
  if (!definition) throw new Error(`Pack métropolitain inconnu: ${id}`);

  const placed: PlacedChannel[] = [];
  addBlock(placed, loadChannels("data/national/pmr446.json"), 0, "PMR446");
  addBlock(placed, loadChannels("data/national/amateur-calls-rx.json"), 20, "CALLS");
  addBlock(placed, loadChannels("data/national/amateur-listening-rx.json"), 30, "APRS_ISS");

  let location = 50;
  for (const repeater of definition.repeaters) {
    placed.push({
      location: location++,
      block: "REGIONAL_2M",
      channel: repeaterChannel(repeater, repeater.output, "sortie"),
    });
    placed.push({
      location: location++,
      block: "REGIONAL_2M",
      channel: repeaterChannel(repeater, Number((repeater.output - 0.6).toFixed(4)), "entrée"),
    });
  }

  placed.sort((a, b) => a.location - b.location);
  validatePlacedChannels(placed);

  if (placed.length !== definition.memoryCount) {
    throw new Error(`${definition.name}: ${placed.length} mémoires générées, ${definition.memoryCount} attendues`);
  }

  return placed;
};

export const buildMetropolitanPackCsv = (id: string) =>
  buildChirpCsv(buildMetropolitanPack(id));
