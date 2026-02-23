# Tiered Grow Lights

A RimWorld 1.6 mod that adds five tiers of artificial grow lights modelled on the real-world evolution of horticultural lighting technology.

Each tier provides progressively wider light coverage and better energy efficiency, while generating heat proportional to its inefficiency — early lamps heat grow rooms noticeably, LED tiers barely register. Unlocked through a dedicated five-stage research chain.

**No DLC required. No Harmony patches**

---

## Tiers

| Lamp | Power | Radius | Heat | Efficiency | Glow |
|---|---|---|---|---|---|
| Incandescent Grow Lamp | 1 200 W | 6 | 1.5 /s | 30% | Warm amber |
| Halogen Grow Lamp | 1 800 W | 7 | 1.9 /s | 40% | Warm white |
| Sodium Grow Lamp | 2 600 W | 8 | 2.3 /s | 50% | Deep orange |
| LED Grow Lamp Mk I | 2 200 W | 8 | 0.9 /s | 70% | Cool blue-white |
| LED Grow Lamp Mk I (red) | 2 400 W | 8 | 1.1 /s | 65% | Magenta-red |
| LED Grow Lamp Mk I (blue) | 2 000 W | 8 | 0.7 /s | 75% | Vivid blue |
| Advanced LED Array | 4 000 W | 10 | 0.5 /s | 85% | Bright neutral white |

**Light efficiency** is displayed in the building info card and represents how much of the electrical draw is converted to useful plant-growth light rather than waste heat.

**Heat** (`heatPerSecond`) is calculated as `power × wasteRatio / 560`. The sodium lamp is the hottest lamp in the lineup — a grow room running three of them will need active cooling. A room full of Advanced LED Arrays will barely register on the thermometer.

---

## LED Mk I colour variants

Three flavours of the Mk I unlock together at *LED Agronomy*. The mechanical difference is real and biome-dependent:

| Variant | Trade-off | Best used in |
|---|---|---|
| Balanced | All-rounder | Any biome |
| Red `(620–700 nm)` | More power, more waste heat | **Cold biomes** — the heat does double duty keeping plants warm |
| Blue `(400–500 nm)` | Less power, least heat | **Hot biomes** — keeps grow rooms coolest |

---

## Research chain

All five projects appear in a dedicated **Grow Lighting** research tab.

```
Electricity  (vanilla)
  └─ Electric Agriculture I       400 pt  · Industrial  · any bench
       └─ Electric Agriculture II     600 pt  · Industrial  · any bench
             └─ Industrial Grow Lighting  1000 pt  · Industrial  · any bench
                   └─ LED Agronomy           1600 pt  · Spacer
                        requires: MicroelectronicsBasics + Hi-Tech Research Bench
                        unlocks: all three LED Mk I variants
                          └─ Advanced Photonic Cultivation  2400 pt  · Spacer
                               requires: Hi-Tech Research Bench + Multi-Analyser
```

---

## Breakdown behaviour

Filament and discharge lamps (Incandescent, Halogen, Sodium) include `CompBreakdownable` — they fail randomly and need a pawn to repair them, consistent with the fragility of those technologies. LED tiers use solid-state emitters and never break down.

---

## Compatibility

- **Vanilla:** fully compatible, no vanilla defs modified
- **No DLC dependency**
- **No Harmony**

---

## Installation

### Steam Workshop
*(Not yet published)*

### Manual
1. Clone or download this repository
2. Copy the `SevereGrowLights` folder into your RimWorld `Mods` directory
3. Enable **Tiered Grow Lights** in the mod manager and start a new game or load an existing save

```
RimWorld/Mods/
└── SevereGrowLights/
    ├── About/
    ├── Defs/
    └── Languages/
```

---

## File structure

```
SevereGrowLights/
├── About/
│   └── About.xml
├── Defs/
│   ├── ThingDefs_Buildings/
│   │   └── GrowLights.xml          ← all lamps
│   ├── ResearchProjectDefs/
│   │   └── GrowLightResearch.xml   ← research tab + 5 projects
│   └── StatDefs/
│       └── GrowLightStats.xml      ← SGL_LightEfficiency stat
└── Languages/
    └── English/
        └── Keyed/
            └── GrowLights.xml      ← translator placeholder
```

---

## License

[MIT](LICENSE)
