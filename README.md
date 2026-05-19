# WeSmart Garbage

Home Assistant custom integration for managing garbage collection schedules. Stores a weekly schedule in local storage and exposes a sensor that shows what needs to be collected today.

---

## How it works

The integration keeps a persistent schedule (stored in `.storage/wesmart_garbage.storage`) that maps each day of the week to a list of waste types. A sensor reads that schedule reactively: when you update the schedule via service call, the sensor updates immediately without needing a restart or polling.

---

## Requirements

- Home Assistant 2024.1.0 or newer
- No external dependencies

---

## Installation

### Via HACS (recommended)

1. Open HACS → **Integrations**
2. Click the three-dot menu → **Custom repositories**
3. Add `https://github.com/WeAreSmart-home/wesmart-garbage` — category **Integration**
4. Click **Download**
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/wesmart_garbage/` folder into your `/config/custom_components/` directory
2. Restart Home Assistant

---

## Configuration

Add to `configuration.yaml`:

```yaml
wesmart_garbage:
```

No further options are required. Restart HA after adding it.

---

## Sensor

After setup, a single sensor is created:

| Entity | Description |
|--------|-------------|
| `sensor.wesmart_garbage_today` | Comma-separated list of waste types scheduled for today, or `Nothing` |

### Attributes

| Attribute | Description |
|-----------|-------------|
| `schedule` | Full weekly schedule as a JSON object, keyed by ISO weekday (1 = Monday, 7 = Sunday) |

---

## Service

### `wesmart_garbage.update_schedule`

Adds or removes a waste type for a given day (toggle). Calling it twice with the same parameters removes the entry.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `day` | integer | yes | Day of the week (1 = Monday … 7 = Sunday) |
| `waste_type` | string | yes | Name of the waste type (e.g. `Plastica`) |
| `icon` | string | no | MDI icon (e.g. `mdi:recycle`) |

**Example:**

```yaml
service: wesmart_garbage.update_schedule
data:
  day: 1
  waste_type: Plastica
  icon: mdi:recycle
```

---

## Lovelace card

A companion Lovelace card is available as a separate HACS repository:
👉 [wesmart-garbage-card](https://github.com/WeAreSmart-home/wesmart-garbage-card)

The card reads the schedule from `sensor.wesmart_garbage_today` and provides:

- **Phase-aware hero** — today and tomorrow shown side by side; after a configurable hour (default 18:00) today fades to gray and tomorrow becomes the focus
- **Upcoming list** — collections from the day after tomorrow onward, with contextual labels ("Esporre stasera", "Esporre adesso")
- **Built-in editor** — toggle waste types per day directly from the card; changes persist immediately via `wesmart_garbage.update_schedule`

Minimal YAML to add the card:

```yaml
type: custom:wesmart-infinite-garbage-lab-card
```

Full example with all options:

```yaml
type: custom:wesmart-infinite-garbage-lab-card
title: Raccolta Rifiuti
color: "#D97757"
theme: auto
show_weekly_schedule: true
remind_hour: 18   # hour at which evening urgency phase activates (0–23)
```

See the [card repository](https://github.com/WeAreSmart-home/wesmart-garbage-card) for full documentation.

---

## License

MIT
