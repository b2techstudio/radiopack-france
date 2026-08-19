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
type AviationMemory = {
  name: string;
  frequency: number;
  area: string;
  service: string;
  icao?: string;
};

export type MetropolitanPackVersion = "v0.1" | "v0.2";

export type MetropolitanPackDefinition = {
  id: string;
  regionSlug: string;
  name: string;
  version: MetropolitanPackVersion;
  memoryCount: number;
  repeaters: Repeater2m[];
  aviation: AviationMemory[];
  includeMarine: boolean;
  filename: string;
};

export const metropolitanSourceNotes = {
  checkedOn: "2026-08-19",
  refBandPlan: "https://www.r-e-f.org/index.php?option=com_content&view=article&id=94&Itemid=173",
  repeaterBook: "https://www.repeaterbook.com/row_repeaters/Display_SS.php?state_id=FR&band=14",
  f5aibRoster: "https://f5aib.net/index.php?option=com_content&view=article&id=20&Itemid=170",
  siaAirac: "https://www.sia.aviation-civile.gouv.fr/produits-numeriques-en-libre-disposition/les-bases-de-donnees-sia/donnees-aeronautiques-xml-airac-08-26.html",
  siaMethodology: "AIRAC 08/26 current-cycle context cross-checked against latest effective public SIA eAIP AD 2.18 pages; no direct XML field extraction is claimed.",
  anfrOpenData: "https://data.anfr.fr/",
} as const;

const v01 = (
  id: string,
  name: string,
  memoryCount: number,
  repeaters: Repeater2m[],
): MetropolitanPackDefinition => ({
  id,
  regionSlug: id,
  name,
  version: "v0.1",
  memoryCount,
  repeaters,
  aviation: [],
  includeMarine: false,
  filename: `radiopack-france-${id}-v0.1.csv`,
});

export const metropolitanV01PackDefinitions: MetropolitanPackDefinition[] = [
  v01("hauts-de-france", "Hauts-de-France", 36, [
    { call: "F1ZKY", site: "Capelle-la-Grande", output: 145.6125 },
    { call: "F1ZFM", site: "Bouvigny-Boyeffles", output: 145.6875 },
    { call: "F5ZTP", site: "Abbeville", output: 145.7125 },
    { call: "F5ZAG", site: "Raismes", output: 145.725 },
    { call: "F1ZTK", site: "Lille", output: 145.7625 },
    { call: "F1ZGY", site: "Valenciennes", output: 145.7875 },
  ]),
  v01("ile-de-france", "Île-de-France", 34, [
    { call: "F5ZNN", site: "Coulommiers", output: 145.65 },
    { call: "F6ZEE", site: "Pontault-Combault", output: 145.7 },
    { call: "F5ZMH", site: "Linas", output: 145.7375 },
    { call: "F5ZEQ", site: "Sartrouville", output: 145.75 },
    { call: "F1ZHK", site: "Nangis", output: 145.7625 },
  ]),
  v01("grand-est", "Grand Est", 36, [
    { call: "F5ZAU", site: "Dabo / Col du Valsberg", output: 145.6125 },
    { call: "F1ZDG", site: "Sondernach / Petit Ballon", output: 145.625 },
    { call: "F1ZAE", site: "Metz", output: 145.675 },
    { call: "F5ZCQ", site: "Wissembourg", output: 145.725 },
    { call: "F1ZPJ", site: "Saint-Avold", output: 145.75 },
    { call: "F1ZAX", site: "Cosnes-et-Romain", output: 145.7625 },
  ]),
  v01("centre-val-de-loire", "Centre-Val de Loire", 32, [
    { call: "F5ZHF", site: "Orléans", output: 145.625 },
    { call: "F5ZDE", site: "Aigurande-sur-Bouzanne", output: 145.6375 },
    { call: "F5ZNX", site: "Chartres", output: 145.7125 },
    { call: "F5ZLP", site: "Mazières-de-Touraine", output: 145.7375 },
  ]),
  v01("pays-de-la-loire", "Pays de la Loire", 30, [
    { call: "F5ZKC", site: "Saint-Nazaire", output: 145.6375 },
    { call: "F1ZSM", site: "Pellouailles-les-Vignes", output: 145.6625 },
    { call: "F6ZCU", site: "Les Herbiers", output: 145.775 },
  ]),
  v01("bourgogne-franche-comte", "Bourgogne-Franche-Comté", 30, [
    { call: "F5ZBP", site: "Salins / Mont Poupet", output: 145.775 },
    { call: "F1ZDK", site: "Montceau", output: 145.75 },
    { call: "F1ZCT", site: "Chitry", output: 145.7875 },
  ]),
  v01("nouvelle-aquitaine", "Nouvelle-Aquitaine", 42, [
    { call: "F5ZQF", site: "Guéret", output: 145.6 },
    { call: "F5ZVE", site: "Sainte-Fortunade", output: 145.6125 },
    { call: "F5ZFX", site: "Domme", output: 145.625 },
    { call: "F5ZGM", site: "Limoges", output: 145.65 },
    { call: "F1ZWT", site: "Périgueux", output: 145.6625 },
    { call: "F1ZCW", site: "Bordeaux", output: 145.725 },
    { call: "F1ZUI", site: "Irouléguy / Mont Jara", output: 145.7375 },
    { call: "F5ZZK", site: "Parthenay", output: 145.7625 },
    { call: "F5ZUL", site: "Labenne", output: 145.775 },
  ]),
  v01("auvergne-rhone-alpes", "Auvergne-Rhône-Alpes", 38, [
    { call: "F1ZBA", site: "Aubenas", output: 145.625 },
    { call: "F1ZCQ", site: "Grenoble", output: 145.65 },
    { call: "F1ZFD", site: "Le Puy-en-Velay", output: 145.6625 },
    { call: "F5ZDK", site: "Aurillac", output: 145.675 },
    { call: "F5ZFH", site: "Lyon", output: 145.6875 },
    { call: "F1ZBS", site: "Clermont-Ferrand", output: 145.7625 },
    { call: "F1ZJV", site: "Viuz-en-Sallaz", output: 145.7875 },
  ]),
  v01("occitanie", "Occitanie", 44, [
    { call: "F1ZBM", site: "Alès", output: 145.6 },
    { call: "F1ZCM", site: "Perpignan", output: 145.6125 },
    { call: "F1ZMQ", site: "Figeac", output: 145.6375 },
    { call: "F5ZTO", site: "Le Carla-Bayle", output: 145.65 },
    { call: "F5ZKT", site: "Germs-sur-l'Oussouet", output: 145.675 },
    { call: "F1ZGU", site: "Sète", output: 145.6875 },
    { call: "F5ZZR", site: "Millau", output: 145.7125 },
    { call: "F5ZCL", site: "Escoussens", output: 145.75 },
    { call: "F1ZED", site: "Montastruc", output: 145.775 },
    { call: "F1ZCZ", site: "Foix", output: 145.7875 },
  ]),
  v01("provence-alpes-cote-d-azur", "Provence-Alpes-Côte d’Azur", 42, [
    { call: "F5ZOO", site: "Sainte-Maxime", output: 145.625 },
    { call: "F1ZVB", site: "Suzette", output: 145.65 },
    { call: "F5ZAY", site: "Nice", output: 145.675 },
    { call: "F1ZHI", site: "Ampus", output: 145.6875 },
    { call: "F1ZVH", site: "Digne", output: 145.7 },
    { call: "F5ZVD", site: "Solliès-Toucas", output: 145.725 },
    { call: "F5ZAX", site: "Nice", output: 145.75 },
    { call: "F5ZTH", site: "Marseille", output: 145.775 },
    { call: "F5ZAI", site: "Briançon", output: 145.7875 },
  ]),
  v01("corse", "Corse", 28, [
    { call: "TK5ZCF", site: "Alata", output: 145.6375 },
    { call: "TK5ZPS", site: "Bastia", output: 145.7375 },
  ]),
];

export const metropolitanPackDefinitions: MetropolitanPackDefinition[] = [
  {
    id: "hauts-de-france",
    regionSlug: "hauts-de-france",
    name: "Hauts-de-France",
    version: "v0.2",
    memoryCount: 144,
    includeMarine: true,
    filename: "radiopack-france-hauts-de-france-v0.2.csv",
    aviation: [
      { name: "AIR-EMERG", frequency: 121.5, area: "France / aviation", service: "EMERGENCY" },
      { name: "LIL-INFO", frequency: 126.475, area: "Lille", service: "FIS", icao: "LFQQ" },
      { name: "LIL-APP1", frequency: 120.275, area: "Lille", service: "APP", icao: "LFQQ" },
      { name: "LIL-APP2", frequency: 134.825, area: "Lille", service: "APP", icao: "LFQQ" },
      { name: "LIL-GND", frequency: 121.65, area: "Lille", service: "GND", icao: "LFQQ" },
      { name: "LIL-TWR", frequency: 118.55, area: "Lille", service: "TWR", icao: "LFQQ" },
      { name: "LIL-ATIS", frequency: 127.075, area: "Lille", service: "ATIS", icao: "LFQQ" },
      { name: "LTQ-GND", frequency: 121.755, area: "Le Touquet", service: "GND", icao: "LFAT" },
      { name: "LTQ-TWR", frequency: 118.45, area: "Le Touquet", service: "TWR", icao: "LFAT" },
      { name: "LTQ-ATIS", frequency: 123.13, area: "Le Touquet", service: "ATIS", icao: "LFAT" },
      { name: "BVS-FIS", frequency: 119.8, area: "Beauvais", service: "FIS", icao: "LFOB" },
      { name: "BVS-APP", frequency: 121.4, area: "Beauvais", service: "APP/TWR", icao: "LFOB" },
      { name: "BVS-AUX", frequency: 123.985, area: "Beauvais", service: "APP/TWR", icao: "LFOB" },
      { name: "BVS-ATIS", frequency: 118.38, area: "Beauvais", service: "ATIS", icao: "LFOB" },
    ],
    repeaters: [
      { call: "F1ZKY", site: "Capelle-la-Grande", output: 145.6125 },
      { call: "F1ZFS", site: "Saint-Gobain", output: 145.675 },
      { call: "F1ZFM", site: "Bouvigny-Boyeffles", output: 145.6875 },
      { call: "F5ZTP", site: "Abbeville", output: 145.7125 },
      { call: "F5ZAG", site: "Raismes", output: 145.725 },
      { call: "F5ZBH", site: "Pozières", output: 145.75 },
      { call: "F1ZTK", site: "Lille", output: 145.7625 },
      { call: "F1ZGY", site: "Valenciennes", output: 145.7875 },
    ],
  },
  {
    id: "ile-de-france",
    regionSlug: "ile-de-france",
    name: "Île-de-France",
    version: "v0.2",
    memoryCount: 58,
    includeMarine: false,
    filename: "radiopack-france-ile-de-france-v0.2.csv",
    aviation: [
      { name: "AIR-EMERG", frequency: 121.5, area: "France / aviation", service: "EMERGENCY" },
      { name: "CDG-APP1", frequency: 118.155, area: "Paris CDG", service: "APP", icao: "LFPG" },
      { name: "CDG-APP2", frequency: 119.855, area: "Paris CDG", service: "APP", icao: "LFPG" },
      { name: "CDG-APP3", frequency: 121.155, area: "Paris CDG", service: "APP", icao: "LFPG" },
      { name: "CDG-APP4", frequency: 124.355, area: "Paris CDG", service: "APP", icao: "LFPG" },
      { name: "ORY-APP1", frequency: 118.855, area: "Paris Orly", service: "APP", icao: "LFPO" },
      { name: "ORY-APP2", frequency: 124.45, area: "Paris Orly", service: "APP", icao: "LFPO" },
      { name: "ORY-APP3", frequency: 127.75, area: "Paris Orly", service: "APP", icao: "LFPO" },
      { name: "ORY-GND1", frequency: 121.555, area: "Paris Orly", service: "GND", icao: "LFPO" },
      { name: "ORY-GND2", frequency: 121.705, area: "Paris Orly", service: "GND", icao: "LFPO" },
      { name: "ORY-TWR", frequency: 118.7, area: "Paris Orly", service: "TWR", icao: "LFPO" },
      { name: "ORY-ATIS", frequency: 126.505, area: "Paris Orly", service: "ATIS", icao: "LFPO" },
      { name: "ORY-INFO", frequency: 131.355, area: "Paris Orly", service: "INFO", icao: "LFPO" },
      { name: "LBG-APP", frequency: 123.835, area: "Le Bourget", service: "APP", icao: "LFPB" },
      { name: "LBG-GND1", frequency: 121.955, area: "Le Bourget", service: "GND", icao: "LFPB" },
      { name: "LBG-GND2", frequency: 121.905, area: "Le Bourget", service: "GND", icao: "LFPB" },
      { name: "LBG-TWR", frequency: 118.93, area: "Le Bourget", service: "TWR", icao: "LFPB" },
      { name: "LBG-ATIS", frequency: 120.005, area: "Le Bourget", service: "ATIS", icao: "LFPB" },
    ],
    repeaters: [
      { call: "F5ZAD", site: "Clamart", output: 145.6 },
      { call: "F5ZNG", site: "Provins", output: 145.625 },
      { call: "F5ZNN", site: "Coulommiers", output: 145.65 },
      { call: "F1ZSY", site: "Paris", output: 145.7 },
      { call: "F1ZUX", site: "Achères", output: 145.7125 },
      { call: "F5ZMH", site: "Linas", output: 145.7375 },
      { call: "F5ZEQ", site: "Sartrouville", output: 145.75 },
      { call: "F1ZHK", site: "Nangis", output: 145.7625 },
    ],
  },
  {
    id: "grand-est",
    regionSlug: "grand-est",
    name: "Grand Est",
    version: "v0.2",
    memoryCount: 59,
    includeMarine: false,
    filename: "radiopack-france-grand-est-v0.2.csv",
    aviation: [
      { name: "AIR-EMERG", frequency: 121.5, area: "France / aviation", service: "EMERGENCY" },
      { name: "SXB-FIS1", frequency: 120.7, area: "Strasbourg", service: "FIS", icao: "LFST" },
      { name: "SXB-FIS2", frequency: 124.75, area: "Strasbourg", service: "FIS", icao: "LFST" },
      { name: "SXB-APP1", frequency: 119.45, area: "Strasbourg", service: "APP", icao: "LFST" },
      { name: "SXB-APP2", frequency: 120.575, area: "Strasbourg", service: "APP", icao: "LFST" },
      { name: "SXB-GND", frequency: 121.805, area: "Strasbourg", service: "GND", icao: "LFST" },
      { name: "SXB-TWR", frequency: 119.25, area: "Strasbourg", service: "TWR", icao: "LFST" },
      { name: "SXB-ATIS", frequency: 126.875, area: "Strasbourg", service: "ATIS", icao: "LFST" },
      { name: "MLH-FIS", frequency: 135.85, area: "Bâle-Mulhouse", service: "FIS", icao: "LFSB" },
      { name: "MLH-APP1", frequency: 119.35, area: "Bâle-Mulhouse", service: "APP", icao: "LFSB" },
      { name: "MLH-APP2", frequency: 124.925, area: "Bâle-Mulhouse", service: "APP", icao: "LFSB" },
      { name: "MLH-GND", frequency: 121.805, area: "Bâle-Mulhouse", service: "GND", icao: "LFSB" },
      { name: "MLH-TWR", frequency: 118.3, area: "Bâle-Mulhouse", service: "TWR", icao: "LFSB" },
      { name: "MLH-ATIS", frequency: 127.88, area: "Bâle-Mulhouse", service: "ATIS", icao: "LFSB" },
      { name: "ETZ-APP", frequency: 119.7, area: "Metz-Nancy", service: "APP", icao: "LFJL" },
      { name: "ETZ-GND", frequency: 121.825, area: "Metz-Nancy", service: "GND", icao: "LFJL" },
      { name: "ETZ-TWR", frequency: 118.775, area: "Metz-Nancy", service: "TWR", icao: "LFJL" },
      { name: "ETZ-ATIS", frequency: 128.725, area: "Metz-Nancy", service: "ATIS", icao: "LFJL" },
      { name: "ENC-INFO", frequency: 119.6, area: "Nancy-Essey", service: "AFIS", icao: "LFSN" },
    ],
    repeaters: [
      { call: "F5ZAU", site: "Dabo / Col du Valsberg", output: 145.6125 },
      { call: "F1ZDG", site: "Sondernach / Petit Ballon", output: 145.625 },
      { call: "F5ZDL", site: "Tilloy", output: 145.6375 },
      { call: "F1ZAE", site: "Metz", output: 145.675 },
      { call: "F5ZEC", site: "Chaumont", output: 145.7 },
      { call: "F5ZCQ", site: "Wissembourg", output: 145.725 },
      { call: "F1ZPJ", site: "Saint-Avold", output: 145.75 },
      { call: "F1ZAX", site: "Cosnes-et-Romain", output: 145.7625 },
    ],
  },
  {
    id: "centre-val-de-loire",
    regionSlug: "centre-val-de-loire",
    name: "Centre-Val de Loire",
    version: "v0.2",
    memoryCount: 42,
    includeMarine: false,
    filename: "radiopack-france-centre-val-de-loire-v0.2.csv",
    aviation: [
      { name: "AIR-EMERG", frequency: 121.5, area: "France / aviation", service: "EMERGENCY" },
      { name: "TUF-TWR", frequency: 124.4, area: "Tours Val de Loire", service: "TWR/AFIS", icao: "LFOT" },
      { name: "CHR-TWR1", frequency: 125.875, area: "Châteauroux", service: "TWR/AFIS", icao: "LFLX" },
      { name: "CHR-TWR2", frequency: 133.805, area: "Châteauroux", service: "TWR/AFIS", icao: "LFLX" },
      { name: "BOU-AFIS", frequency: 119.605, area: "Bourges", service: "AFIS", icao: "LFLD" },
      { name: "BLO-AFIS", frequency: 118.455, area: "Blois-Le Breuil", service: "AFIS", icao: "LFOQ" },
    ],
    repeaters: [
      { call: "F5ZHF", site: "Orléans", output: 145.625 },
      { call: "F5ZDE", site: "Aigurande-sur-Bouzanne", output: 145.6375 },
      { call: "F5ZVB", site: "Amilly", output: 145.675 },
      { call: "F5ZNX", site: "Chartres", output: 145.7125 },
      { call: "F5ZLP", site: "Mazières-de-Touraine", output: 145.7375 },
      { call: "F5ZQY", site: "Blois", output: 145.75 },
    ],
  },
  {
    id: "pays-de-la-loire",
    regionSlug: "pays-de-la-loire",
    name: "Pays de la Loire",
    version: "v0.2",
    memoryCount: 130,
    includeMarine: true,
    filename: "radiopack-france-pays-de-la-loire-v0.2.csv",
    aviation: [
      { name: "AIR-EMERG", frequency: 121.5, area: "France / aviation", service: "EMERGENCY" },
      { name: "NTE-FIS1", frequency: 122.8, area: "Nantes", service: "FIS", icao: "LFRS" },
      { name: "NTE-FIS2", frequency: 130.275, area: "Nantes", service: "FIS", icao: "LFRS" },
      { name: "NTE-APP1", frequency: 120.125, area: "Nantes", service: "APP", icao: "LFRS" },
      { name: "NTE-APP2", frequency: 124.25, area: "Nantes", service: "APP", icao: "LFRS" },
      { name: "NTE-GND", frequency: 121.655, area: "Nantes", service: "GND", icao: "LFRS" },
      { name: "NTE-TWR", frequency: 118.65, area: "Nantes", service: "TWR", icao: "LFRS" },
      { name: "NTE-ATIS", frequency: 126.93, area: "Nantes", service: "ATIS", icao: "LFRS" },
      { name: "ANE-AFIS", frequency: 124.705, area: "Angers", service: "AFIS", icao: "LFJR" },
      { name: "SNR-TWR", frequency: 118.95, area: "Saint-Nazaire", service: "TWR/A-A", icao: "LFRZ" },
    ],
    repeaters: [
      { call: "F5ZKC", site: "Saint-Nazaire", output: 145.6375 },
      { call: "F1ZSM", site: "Pellouailles-les-Vignes", output: 145.6625 },
      { call: "F6ZCU", site: "Les Herbiers", output: 145.775 },
    ],
  },
  {
    id: "bourgogne-franche-comte",
    regionSlug: "bourgogne-franche-comte",
    name: "Bourgogne-Franche-Comté",
    version: "v0.2",
    memoryCount: 37,
    includeMarine: false,
    filename: "radiopack-france-bourgogne-franche-comte-v0.2.csv",
    aviation: [
      { name: "AIR-EMERG", frequency: 121.5, area: "France / aviation", service: "EMERGENCY" },
      { name: "DLE-AFIS", frequency: 130.775, area: "Dole-Tavaux", service: "TWR/AFIS", icao: "LFGJ" },
      { name: "DLE-ATIS", frequency: 121.605, area: "Dole-Tavaux", service: "ATIS", icao: "LFGJ" },
      { name: "DIJ-AFIS", frequency: 118.33, area: "Dijon", service: "AFIS", icao: "LFSD" },
      { name: "NVS-AFIS", frequency: 120.605, area: "Nevers", service: "AFIS", icao: "LFQG" },
      { name: "AUF-AFIS", frequency: 129.805, area: "Auxerre", service: "AFIS", icao: "LFLA" },
      { name: "MONT-AFIS", frequency: 132.03, area: "Montbéliard", service: "AFIS", icao: "LFSM" },
    ],
    repeaters: [
      { call: "F1ZDK", site: "Montceau", output: 145.75 },
      { call: "F5ZBP", site: "Salins / Mont Poupet", output: 145.775 },
      { call: "F1ZCT", site: "Chitry", output: 145.7875 },
    ],
  },
  {
    id: "nouvelle-aquitaine",
    regionSlug: "nouvelle-aquitaine",
    name: "Nouvelle-Aquitaine",
    version: "v0.2",
    memoryCount: 151,
    includeMarine: true,
    filename: "radiopack-france-nouvelle-aquitaine-v0.2.csv",
    aviation: [
      { name: "AIR-EMERG", frequency: 121.5, area: "France / aviation", service: "EMERGENCY" },
      { name: "BOD-FIS", frequency: 120.575, area: "Bordeaux", service: "FIS", icao: "LFBD" },
      { name: "BOD-APP1", frequency: 119.275, area: "Bordeaux", service: "APP", icao: "LFBD" },
      { name: "BOD-APP2", frequency: 129.875, area: "Bordeaux", service: "APP", icao: "LFBD" },
      { name: "BOD-APP3", frequency: 121.2, area: "Bordeaux", service: "APP", icao: "LFBD" },
      { name: "BOD-GND", frequency: 121.9, area: "Bordeaux", service: "GND", icao: "LFBD" },
      { name: "BOD-TWR", frequency: 118.3, area: "Bordeaux", service: "TWR", icao: "LFBD" },
      { name: "BOD-ATIS", frequency: 131.155, area: "Bordeaux", service: "ATIS", icao: "LFBD" },
      { name: "BIQ-FIS", frequency: 119.175, area: "Biarritz", service: "FIS", icao: "LFBZ" },
      { name: "BIQ-APP", frequency: 125.6, area: "Biarritz", service: "APP", icao: "LFBZ" },
      { name: "BIQ-GND", frequency: 121.95, area: "Biarritz", service: "GND", icao: "LFBZ" },
      { name: "BIQ-TWR", frequency: 118.7, area: "Biarritz", service: "TWR", icao: "LFBZ" },
      { name: "BIQ-ATIS", frequency: 128.23, area: "Biarritz", service: "ATIS", icao: "LFBZ" },
    ],
    repeaters: [
      { call: "F5ZQF", site: "Guéret", output: 145.6 },
      { call: "F5ZVE", site: "Sainte-Fortunade", output: 145.6125 },
      { call: "F5ZFX", site: "Domme", output: 145.625 },
      { call: "F5ZGM", site: "Limoges", output: 145.65 },
      { call: "F1ZWT", site: "Périgueux", output: 145.6625 },
      { call: "F5ZCK", site: "Poitiers", output: 145.6875 },
      { call: "F6ZCV", site: "Arette", output: 145.7 },
      { call: "F1ZMB", site: "Saint-Pierre-d’Oléron", output: 145.7125 },
      { call: "F1ZCW", site: "Bordeaux", output: 145.725 },
      { call: "F1ZUI", site: "Irouléguy / Mont Jara", output: 145.7375 },
      { call: "F5ZZK", site: "Parthenay", output: 145.7625 },
      { call: "F5ZUL", site: "Labenne", output: 145.775 },
    ],
  },
  {
    id: "auvergne-rhone-alpes",
    regionSlug: "auvergne-rhone-alpes",
    name: "Auvergne-Rhône-Alpes",
    version: "v0.2",
    memoryCount: 62,
    includeMarine: false,
    filename: "radiopack-france-auvergne-rhone-alpes-v0.2.csv",
    aviation: [
      { name: "AIR-EMERG", frequency: 121.5, area: "France / aviation", service: "EMERGENCY" },
      { name: "LYS-FIS1", frequency: 135.2, area: "Lyon", service: "FIS", icao: "LFLL" },
      { name: "LYS-FIS2", frequency: 135.53, area: "Lyon", service: "FIS", icao: "LFLL" },
      { name: "LYS-APP1", frequency: 120.23, area: "Lyon", service: "APP", icao: "LFLL" },
      { name: "LYS-APP2", frequency: 131.315, area: "Lyon", service: "APP", icao: "LFLL" },
      { name: "LYS-APP3", frequency: 136.075, area: "Lyon", service: "APP", icao: "LFLL" },
      { name: "LYS-DEL", frequency: 121.655, area: "Lyon", service: "DEL", icao: "LFLL" },
      { name: "LYS-GND", frequency: 121.83, area: "Lyon", service: "GND", icao: "LFLL" },
      { name: "CFE-FIS", frequency: 119.375, area: "Clermont-Ferrand", service: "FIS", icao: "LFLC" },
      { name: "CFE-APP", frequency: 120.675, area: "Clermont-Ferrand", service: "APP", icao: "LFLC" },
      { name: "CFE-GND", frequency: 121.95, area: "Clermont-Ferrand", service: "GND", icao: "LFLC" },
      { name: "CFE-TWR", frequency: 118.625, area: "Clermont-Ferrand", service: "TWR", icao: "LFLC" },
      { name: "CFE-ATIS", frequency: 136.405, area: "Clermont-Ferrand", service: "ATIS", icao: "LFLC" },
      { name: "CMF-FIS", frequency: 123.7, area: "Chambéry", service: "FIS/APP", icao: "LFLB" },
      { name: "CMF-APP", frequency: 121.205, area: "Chambéry", service: "APP", icao: "LFLB" },
      { name: "CMF-TWR", frequency: 118.3, area: "Chambéry", service: "TWR", icao: "LFLB" },
      { name: "CMF-ATIS", frequency: 127.1, area: "Chambéry", service: "ATIS", icao: "LFLB" },
      { name: "NCY-AFIS", frequency: 118.2, area: "Annecy", service: "AFIS", icao: "LFLP" },
    ],
    repeaters: [
      { call: "F1ZFG", site: "Lyon", output: 145.6 },
      { call: "F1ZBA", site: "Aubenas", output: 145.625 },
      { call: "F1ZJD", site: "Nurieux", output: 145.6375 },
      { call: "F1ZCQ", site: "Grenoble", output: 145.65 },
      { call: "F1ZFD", site: "Le Puy-en-Velay", output: 145.6625 },
      { call: "F5ZDK", site: "Aurillac", output: 145.675 },
      { call: "F5ZFH", site: "Lyon", output: 145.6875 },
      { call: "F1ZTL", site: "Les Estables", output: 145.7375 },
      { call: "F1ZBS", site: "Clermont-Ferrand", output: 145.7625 },
      { call: "F1ZJV", site: "Viuz-en-Sallaz", output: 145.7875 },
    ],
  },
  {
    id: "occitanie",
    regionSlug: "occitanie",
    name: "Occitanie",
    version: "v0.2",
    memoryCount: 156,
    includeMarine: true,
    filename: "radiopack-france-occitanie-v0.2.csv",
    aviation: [
      { name: "AIR-EMERG", frequency: 121.5, area: "France / aviation", service: "EMERGENCY" },
      { name: "TLS-FIS1", frequency: 121.25, area: "Toulouse", service: "FIS", icao: "LFBO" },
      { name: "TLS-FIS2", frequency: 123.93, area: "Toulouse", service: "FIS", icao: "LFBO" },
      { name: "TLS-APP1", frequency: 121.105, area: "Toulouse", service: "APP", icao: "LFBO" },
      { name: "TLS-APP2", frequency: 120.355, area: "Toulouse", service: "APP", icao: "LFBO" },
      { name: "TLS-GND", frequency: 121.905, area: "Toulouse", service: "GND", icao: "LFBO" },
      { name: "TLS-TWR", frequency: 118.105, area: "Toulouse", service: "TWR", icao: "LFBO" },
      { name: "TLS-ATIS", frequency: 123.13, area: "Toulouse", service: "ATIS", icao: "LFBO" },
      { name: "MPL-FIS1", frequency: 125.9, area: "Montpellier", service: "FIS", icao: "LFMT" },
      { name: "MPL-FIS2", frequency: 134.375, area: "Montpellier", service: "FIS", icao: "LFMT" },
      { name: "MPL-FIS3", frequency: 136.625, area: "Montpellier", service: "FIS", icao: "LFMT" },
      { name: "MPL-APP1", frequency: 120.375, area: "Montpellier", service: "APP", icao: "LFMT" },
      { name: "MPL-APP2", frequency: 127.28, area: "Montpellier", service: "APP", icao: "LFMT" },
      { name: "MPL-APP3", frequency: 130.855, area: "Montpellier", service: "APP", icao: "LFMT" },
      { name: "MPL-GND", frequency: 121.955, area: "Montpellier", service: "GND", icao: "LFMT" },
      { name: "MPL-TWR", frequency: 118.2, area: "Montpellier", service: "TWR", icao: "LFMT" },
      { name: "MPL-ATIS", frequency: 124.13, area: "Montpellier", service: "ATIS", icao: "LFMT" },
      { name: "PGF-GND", frequency: 121.78, area: "Perpignan", service: "GND", icao: "LFMP" },
      { name: "PGF-TWR", frequency: 118.3, area: "Perpignan", service: "TWR", icao: "LFMP" },
      { name: "PGF-ATIS", frequency: 127.88, area: "Perpignan", service: "ATIS", icao: "LFMP" },
    ],
    repeaters: [
      { call: "F1ZBM", site: "Alès", output: 145.6 },
      { call: "F1ZCM", site: "Perpignan", output: 145.6125 },
      { call: "F1ZMQ", site: "Figeac", output: 145.6375 },
      { call: "F5ZTO", site: "Le Carla-Bayle", output: 145.65 },
      { call: "F5ZEZ", site: "Eyne", output: 145.6625 },
      { call: "F5ZKT", site: "Germs-sur-l'Oussouet", output: 145.675 },
      { call: "F1ZGU", site: "Sète", output: 145.6875 },
      { call: "F5ZZR", site: "Millau", output: 145.7125 },
      { call: "F5ZCL", site: "Escoussens", output: 145.75 },
      { call: "F1ZED", site: "Montastruc", output: 145.775 },
      { call: "F1ZCZ", site: "Foix", output: 145.7875 },
    ],
  },
  {
    id: "provence-alpes-cote-d-azur",
    regionSlug: "provence-alpes-cote-d-azur",
    name: "Provence-Alpes-Côte d’Azur",
    version: "v0.2",
    memoryCount: 159,
    includeMarine: true,
    filename: "radiopack-france-provence-alpes-cote-d-azur-v0.2.csv",
    aviation: [
      { name: "AIR-EMERG", frequency: 121.5, area: "France / aviation", service: "EMERGENCY" },
      { name: "NCE-FIS1", frequency: 120.85, area: "Nice", service: "FIS", icao: "LFMN" },
      { name: "NCE-FIS2", frequency: 122.925, area: "Nice", service: "FIS", icao: "LFMN" },
      { name: "NCE-FIS3", frequency: 124.425, area: "Nice", service: "FIS", icao: "LFMN" },
      { name: "NCE-APP1", frequency: 120.16, area: "Nice", service: "APP", icao: "LFMN" },
      { name: "NCE-APP2", frequency: 120.655, area: "Nice", service: "APP", icao: "LFMN" },
      { name: "NCE-APP3", frequency: 124.18, area: "Nice", service: "APP", icao: "LFMN" },
      { name: "NCE-APP4", frequency: 128.205, area: "Nice", service: "APP", icao: "LFMN" },
      { name: "NCE-GND", frequency: 121.705, area: "Nice", service: "GND", icao: "LFMN" },
      { name: "NCE-TWR", frequency: 118.7, area: "Nice", service: "TWR", icao: "LFMN" },
      { name: "NCE-ATIS1", frequency: 129.605, area: "Nice", service: "ATIS", icao: "LFMN" },
      { name: "NCE-ATIS2", frequency: 136.58, area: "Nice", service: "ATIS", icao: "LFMN" },
      { name: "MRS-FIS1", frequency: 124.35, area: "Marseille", service: "FIS", icao: "LFML" },
      { name: "MRS-FIS2", frequency: 126.26, area: "Marseille", service: "FIS", icao: "LFML" },
      { name: "MRS-FIS3", frequency: 131.23, area: "Marseille", service: "FIS", icao: "LFML" },
      { name: "MRS-FIS4", frequency: 132.3, area: "Marseille", service: "FIS", icao: "LFML" },
      { name: "MRS-FIS5", frequency: 132.95, area: "Marseille", service: "FIS", icao: "LFML" },
      { name: "MRS-APP", frequency: 120.205, area: "Marseille", service: "APP", icao: "LFML" },
      { name: "MRS-GND", frequency: 121.905, area: "Marseille", service: "GND", icao: "LFML" },
      { name: "MRS-TWR", frequency: 133.1, area: "Marseille", service: "TWR", icao: "LFML" },
      { name: "MRS-ATIS", frequency: 125.355, area: "Marseille", service: "ATIS", icao: "LFML" },
      { name: "TLN-TWR", frequency: 126.325, area: "Toulon-Hyères", service: "TWR", icao: "LFTH" },
      { name: "AVN-GND", frequency: 121.755, area: "Avignon", service: "GND", icao: "LFMV" },
      { name: "AVN-TWR", frequency: 122.6, area: "Avignon", service: "TWR", icao: "LFMV" },
      { name: "AVN-ATIS", frequency: 120.83, area: "Avignon", service: "ATIS", icao: "LFMV" },
    ],
    repeaters: [
      { call: "F5ZOL", site: "Pierrefeu", output: 145.6 },
      { call: "F5ZOO", site: "Sainte-Maxime", output: 145.625 },
      { call: "F1ZVB", site: "Suzette", output: 145.65 },
      { call: "F5ZAY", site: "Nice", output: 145.675 },
      { call: "F1ZHI", site: "Ampus", output: 145.6875 },
      { call: "F1ZVH", site: "Digne", output: 145.7 },
      { call: "F5ZVD", site: "Solliès-Toucas", output: 145.725 },
      { call: "F5ZAX", site: "Nice", output: 145.75 },
      { call: "F5ZTH", site: "Marseille", output: 145.775 },
      { call: "F5ZAI", site: "Briançon", output: 145.7875 },
    ],
  },
  {
    id: "corse",
    regionSlug: "corse",
    name: "Corse",
    version: "v0.2",
    memoryCount: 137,
    includeMarine: true,
    filename: "radiopack-france-corse-v0.2.csv",
    aviation: [
      { name: "AIR-EMERG", frequency: 121.5, area: "France / aviation", service: "EMERGENCY" },
      { name: "BIA-FIS1", frequency: 124.725, area: "Bastia", service: "FIS", icao: "LFKB" },
      { name: "BIA-FIS2", frequency: 135.135, area: "Bastia", service: "FIS", icao: "LFKB" },
      { name: "BIA-APP1", frequency: 123.825, area: "Bastia", service: "APP", icao: "LFKB" },
      { name: "BIA-APP2", frequency: 127.255, area: "Bastia", service: "APP", icao: "LFKB" },
      { name: "BIA-GND", frequency: 121.83, area: "Bastia", service: "GND", icao: "LFKB" },
      { name: "BIA-TWR", frequency: 118, area: "Bastia", service: "TWR", icao: "LFKB" },
      { name: "BIA-ATIS", frequency: 125.93, area: "Bastia", service: "ATIS", icao: "LFKB" },
      { name: "AJA-FIS", frequency: 119.825, area: "Ajaccio", service: "FIS", icao: "LFKJ" },
      { name: "AJA-APP1", frequency: 121.05, area: "Ajaccio", service: "APP", icao: "LFKJ" },
      { name: "AJA-APP2", frequency: 127.78, area: "Ajaccio", service: "APP", icao: "LFKJ" },
      { name: "AJA-GND", frequency: 121.705, area: "Ajaccio", service: "GND", icao: "LFKJ" },
      { name: "AJA-TWR", frequency: 118.075, area: "Ajaccio", service: "TWR", icao: "LFKJ" },
      { name: "AJA-ATIS", frequency: 126.93, area: "Ajaccio", service: "ATIS", icao: "LFKJ" },
      { name: "FSC-GND", frequency: 121.805, area: "Figari", service: "GND", icao: "LFKF" },
      { name: "FSC-TWR", frequency: 120.3, area: "Figari", service: "TWR", icao: "LFKF" },
      { name: "FSC-ATIS", frequency: 118.73, area: "Figari", service: "ATIS", icao: "LFKF" },
      { name: "CLY-TWR", frequency: 123.2, area: "Calvi", service: "TWR", icao: "LFKC" },
      { name: "CLY-ATIS", frequency: 131.18, area: "Calvi", service: "ATIS", icao: "LFKC" },
    ],
    repeaters: [
      { call: "TK5ZCF", site: "Alata", output: 145.6375 },
      { call: "TK5ZPS", site: "Bastia", output: 145.7375 },
    ],
  },
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

const aviationChannel = (memory: AviationMemory): Channel => ({
  name: memory.name,
  frequency_mhz: memory.frequency,
  mode: "AM",
  step_khz: 8.33,
  verification: "verified_current_airac08",
  comment: `${memory.area} · ${memory.service}${memory.icao ? ` · ${memory.icao}` : ""} · SIA AIRAC 08/26 / eAIP courant · RX seule`,
});

export const getMetropolitanPackDefinition = (
  id: string,
  version: MetropolitanPackVersion = "v0.2",
) => (version === "v0.1" ? metropolitanV01PackDefinitions : metropolitanPackDefinitions)
  .find((pack) => pack.id === id);

const buildBase = () => {
  const placed: PlacedChannel[] = [];
  addBlock(placed, loadChannels("data/national/pmr446.json"), 0, "PMR446");
  addBlock(placed, loadChannels("data/national/amateur-calls-rx.json"), 20, "CALLS");
  addBlock(placed, loadChannels("data/national/amateur-listening-rx.json"), 30, "APRS_ISS");
  return placed;
};

const addRepeaters = (
  placed: PlacedChannel[],
  repeaters: Repeater2m[],
  start: number,
) => {
  let location = start;
  for (const repeater of repeaters) {
    placed.push({ location: location++, block: "REGIONAL_2M", channel: repeaterChannel(repeater, repeater.output, "sortie") });
    placed.push({ location: location++, block: "REGIONAL_2M", channel: repeaterChannel(repeater, Number((repeater.output - 0.6).toFixed(4)), "entrée") });
  }
};

const finish = (placed: PlacedChannel[], definition: MetropolitanPackDefinition) => {
  placed.sort((a, b) => a.location - b.location);
  validatePlacedChannels(placed);
  if (placed.length !== definition.memoryCount) {
    throw new Error(`${definition.name} ${definition.version}: ${placed.length} mémoires générées, ${definition.memoryCount} attendues`);
  }
  return placed;
};

const buildMetropolitanPackV01 = (definition: MetropolitanPackDefinition) => {
  const placed = buildBase();
  addRepeaters(placed, definition.repeaters, 50);
  return finish(placed, definition);
};

const buildMetropolitanPackV02 = (definition: MetropolitanPackDefinition) => {
  const placed = buildBase();
  addBlock(placed, definition.aviation.map(aviationChannel), 40, "AVIATION");
  addRepeaters(placed, definition.repeaters, 70);
  if (definition.includeMarine) {
    addBlock(placed, loadChannels("data/national/marine-vhf-rx.json"), 100, "MARINE");
  }
  return finish(placed, definition);
};

export const buildMetropolitanPack = (
  id: string,
  version: MetropolitanPackVersion = "v0.2",
): PlacedChannel[] => {
  const definition = getMetropolitanPackDefinition(id, version);
  if (!definition) throw new Error(`Pack métropolitain inconnu: ${id} ${version}`);
  return version === "v0.1" ? buildMetropolitanPackV01(definition) : buildMetropolitanPackV02(definition);
};

export const buildMetropolitanPackCsv = (
  id: string,
  version: MetropolitanPackVersion = "v0.2",
) => buildChirpCsv(buildMetropolitanPack(id, version));
