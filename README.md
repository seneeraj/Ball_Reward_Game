# 🎲 Ball Reward Game (Streamlit App)

This is a fun and interactive Streamlit-based web application where users can play a ball drawing game and earn virtual coins based on the colors drawn.

## 💡 Game Rules

- The player draws 4 balls (either Red or Blue) in each game.
- Entry fee per game: 10 coins.
- Rewards:
  - 4 Red balls → 50 coins
  - 3 Red + 1 Blue → 5 coins
  - 2 Red + 2 Blue → 5 coins
  - 1 Red + 3 Blue → 5 coins
  - 4 Blue balls → No reward
- If user lacks coins, they are lent minimum required coins (deducted later from rewards).

## 🚀 How to Run

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run streamlit_ball_reward_game.py
```

## 📊 Owner Summary

After each play session, a detailed owner summary is displayed:
- Total Revenue
- Total Payout
- Net Profit

Enjoy the game!

## 🛠️ Built With

- Python
- Streamlit
