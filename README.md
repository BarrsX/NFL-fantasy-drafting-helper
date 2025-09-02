# Fantasy Draft Cheat Sheet Generator

A comprehensive tool for generating optimized fantasy football draft cheat sheets with advanced analytics, ADP integration, and live draft board functionality.

## 🚀 Quick Start

### One-Command Workflow (Recommended)

``├── 📁 scripts/ # 🐍 Python scripts
│ ├── 📁 core/ # Core functionality
│ │ └── 📄 sleeper_cheatsheet.py
│ ├── 📁 utils/ # Utility scripts
│ │ ├── 📄 add_strikethrough_formatting.py
│ │ └── 📄 ...
│ ├── 📁 run/ # 🚀 Run scripts
│ │ ├── 📄 run_web_dashboard.bat
│ │ └── 📄 ...
│ └── 📁 build/ # Build scripts
│ ├── 📄 generate_cheatsheet.bat
│ └── 📄 ...
│
├── 📁 src/ # 🌐 Web application
│ └── 📁 web/ # Web dashboard
│ ├── 📄 app.py # Flask application
│ ├── 📄 run_dashboard.py # Dashboard runner
│ ├── 📁 templates/ # HTML templates
│ │ └── 📄 dashboard.html # Main dashboard
│ └── 📁 static/ # Static assets
│erate_cheatsheet.bat

````

**What happens automatically:**

- ✅ Generates your dynasty superflex cheat sheet
- ✅ Applies automatic strikethrough formatting
- ✅ Shows draft insights and top priorities
- ✅ Creates a fully formatted Excel file ready for live drafting

**Result:** A complete draft board in `output/dynasty_superflex_cheatsheet.xlsx`

## 🌐 Web Dashboard

### Overview

The Fantasy Drafting Web Dashboard provides a modern, interactive web interface for your draft cheat sheets with the same powerful features as the Excel version.

### Quick Web Start

```batch
# Run the web dashboard
.\scripts\run\run_web_dashboard.bat
````

**Features:**

- ✅ **Interactive Draft Board** - Real-time draft tracking with live updates
- ✅ **Multi-Tab Interface** - Overall rankings + position-specific views
- ✅ **Advanced Search & Filter** - Find players instantly across all data
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Live Drafting** - Mark players as drafted with automatic strikethrough
- ✅ **Color-Coded Tiers** - Visual tier representation with value indicators

**Access:** Navigate to `http://localhost:5000` in your browser

### Web Dashboard Features

#### Core Functionality

- **Overall Rankings** - Complete player rankings with draft priorities
- **Position-Specific Views** - Dedicated tabs for QB, RB, WR, TE
- **Draft Board** - Simplified view optimized for live drafting
- **Real-time Search** - Search players across all tabs instantly

#### Visual Features

- **Tier-Based Coloring** - Different colors for each tier (1-5)
- **Value Indicators** - Highlight steals, values, and reaches
- **Scarcity Indicators** - Mark cliff and drop-off players
- **Position Badges** - Color-coded position indicators
- **Responsive Design** - Works seamlessly on all devices

#### Draft Features

- **Live Draft Tracking** - Mark players as drafted during live drafts
- **Round/Pick Tracking** - Record which round and pick players were drafted
- **Draft Reset** - Reset the entire draft if needed
- **Interactive Drafting** - Click to mark players as drafted

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
- `flask` - Web framework for dashboard
- `flask-cors` - Cross-origin resource sharing for API
- `flask-compress` - Response compression for better performance
- `gunicorn` - Production WSGI server (optional)

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

### Excel Cheat Sheet (Default)

```batch
# Generate cheat sheet with automatic formatting
.\generate_cheatsheet.bat
```

### Web Dashboard

```batch
# Run interactive web dashboard
.\scripts\run\run_web_dashboard.bat
```

**Access:** Open `http://localhost:5000` in your browser

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

### Web Dashboard Features

- ✅ **Interactive Draft Board** - Click-to-draft with live updates
- ✅ **Real-time Search** - Instant player search across all tabs
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Multi-Tab Interface** - Overall + position-specific rankings
- ✅ **Live Draft Tracking** - Track rounds, picks, and drafted players
- ✅ **Visual Tier System** - Color-coded tiers with value indicators

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
├── 📁 src/                        # 🐍 Source code
│   ├── 📁 core/                   # Core functionality
│   │   └── 📄 sleeper_cheatsheet.py
│   ├── 📁 utils/                  # Utility scripts
│   │   ├── 📄 add_strikethrough_formatting.py
│   │   └── 📄 ...
│   └── 📁 web/                    # 🌐 Web dashboard
│       ├── 📄 app.py              # Flask application
│       ├── 📄 run_dashboard.py    # Dashboard runner
│       ├── � templates/          # HTML templates
│       │   └── 📄 dashboard.html  # Main dashboard
│       └── � static/             # Static assets
│
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

#### "Dashboard won't start"

**Solution:**

1. Ensure Flask is installed: `pip install flask flask-cors`
2. Check that all data files exist in the `data/` directory
3. Verify configuration files are present
4. Try running: `python src/web/app.py` directly

#### "No data displayed in dashboard"

**Solution:**

1. Check browser console for JavaScript errors
2. Verify the Flask server is running on port 5000
3. Ensure CSV data files are properly formatted
4. Clear browser cache and refresh

### Getting Help

1. **Check the logs** - The batch file shows detailed error messages
2. **Verify data files** - Ensure CSV files are properly formatted
3. **Test components** - Run individual scripts to isolate issues
4. **Check Excel** - Ensure Excel isn't blocking automation
5. **Web dashboard** - Check browser developer tools for console errors

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

_Last updated: September 1, 2025_
