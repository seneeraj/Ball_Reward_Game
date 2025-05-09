import streamlit as st
import random

# Initialize session state
if 'coins' not in st.session_state:
    st.session_state.coins = 0
if 'loan_taken' not in st.session_state:
    st.session_state.loan_taken = False
if 'revenue' not in st.session_state:
    st.session_state.revenue = 0
if 'payout' not in st.session_state:
    st.session_state.payout = 0
if 'drawn_balls' not in st.session_state:
    st.session_state.drawn_balls = []
if 'games_to_play' not in st.session_state:
    st.session_state.games_to_play = 0
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0

st.title("🎲 Ball Reward Game")

ball_emoji = {"Red": "🔴", "Blue": "🔵"}
source_bag = ['Red'] * 4 + ['Blue'] * 2
st.markdown("### 🎒 Transparent Bag (Click Play to draw 4 balls)")
st.markdown(" ".join([ball_emoji[color] for color in source_bag]))

# Game setup
if st.session_state.games_to_play == 0:
    num_games = st.selectbox("🎮 How many games do you want to play?", [5, 10, 15, 20])
    entry_fee_total = num_games * 10

    if st.session_state.coins < entry_fee_total:
        if not st.session_state.loan_taken:
            st.session_state.coins += entry_fee_total
            st.session_state.loan_taken = True
            st.info(f"💰 You've been lent {entry_fee_total} coins to start playing.")

    if st.button("Start Game"):
        st.session_state.games_to_play = num_games
        st.session_state.drawn_balls.clear()
        st.session_state.games_played = 0
        st.success(f"🎮 Game started! Click ▶️ Play to begin {num_games} games.")

# Progressive play
if st.session_state.games_to_play > 0 and st.session_state.games_played < st.session_state.games_to_play:
    if st.button("▶️ Play"):
        # Play one game at a time
        drawn = random.sample(source_bag, 4)
        st.session_state.drawn_balls.append(drawn)

        red = drawn.count('Red')
        blue = drawn.count('Blue')
        reward = 0

        if red == 4:
            reward = 50
        elif (red == 3 and blue == 1) or (red == 2 and blue == 2) or (red == 1 and blue == 3):
            reward = 5

        st.session_state.revenue += 10
        st.session_state.payout += reward
        st.session_state.coins += (reward - 10)
        st.session_state.games_played += 1

        st.markdown(f"### 🎯 Game {st.session_state.games_played} Result")
        reward_str = (
            "🏆 50 coins" if red == 4 else
            "🥈 5 coins" if red in [1, 2, 3] else
            "❌ No reward"
        )
        st.write(" ".join([ball_emoji[color] for color in drawn]) + f" → Reward: {reward_str}")
        st.info(f"💰 Coins: {st.session_state.coins} | Games Played: {st.session_state.games_played}/{st.session_state.games_to_play}")

# Game finished
if st.session_state.games_to_play > 0 and st.session_state.games_played == st.session_state.games_to_play:
    st.success("🎉 All games completed!")
    st.write(f"💰 Final Coin Balance: {st.session_state.coins}")

    if st.button("🔁 Reset Game"):
        st.session_state.games_to_play = 0
        st.session_state.games_played = 0
        st.session_state.drawn_balls.clear()

# Owner Summary
with st.expander("👑 Show Game Owner Profit Summary"):
    st.markdown("### 📊 Profit Summary")
    st.write(f"Total Revenue: {st.session_state.revenue} coins")
    st.write(f"Total Payout: {st.session_state.payout} coins")
    st.write(f"Net Profit: {st.session_state.revenue - st.session_state.payout} coins")
