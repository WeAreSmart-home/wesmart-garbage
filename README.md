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

The card provides a visual schedule editor and shows today's and upcoming collections.

---

## License

MIT
