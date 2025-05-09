# 🎲 Ball Reward Game (Streamlit App)

This is a visual and interactive ball game where users draw 4 balls from a transparent bag and win coins based on the color combination.

## Game Rules
- Transparent bag contains: 4 Red 🔴 and 2 Blue 🔵 balls
- User chooses how many games to play (multiples of 5)
- Each game costs 10 coins
- Rewards:
  - 4 Red Balls: 50 coins
  - 3 Red + 1 Blue, 2 Red + 2 Blue, or 1 Red + 3 Blue: 5 coins
  - 4 Blue: No reward
- If user has no coins, auto-loan of 50 coins is given

## Owner View
A collapsible summary shows:
- Total Revenue
- Total Payout
- Net Profit

## Run the App
```bash
pip install -r requirements.txt
streamlit run ball_reward_game.py
