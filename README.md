# Fantasy Draft Cheat Sheet Generator

A comprehensive tool for generating optimized fantasy football draft cheat sheets with advanced analytics, ADP integration, and live draft board functionality.

## 🚀 Quick Start

### One-Command Workflow (Recommended)

```batch
.\generate_cheatsheet.bat
```

**What happens automatically:**

- ✅ Generates your dynasty superflex cheat sheet
- ✅ Applies automatic strikethrough formatting
- ✅ Shows draft insights and top priorities
- ✅ Creates a fully formatted Excel file ready for live drafting

**Result:** A complete draft board in `output/dynasty_superflex_cheatsheet.xlsx`

## 📋 Prerequisites

### System Requirements

- **Windows 10/11** (required for Excel automation)
- **Python 3.8+**
- **Microsoft Excel** (for formatting features)
- **PowerShell** (included with Windows)

### Required Python Packages

- `pandas` - Data manipulation
- `numpy` - Numerical computations
- `openpyxl` - Excel file handling
- `pywin32` - Windows/Excel integration (optional, for advanced formatting)

## 🛠️ Installation

### 1. Clone or Download

```bash
# Clone the repository
git clone <repository-url>
cd fantasy-drafting

# Or download and extract the ZIP file
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Installation

```batch
.\generate_cheatsheet.bat
```

If successful, you'll see the cheat sheet generation process start.

## 📊 Data Setup

### Required Data Files

Place these CSV files in the `data/` directory:

#### 1. Sleeper ADP (`data/sleeper_adp.csv`)

Download from Sleeper:

1. Go to your league → Draft → Settings
2. Click "Export Draft Results" or "Export ADP"
3. Save as `data/sleeper_adp.csv`

**Required columns:** `player`, `position`, `team`, `adp`

#### 2. Offense Projections (`data/offense_projections.csv`)

Your fantasy projections for QB/RB/WR/TE.

**Required columns:**

- `player_name`, `position`, `team`
- Fantasy points columns (e.g., `passing_yds`, `passing_tds`, `rushing_yds`, etc.)

#### 3. IDP Projections (`data/idp_projections.csv`) - Optional

Projections for DL/LB/DB (for dynasty leagues).

### Sample Data Structure

**ADP CSV:**

```csv
player,position,team,adp
Josh Allen,QB,BUF,1.5
Lamar Jackson,QB,BAL,2.3
```

**Projections CSV:**

```csv
player_name,position,team,passing_yds,passing_tds,rushing_yds,rushing_tds,receiving_yds,receiving_tds
Josh Allen,QB,BUF,4500,35,350,3,0,0
```

## 🎯 Usage

### Basic Usage

```batch
# Generate cheat sheet with automatic formatting
.\generate_cheatsheet.bat
```

### Manual Formatting (If Needed)

```batch
# Apply formatting to existing file
.\apply_formatting.bat

# Test formatting functionality
.\test_formatting.bat
```

### Advanced Usage

```batch
# Run specific components
python scripts\core\sleeper_cheatsheet.py

# List available configurations
python scripts\core\sleeper_cheatsheet.py list all
```

## ⚙️ Configuration

### League Types

The tool supports multiple league configurations:

- **Dynasty Superflex** (default) - Dynasty league with superflex QB
- **Redraft 12-team** - Standard redraft league
- **Superflex 12-team** - Superflex without dynasty features

### Customizing Settings

Edit `configs/config_dynasty.json` to modify:

- **Scoring rules** - Points per yard/TD
- **League settings** - Team count, starters, superflex
- **Tier gaps** - Point differences between tiers
- **Bench factors** - Replacement level calculations

## 🎨 Features

### Core Features

- ✅ **Draft Priority Algorithm** - Advanced scoring system combining VORP, ADP, and position scarcity
- ✅ **ADP Integration** - Robust name matching with fuzzy logic for player identification
- ✅ **Tier Assignment** - Automatic tiering based on configurable point gaps
- ✅ **Position Scarcity** - Dynamic calculations for each position
- ✅ **Value Analysis** - Best value picks based on priority vs. ADP

### Excel Features

- ✅ **Color-Coded Tiers** - Visual tier representation
- ✅ **Auto-Strikethrough** - Type 'X' to cross out drafted players
- ✅ **Live Draft Board** - Real-time draft tracking
- ✅ **Multiple Sheets** - Overall + position-specific views
- ✅ **Conditional Formatting** - Automatic visual updates

### Advanced Features

- ✅ **IDP Support** - Defensive player projections and rankings
- ✅ **Superflex QB** - Enhanced QB evaluation for superflex leagues
- ✅ **Dynasty Mode** - Long-term value calculations
- ✅ **Configurable Scoring** - Custom point systems
- ✅ **Robust Data Matching** - Handles name variations and special characters

## 📁 Project Structure

```
fantasy-drafting/
├── 📄 generate_cheatsheet.bat     # 🚀 ONE-CLICK: Generate + format
├── 📄 apply_formatting.bat        # 🎨 Manual formatting application
├── 📄 test_formatting.bat         # ✅ Test strikethrough functionality
├── 📄 requirements.txt            # 📦 Python dependencies
├── 📄 README.md                   # 📖 This documentation
│
├── 📁 data/                       # 📊 Input data files
│   ├── 📄 sleeper_adp.csv         # Sleeper ADP rankings
│   ├── 📄 offense_projections.csv # QB/RB/WR/TE projections
│   └── 📄 idp_projections.csv     # DL/LB/DB projections
│
├── 📁 configs/                    # ⚙️ Configuration files
│   ├── 📄 config_dynasty.json     # Dynasty league settings
│   ├── 📄 config_redraft.json     # Redraft league settings
│   └── 📄 config_superflex.json   # Superflex settings
│
├── 📁 scripts/                    # 🐍 Python scripts
│   ├── 📁 core/                   # Core functionality
│   │   └── 📄 sleeper_cheatsheet.py
│   ├── 📁 formatting/             # Excel formatting tools
│   │   ├── 📄 setup_excel_formatting.ps1
│   │   ├── 📄 add_strikethrough_formatting.py
│   │   └── 📄 auto_setup_formatting.py
│   └── 📁 utilities/              # Helper scripts
│       ├── 📄 check_adp_status.py
│       ├── 📄 test_normalization.py
│       └── 📄 ...
│
├── 📁 output/                     # 📤 Generated files
│   └── 📄 dynasty_superflex_cheatsheet.xlsx
│
├── 📁 docs/                       # 📚 Documentation
│   ├── 📄 excel_strikethrough_guide.md
│   ├── 📄 PROGRAMMATIC_SOLUTIONS_README.md
│   └── 📄 AUTO_STRIKETHROUGH_README.md
│
└── 📁 tools/                      # 🔧 Additional tools
    ├── 📄 setup_formatting.bat
    └── 📄 setup_strikethrough.bat
```

## 🔧 Troubleshooting

### Common Issues

#### "Configuration file not found"

**Solution:** Ensure you're running from the project root directory.

#### "No ADP CSV found"

**Solution:** Check that `data/sleeper_adp.csv` exists and has the correct format.

#### "Excel formatting failed"

**Solution:**

1. Ensure Microsoft Excel is installed
2. Close any open Excel files
3. Run `.\apply_formatting.bat` manually

#### "Import errors"

**Solution:** Install required packages:

```bash
pip install -r requirements.txt
```

### Getting Help

1. **Check the logs** - The batch file shows detailed error messages
2. **Verify data files** - Ensure CSV files are properly formatted
3. **Test components** - Run individual scripts to isolate issues
4. **Check Excel** - Ensure Excel isn't blocking automation

## 🚀 Advanced Usage

### Custom League Configurations

1. Copy an existing config file
2. Modify settings for your league
3. Update the `CONFIG_FILE` variable in the script

### API Integration

The tool can fetch live ADP data from Sleeper:

```json
{
  "sleeper_api": {
    "use_api": true,
    "league_id": "your-league-id"
  }
}
```

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Organization

- **Core logic** → `scripts/core/`
- **Formatting tools** → `scripts/formatting/`
- **Utilities** → `scripts/utilities/`
- **Documentation** → `docs/`

---

**Happy Drafting!** 🏈✨

_Last updated: August 31, 2025_
