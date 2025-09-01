# Fantasy Football Cheat Sheet Generator

A flexible fantasy football cheat sheet generator that works with Sleeper ADP data and projection files. Now supports multiple league configurations through separate JSON files.

## Quick Start

```bash
# Use default configuration
python sleeper_cheatsheet.py

# Use a specific configuration
python sleeper_cheatsheet.py -c config_redraft.json -p redraft_12team

# List available configurations
python sleeper_cheatsheet.py --list-configs
```

## Configuration Files

The script now supports multiple league configurations through JSON files:

### Available Configuration Files

1. **`config.json`** - Main configuration file with your current IDP dynasty league settings
2. **`config_redraft.json`** - 12-team redraft league settings (no IDP)
3. **`config_dynasty.json`** - 10-team superflex dynasty settings (half-PPR, no IDP)

### Creating New Configurations

To create a new league configuration:

1. Copy an existing config file (e.g., `config.json`)
2. Rename it (e.g., `config_my_league.json`)
3. Edit the settings inside:

```json
{
  "my_league_name": {
    "paths": {
      "output_xlsx": "my_league_cheatsheet.xlsx"
    },
    "league": {
      "num_teams": 10,
      "superflex": true,
      "use_idp": false
    },
    "scoring": {
      "offense": {
        "rec": 0.5
      }
    }
  }
}
```

4. Run with: `python sleeper_cheatsheet.py -c config_my_league.json -p my_league_name`

## Configuration Structure

Each configuration contains these sections:

### Paths

- `adp_csv`: Sleeper ADP export file
- `offense_csv`: Offensive projections file
- `idp_csv`: IDP projections file (optional)
- `output_xlsx`: Output Excel file name

### League Settings

- `num_teams`: Number of teams in league
- `superflex`: Enable superflex QB scoring
- `use_idp`: Include IDP positions
- `starters`: Starting roster requirements per position
- `bench_factor`: Bench depth factor for VORP calculations

### Scoring

- `offense`: All offensive scoring settings
- `idp`: All IDP scoring settings (if enabled)

### Tiers

- `tier_gap_points`: Point drops that create new tiers per position

## Usage Examples

```bash
# Your current IDP dynasty league (default)
python sleeper_cheatsheet.py

# 12-team redraft league (no IDP, different scoring)
python sleeper_cheatsheet.py -c config_redraft.json -p redraft_12team

# 10-team superflex dynasty (half-PPR)
python sleeper_cheatsheet.py -c config_dynasty.json -p superflex_dynasty

# See what configurations are available
python sleeper_cheatsheet.py --list-configs -c config_redraft.json
```

## Command Line Options

- `--config, -c`: Specify configuration file (default: config.json)
- `--profile, -p`: Specify configuration profile name (default: default)
- `--list-configs, -l`: List available configurations in a file
- `--help, -h`: Show help message

## File Structure

```
fantasy drafting/
├── sleeper_cheatsheet.py          # Main script
├── config.json                    # Default config (your IDP dynasty)
├── config_redraft.json            # Redraft league configs
├── config_dynasty.json            # Dynasty league configs
├── sleeper_adp.csv               # Input: ADP data
├── offense_projections.csv       # Input: Offensive projections
├── idp_projections.csv           # Input: IDP projections (optional)
├── fantasy_cheatsheet.xlsx       # Output: Default league
├── redraft_12team_cheatsheet.xlsx # Output: Redraft league
└── dynasty_superflex_cheatsheet.xlsx # Output: Dynasty league
```

## Tips

- Each configuration generates its own Excel file
- Edit JSON files to fine-tune scoring for each league
- Use different configurations for different draft strategies
- The script automatically detects projection vs ranking data format
