
# Example: Integrating NFL Data with Your Fantasy Tool

from core.enhanced_fantasy_tool import EnhancedFantasyTool
from core.nfl_data_integration import NFLDataIntegrator

def enhance_existing_cheatsheet():
    """Enhance your existing fantasy cheatsheet with NFL data"""

    # Initialize enhanced tool
    enhanced_tool = EnhancedFantasyTool()

    # Your existing fantasy projections (load from your current system)
    fantasy_projections = pd.read_csv("data/offense_projections.csv")

    # Enhance with NFL data
    enhanced_projections = enhanced_tool.enhance_projections_with_nfl_data(
        fantasy_projections,
        seasons_to_analyze=[2023, 2024]  # Analyze multiple seasons
    )

    # Generate enhanced Excel file
    enhanced_tool.generate_enhanced_cheatsheet(
        enhanced_projections,
        "enhanced_fantasy_cheatsheet.xlsx"
    )

    print("Enhanced cheatsheet created with NFL data insights!")

if __name__ == "__main__":
    enhance_existing_cheatsheet()
