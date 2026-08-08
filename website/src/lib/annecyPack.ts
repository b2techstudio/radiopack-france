import { readFileSync } from "node:fs";
import { basename, resolve } from "node:path";

export const CHIRP_COLUMNS = [
  "Location", "Name", "Frequency", "Duplex", "Offset", "Tone",
  "rToneFreq", "cToneFreq", "DtcsCode", "DtcsPolarity", "RxDtcsCode",
  "CrossMode", "Mode", "TStep", "Skip", "Power", "Comment",
  "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE",
] as const;

type Channel = {
  name: string;
  frequency_mhz: number;
  mode: "FM" | "NFM" | "AM";
  step_khz: number;
  comment: string;
  verification?: string;
  skip?: string;
};

type Dataset = { channels: Channel[] };

export type PlacedChannel = {
  location: number;
  block: string;
  channel: Channel;
};

const repositoryRoot = () => {
  const cwd = process.cwd();
  return basename(cwd) === "website" ? resolve(cwd, "..") : cwd;
};

const load = (relativePath: string): Dataset => {
  const path = resolve(repositoryRoot(), relativePath);
  return JSON.parse(readFileSync(path, "utf-8")) as Dataset;
};

const SOURCES = [
  { path: "data/national/pmr446.json", start: 0, block: "PMR446 national RX", aviation: false },
  { path: "data/national/amateur-listening-rx.json", start: 20, block: "APRS / ISS RX", aviation: false },
  { path: "research/annecy-alpes-leman-v0.2/satellites-fm-inventory.json", start: 26, block: "Satellites FM RX", aviation: false },
  { path: "data/national/amateur-calls-rx.json", start: 30, block: "Canaux d'appel RX", aviation: false },
  { path: "research/annecy-alpes-leman-v0.2/radioamateur-france-inventory.json", start: 40, block: "Radioamateur France RX", aviation: false },
  { path: "research/annecy-alpes-leman-v0.2/radioamateur-switzerland-candidates.json", start: 90, block: "Radioamateur Suisse RX", aviation: false, verifiedOnly: true },
  { path: "research/annecy-alpes-leman-v0.2/aviation-france-airac-08.json", start: 125, block: "Aviation France RX", aviation: true },
  { path: "research/annecy-alpes-leman-v0.2/aviation-switzerland-airac-08.json", start: 155, block: "Aviation Suisse RX", aviation: true },
] as const;

const validate = (placed: PlacedChannel[]) => {
  if (placed.length > 200) throw new Error(`Pack trop grand: ${placed.length}`);

  const locations = new Set<number>();
  const names = new Set<string>();
  const frequencies = new Set<string>();

  for (const item of placed) {
    const { location, channel } = item;
    if (location < 0 || location > 199) throw new Error(`Location invalide: ${location}`);
    if (channel.name.length > 10) throw new Error(`Nom trop long: ${channel.name}`);
    if (!channel.comment) throw new Error(`Commentaire absent: ${channel.name}`);
    if (!Number.isFinite(channel.frequency_mhz) || channel.frequency_mhz <= 0) throw new Error(`Fréquence invalide: ${channel.name}`);
    if (!Number.isFinite(channel.step_khz) || channel.step_khz <= 0) throw new Error(`Pas invalide: ${channel.name}`);

    const frequencyKey = channel.frequency_mhz.toFixed(6);
    if (locations.has(location)) throw new Error(`Location dupliquée: ${location}`);
    if (names.has(channel.name)) throw new Error(`Nom dupliqué: ${channel.name}`);
    if (frequencies.has(frequencyKey)) throw new Error(`Fréquence dupliquée: ${frequencyKey}`);
    locations.add(location);
    names.add(channel.name);
    frequencies.add(frequencyKey);
  }
};

export const getAnnecyPack = (includeAviation = true): PlacedChannel[] => {
  const placed: PlacedChannel[] = [];

  for (const source of SOURCES) {
    if (!includeAviation && source.aviation) continue;

    let channels = load(source.path).channels;
    if ("verifiedOnly" in source && source.verifiedOnly) {
      channels = channels.filter((channel) => channel.verification === "verified_current");
    }

    channels.forEach((channel, index) => {
      placed.push({ location: source.start + index, block: source.block, channel });
    });
  }

  placed.sort((a, b) => a.location - b.location);
  validate(placed);

  const expected = includeAviation ? 65 : 48;
  if (placed.length !== expected) {
    throw new Error(`Nombre de mémoires inattendu: ${placed.length}, attendu ${expected}`);
  }

  return placed;
};

const csvCell = (value: string | number) => {
  const text = String(value);
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
};

const chirpRow = (item: PlacedChannel) => {
  const { location, channel } = item;
  return [
    location,
    channel.name,
    channel.frequency_mhz.toFixed(6),
    "off",
    "0.000000",
    "",
    "88.5",
    "88.5",
    "023",
    "NN",
    "023",
    "Tone->Tone",
    channel.mode,
    channel.step_khz.toFixed(2),
    channel.skip ?? "",
    "",
    channel.comment,
    "",
    "",
    "",
    "",
  ];
};

export const buildAnnecyCsv = (includeAviation = true) => {
  const rows = getAnnecyPack(includeAviation).map(chirpRow);
  return [CHIRP_COLUMNS.join(","), ...rows.map((row) => row.map(csvCell).join(",")), ""].join("\r\n");
};

export const annecyPublicFilename = (includeAviation = true) =>
  includeAviation
    ? "radiopack-france-annecy-alpes-leman-v0.2.csv"
    : "radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv";
