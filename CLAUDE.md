# SevereGrowLights – Project Reference

## Mod identity
- **PackageId:** `severemod.growlights` | **RimWorld:** 1.6 | **DLC:** none | **C#/Harmony:** none

## Directory map
```
SevereGrowLights/
├── About/About.xml
├── Defs/
│   ├── ThingDefs_Buildings/GrowLights.xml     ← all lamps + SpectrumController + base
│   ├── ResearchProjectDefs/GrowLightResearch.xml  ← 5 research nodes + tab def
│   └── StatDefs/GrowLightStats.xml            ← SGL_LightEfficiency stat
├── Patches/
│   └── HydroponicsBasinPatch.xml              ← adds CompAffectedByFacilities to basin
└── Languages/English/Keyed/GrowLights.xml     ← placeholder
```

## Tier quick-reference  (power 1200 W → 4000 W)
| DefName | Label | R | W | Heat/s | Eff% | Breakdown | Research |
|---|---|---|---|---|---|---|---|
| SGL_IncandLamp | incandescent grow lamp | 6 | 1200 | 1.5 | 30 | yes | SGL_ElectricAgricultureI |
| SGL_HalogenLamp | halogen grow lamp | 7 | 1800 | 1.9 | 40 | yes | SGL_ElectricAgricultureII |
| SGL_SodiumLamp | sodium grow lamp | 8 | 2600 | 2.3 | 50 | yes | SGL_IndustrialGrowLighting |
| SGL_LEDLampMk1 | LED grow lamp Mk I | 8 | 2200 | 0.9 | 70 | no | SGL_LEDAgronomy |
| SGL_LEDLampMk1_Red | LED grow lamp Mk I (red) | 8 | 2400 | 1.1 | 65 | no | SGL_LEDAgronomy |
| SGL_LEDLampMk1_Blue | LED grow lamp Mk I (blue) | 8 | 2000 | 0.7 | 75 | no | SGL_LEDAgronomy |
| SGL_AdvancedLEDArray | advanced LED array | 10 | 4000 | 0.5 | 85 | no | SGL_AdvancedPhotonicCultivation |
| SGL_SpectrumController | spectrum controller | — | 150 | — | — | no | SGL_LEDAgronomy |

## Research chain
```
Electricity (vanilla)
  └─ SGL_ElectricAgricultureI    400  Industrial
       └─ SGL_ElectricAgricultureII   600  Industrial
             └─ SGL_IndustrialGrowLighting  1000  Industrial
                   └─ SGL_LEDAgronomy           1600  Spacer
                        [+ Microelectronics, HiTechResearchBench]
                        → unlocks LED Mk I (all 3 variants) + SpectrumController
                          └─ SGL_AdvancedPhotonicCultivation  2400  Spacer
                               [+ HiTechResearchBench, MultiAnalyzer facility]
```

## Key technical choices
| Topic | Decision |
|---|---|
| ThingClass | `Building_SunLamp` – grow-zone UI overlay + day/night scheduling built-in |
| Schedule | Inherent in `Building_SunLamp`; `CompFlickable` for manual override; full hour control needs C# |
| Heat formula | `heatPerSecond = power × wasteRatio / 560` |
| Breakdown | `CompProperties_Breakdownable` on tiers 1–3 only (filament/discharge) |
| Efficiency stat | `SGL_LightEfficiency` (0.30→0.85), `toStringStyle>PercentZero` |
| LED variants | Red (2400W, 1.1 heat/s, 65%) vs Blue (2000W, 0.7 heat/s, 75%) – biome trade-off via heat |
| Hydroponics | `SGL_SpectrumController` (CompFacility, Fertility +0.40) + PatchOperation on HydroponicsBasin |
| Graphic | All reuse `Things/Building/Misc/SunLamp`; replace `texPath` per-def for custom art |
| Advanced component | `ComponentIndustrialAdv` – verify in 1.6 Core |
| glowColor | ColorInt `(R,G,B,0)` 0–255 |

## Glow colours
| Lamp | glowColor |
|---|---|
| Incandescent | (255,210,100,0) warm amber |
| Halogen | (255,240,180,0) warm white |
| Sodium | (255,140,30,0) deep orange |
| LED balanced | (180,215,255,0) cool blue-white |
| LED red | (200,40,80,0) deep magenta-red |
| LED blue | (80,150,255,0) vivid blue |
| Advanced LED | (210,238,255,0) bright neutral white |

## Common edit tasks
- **Power draw:** `basePowerConsumption` in CompProperties_Power
- **Heat:** `heatPerSecond` + optionally `heatPushMaxTemperature`
- **Radius:** `glowRadius` in CompProperties_Glower
- **Efficiency display:** `SGL_LightEfficiency` in statBases (0.0–1.0)
- **Facility bonus:** `Fertility` offset in SGL_SpectrumController CompProperties_Facility
- **New tier:** copy nearest ThingDef, new defName + matching ResearchProjectDef

## 1.6 verification points
- `Building_SunLamp`, `CompProperties_HeatPusher`, `CompProperties_Breakdownable` names
- `ComponentIndustrialAdv` – advanced component defName
- `HiTechResearchBench`, `MultiAnalyzer` – research building defNames
- `CompProperties_Facility.mustBePlacedAdjacentCardinalToBuildingOfType` – property name
- `Fertility` – stat defName on HydroponicsBasin
