import { readFileSync } from "node:fs";
import { basename, resolve } from "node:path";

export const CHIRP_COLUMNS = [
  "Location", "Name", "Frequency", "Duplex", "Offset", "Tone",
  "rToneFreq", "cToneFreq", "DtcsCode", "DtcsPolarity", "RxDtcsCode",
  "CrossMode", "Mode", "TStep", "Skip", "Power", "Comment",
  "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE",
] as const;

export type Channel = {
  name: string;
  frequency_mhz: number;
  mode: "FM" | "NFM" | "AM";
  step_khz: number;
  comment: string;
  verification?: string;
  skip?: string;
};

type Dataset = { channels: Channel[] };

export type PackSource = {
  path: string;
  start: number;
  block: string;
  group?: string;
  verificationAllowList?: string[];
};

export type PlacedChannel = {
  location: number;
  block: string;
  channel: Channel;
};

export const repositoryRoot = () => {
  const cwd = process.cwd();
  return basename(cwd) === "website" ? resolve(cwd, "..") : cwd;
};

const loadDataset = (relativePath: string): Dataset => {
  const path = resolve(repositoryRoot(), relativePath);
  return JSON.parse(readFileSync(path, "utf-8")) as Dataset;
};

export const validatePlacedChannels = (placed: PlacedChannel[]) => {
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

export const assemblePack = (
  sources: PackSource[],
  disabledGroups: ReadonlySet<string> = new Set<string>(),
): PlacedChannel[] => {
  const placed: PlacedChannel[] = [];

  for (const source of sources) {
    if (source.group && disabledGroups.has(source.group)) continue;

    let channels = loadDataset(source.path).channels;
    if (source.verificationAllowList?.length) {
      const allowed = new Set(source.verificationAllowList);
      channels = channels.filter((channel) => allowed.has(channel.verification ?? ""));
    }

    channels.forEach((channel, index) => {
      placed.push({ location: source.start + index, block: source.block, channel });
    });
  }

  placed.sort((a, b) => a.location - b.location);
  validatePlacedChannels(placed);
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

export const buildChirpCsv = (placed: PlacedChannel[]) => {
  validatePlacedChannels(placed);
  const rows = placed.map(chirpRow);
  return [CHIRP_COLUMNS.join(","), ...rows.map((row) => row.map(csvCell).join(",")), ""].join("\r\n");
};
