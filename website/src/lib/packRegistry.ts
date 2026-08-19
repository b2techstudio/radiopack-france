export type PublicPackVariant = {
  id: string;
  label: string;
  memoryCount: number;
  filename: string;
  downloadUrl: string;
  aviationIncluded?: boolean;
};

export type PublicPack = {
  id: string;
  regionSlug: string;
  name: string;
  version: string;
  status: string;
  description: string;
  defaultVariant: string;
  aviationToggle?: {
    includedVariant: string;
    excludedVariant: string;
    memoryCount: number;
  };
  notamCheck: boolean;
  variants: PublicPackVariant[];
};

const legacyPublicPacks: PublicPack[] = [
  {
    id: "annecy-alpes-leman",
    regionSlug: "annecy-haute-savoie",
    name: "Annecy–Alpes–Léman",
    version: "v0.4",
    status: "Disponible",
    description: "Pack Alpes du Nord / bassin lémanique v0.4 avec 77 mémoires RX, dont F1ZTH 50 MHz, et variante sans aviation.",
    defaultVariant: "full",
    aviationToggle: { includedVariant: "full", excludedVariant: "no-aviation", memoryCount: 17 },
    notamCheck: true,
    variants: [
      {
        id: "full",
        label: "Version complète",
        memoryCount: 77,
        filename: "radiopack-france-annecy-alpes-leman-v0.4.csv",
        downloadUrl: "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4.csv",
        aviationIncluded: true,
      },
      {
        id: "no-aviation",
        label: "Sans aviation",
        memoryCount: 60,
        filename: "radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv",
        downloadUrl: "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv",
        aviationIncluded: false,
      },
    ],
  },
  {
    id: "bretagne",
    regionSlug: "bretagne",
    name: "Bretagne",
    version: "v0.2",
    status: "Disponible",
    description: "Pack régional Bretagne v0.2 de 151 mémoires RX, dont 16 mémoires aviation AIRAC 08/26.",
    defaultVariant: "standard",
    notamCheck: false,
    variants: [
      {
        id: "standard",
        label: "Pack complet",
        memoryCount: 151,
        filename: "radiopack-france-bretagne-v0.2.csv",
        downloadUrl: "/downloads/bretagne/radiopack-france-bretagne-v0.2.csv",
        aviationIncluded: true,
      },
    ],
  },
  {
    id: "normandie",
    regionSlug: "normandie",
    name: "Normandie",
    version: "v0.4",
    status: "Disponible",
    description: "Pack régional Normandie v0.4 de 142 mémoires RX, publié en réception seule.",
    defaultVariant: "standard",
    notamCheck: false,
    variants: [
      {
        id: "standard",
        label: "Pack complet",
        memoryCount: 142,
        filename: "radiopack-france-normandie-v0.4.csv",
        downloadUrl: "/downloads/normandie/radiopack-france-normandie-v0.4.csv",
      },
    ],
  },
];

const metropolitanMetadata = [
  { id: "hauts-de-france", name: "Hauts-de-France", memoryCount: 144, marine: true, aviation: 14, version: "v0.2" },
  { id: "ile-de-france", name: "Île-de-France", memoryCount: 58, marine: false, aviation: 18, version: "v0.2" },
  { id: "grand-est", name: "Grand Est", memoryCount: 59, marine: false, aviation: 19, version: "v0.2" },
  { id: "centre-val-de-loire", name: "Centre-Val de Loire", memoryCount: 42, marine: false, aviation: 6, version: "v0.2" },
  { id: "pays-de-la-loire", name: "Pays de la Loire", memoryCount: 130, marine: true, aviation: 10, version: "v0.2" },
  { id: "bourgogne-franche-comte", name: "Bourgogne-Franche-Comté", memoryCount: 54, marine: false, aviation: 14, version: "v0.3" },
  { id: "nouvelle-aquitaine", name: "Nouvelle-Aquitaine", memoryCount: 151, marine: true, aviation: 13, version: "v0.2" },
  { id: "auvergne-rhone-alpes", name: "Auvergne-Rhône-Alpes", memoryCount: 62, marine: false, aviation: 18, version: "v0.2" },
  { id: "occitanie", name: "Occitanie", memoryCount: 156, marine: true, aviation: 20, version: "v0.2" },
  { id: "provence-alpes-cote-d-azur", name: "Provence-Alpes-Côte d’Azur", memoryCount: 159, marine: true, aviation: 25, version: "v0.2" },
  { id: "corse", name: "Corse", memoryCount: 137, marine: true, aviation: 19, version: "v0.2" },
] as const;

const metropolitanPublicPacks: PublicPack[] = metropolitanMetadata.map((item) => {
  const filename = `radiopack-france-${item.id}-${item.version}.csv`;
  const radioScope = item.id === "bourgogne-franche-comte"
    ? "relais FM 2 m/70 cm et transpondeurs crossband paired RX"
    : "relais FM 2 m paired RX";
  const scope = [
    "PMR446",
    "appels",
    "APRS/ISS",
    `${item.aviation} mémoires aviation SIA`,
    radioScope,
    ...(item.marine ? ["module VHF marine"] : []),
  ].join(", ");
  return {
    id: item.id,
    regionSlug: item.id,
    name: item.name,
    version: item.version,
    status: "Disponible",
    description: `Pack régional enrichi ${item.version} de ${item.memoryCount} mémoires RX : ${scope}.`,
    defaultVariant: "standard",
    notamCheck: item.aviation > 0,
    variants: [
      {
        id: "standard",
        label: `Pack enrichi ${item.version}`,
        memoryCount: item.memoryCount,
        filename,
        downloadUrl: `/downloads/${item.id}/${filename}`,
        aviationIncluded: true,
      },
    ],
  };
});

export const publicPacks: PublicPack[] = [
  legacyPublicPacks[0],
  legacyPublicPacks[2],
  legacyPublicPacks[1],
  ...metropolitanPublicPacks,
];

export const defaultPublicPackId = "annecy-alpes-leman";

export const getPublicPack = (packId: string) => publicPacks.find((pack) => pack.id === packId);
export const getPublicVariant = (pack: PublicPack, variantId: string) => pack.variants.find((variant) => variant.id === variantId);
