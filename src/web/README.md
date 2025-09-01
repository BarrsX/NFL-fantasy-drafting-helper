# Fantasy Drafting Web Dashboard

A modern web-based dashboard for fantasy football drafting with the same features as the Excel spreadsheet.

## Features

### 🎯 Core Features

- **Overall Rankings**: Complete player rankings with draft priorities
- **Position-Specific Views**: Dedicated tabs for QB, RB, WR, TE
- **Draft Board**: Simplified view optimized for live drafting
- **Real-time Search**: Search players across all tabs
- **Interactive Drafting**: Mark players as drafted with strikethrough

### 🎨 Visual Features

- **Tier-Based Coloring**: Different colors for each tier (1-5)
- **Value Indicators**: Highlight steals, values, and reaches
- **Scarcity Indicators**: Mark cliff and drop-off players
- **Position Badges**: Color-coded position indicators
- **Responsive Design**: Works on desktop and mobile devices

### 📊 Draft Features

- **Live Draft Tracking**: Mark players as drafted during live drafts
- **Round/Pick Tracking**: Record which round and pick players were drafted
- **Draft Reset**: Reset the entire draft if needed
- **Strikethrough**: Visually mark drafted players

## Installation

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Dashboard**:

   ```bash
   cd web_dashboard
   python run_dashboard.py
   ```

3. **Open in Browser**:
   Navigate to `http://localhost:5000`

## Usage

### Navigation

- Use the tabs at the top to switch between different views
- **Overall**: Complete rankings with all metrics
- **QB/RB/WR/TE**: Position-specific rankings
- **Draft Board**: Simplified view for live drafting

### Drafting Players

1. Enter the current round and pick number in the draft controls
2. Click the checkbox next to a player's name to mark them as drafted
3. The player will be crossed out and the round counter will advance
4. Use the search box to quickly find players

### Search & Filter

- Use the search box in each tab to filter players by name
- Search works across all columns (name, team, position, etc.)

### Color Coding

- **Tier Colors**: Green (Tier 1), Blue (Tier 2), Yellow (Tier 3), Red (Tier 4), Purple (Tier 5)
- **Value Colors**: Dark green (STEAL), Light green (VALUE), Red (REACH)
- **Scarcity**: Red border (CLIFF), Orange border (DROP)

## Configuration

The dashboard uses the same configuration files as the Excel output:

- `configs/config_redraft.json` - Main configuration
- Data files in the `data/` directory

## API Endpoints

- `GET /api/overall` - Overall player rankings
- `GET /api/position/<QB|RB|WR|TE>` - Position-specific rankings
- `GET /api/draft_board` - Draft board data
- `POST /api/update_drafted` - Update drafted status

## Troubleshooting

### Common Issues

1. **"Import could not be resolved" errors**:

   - Install dependencies: `pip install -r requirements.txt`

2. **Dashboard won't start**:

   - Check that all data files exist in the `data/` directory
   - Verify configuration file paths are correct

3. **No data displayed**:

   - Check browser console for JavaScript errors
   - Verify the Flask server is running on port 5000

4. **Styling issues**:
   - Clear browser cache
   - Check that Bootstrap CDN is accessible

### Data Requirements

The dashboard requires the same data files as the Excel output:

- `data/sleeper_adp.csv` - ADP data
- `data/offense_projections.csv` - Projection data
- `data/idp_projections.csv` - IDP data (optional)

## Development

### Project Structure

```
web_dashboard/
├── app.py                 # Main Flask application
├── run_dashboard.py       # Run script with dependency management
├── templates/
│   └── dashboard.html     # Main dashboard template
└── static/               # Static files (CSS, JS, images)
```

### Adding New Features

1. Update the Flask routes in `app.py`
2. Modify the HTML template in `templates/dashboard.html`
3. Add CSS styles or JavaScript functions as needed

## License

This project is part of the Fantasy Drafting Helper toolset.
