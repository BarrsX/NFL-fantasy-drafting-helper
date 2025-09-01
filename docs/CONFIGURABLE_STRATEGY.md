# Configurable Draft Strategy System

## 🎯 **Problem Solved**

**Before:** Hardcoded player names made the app unusable across seasons
**After:** Statistical thresholds and configurable strategy make it evergreen

## 🔧 **How It Works Now**

### **1. Statistical-Based Round Bonuses**

Instead of hardcoded names like "jefferson", "chase", etc., the system now uses:

- **VORP thresholds** (Value Over Replacement Player)
- **Overall rank thresholds** (top X players overall)
- **Position rank thresholds** (top X at position)
- **Flexible criteria combinations**

### **2. Default Strategy (Built-in)**

```python
# Example: Rounds 1-2 bonus criteria
"rounds_1_2": {
    "bonus": 50,
    "criteria": {
        "WR": {"min_vorp": 50, "max_rank": 5},  # Top 5 WRs with 50+ VORP
        "QB": {"min_vorp": 80, "max_rank": 3}   # Top 3 QBs with 80+ VORP
    }
}
```

### **3. Custom Strategy Files (Optional)**

Create `draft_strategy.json` to customize for your league or season:

```json
{
  "my_2025_strategy": {
    "round_bonuses": {
      "rounds_1_2": {
        "bonus": 60,
        "criteria": {
          "QB": { "min_vorp": 70, "max_rank": 4 },
          "WR": { "min_vorp": 45, "max_rank": 6 }
        }
      }
    }
  }
}
```

## 📊 **Available Criteria Options**

| Criteria       | Description           | Example             |
| -------------- | --------------------- | ------------------- |
| `min_vorp`     | Minimum VORP score    | `"min_vorp": 50`    |
| `max_vorp`     | Maximum VORP score    | `"max_vorp": 100`   |
| `min_rank`     | Minimum overall rank  | `"min_rank": 1`     |
| `max_rank`     | Maximum overall rank  | `"max_rank": 10`    |
| `min_pos_rank` | Minimum position rank | `"min_pos_rank": 1` |
| `max_pos_rank` | Maximum position rank | `"max_pos_rank": 5` |

## 🚀 **Usage Examples**

### **Basic Usage (Default Strategy)**

```bash
python sleeper_cheatsheet.py
```

### **With Custom Strategy File**

```python
# Modify the main function call to include strategy
main(CONFIG_FILE, CONFIG_PROFILE, "draft_strategy.json", "draft_strategy_2025")
```

### **Create Your Own Strategy**

1. **Copy the template:** Start with `draft_strategy.json`
2. **Modify thresholds:** Adjust VORP and rank thresholds
3. **Add/remove positions:** Include positions you care about
4. **Test and refine:** Run the script and see the results

## 🎯 **Strategy Examples**

### **Aggressive (High Risk/Reward)**

```json
"aggressive_2025": {
  "round_bonuses": {
    "rounds_1_2": {
      "bonus": 70,
      "criteria": {
        "QB": {"min_vorp": 90},  # Only elite QBs
        "RB": {"min_vorp": 80, "max_rank": 2}  # Only top 2 RBs
      }
    }
  }
}
```

### **Conservative (High Floor)**

```json
"conservative_2025": {
  "round_bonuses": {
    "rounds_1_2": {
      "bonus": 30,
      "criteria": {
        "WR": {"min_vorp": 30, "max_rank": 12},  # Broader WR1 range
        "RB": {"min_vorp": 40, "max_rank": 8}
      }
    }
  }
}
```

### **IDP-Focused**

```json
"idp_heavy_2025": {
  "round_bonuses": {
    "rounds_4_5": {
      "bonus": 50,  # Higher bonus for IDP
      "criteria": {
        "DL": {"min_vorp": 10, "max_pos_rank": 12},
        "LB": {"min_vorp": 5, "max_pos_rank": 15}
      }
    }
  }
}
```

## ✅ **Benefits Achieved**

### **🔄 Reusability**

- **Works for any season** - no hardcoded names
- **Works for any league** - customize thresholds
- **Works for any format** - dynasty, redraft, superflex, etc.

### **🛠️ Maintainability**

- **No code changes needed** for new seasons
- **Easy strategy tweaking** via config files
- **Clear separation** of logic vs. data

### **📈 Flexibility**

- **Multiple strategies** can be saved and compared
- **A/B testing** different approaches
- **League-specific customization** for different rules

### **🎯 Accuracy**

- **Data-driven decisions** instead of name recognition
- **Adapts automatically** to projection changes
- **Consistent criteria** applied fairly to all players

## 🔮 **Future-Proofing**

This system will work for:

- **2025, 2026, 2027...** - Any future season
- **Rookie classes** - Automatically evaluates new players
- **Injury replacements** - Adapts when players rise/fall
- **Different sites** - Works with any projection source
- **Rule changes** - Easy to adjust strategy configs

---

_No more hardcoded player names. No more season-specific updates. Just pure, statistical draft strategy that works forever._ 🏆
