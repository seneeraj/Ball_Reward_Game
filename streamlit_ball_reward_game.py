import streamlit as st
import random

# Initialize session state variables if not present
if 'coins' not in st.session_state:
    st.session_state.coins = 60
if 'loan_taken' not in st.session_state:
    st.session_state.loan_taken = False
if 'loan_amount' not in st.session_state:
    st.session_state.loan_amount = 0
if 'revenue' not in st.session_state:
    st.session_state.revenue = 0
if 'payout' not in st.session_state:
    st.session_state.payout = 0
if 'games_to_play' not in st.session_state:
    st.session_state.games_to_play = 0
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0
if 'drawn_balls' not in st.session_state:
    st.session_state.drawn_balls = []

# Set up UI elements
st.title("🎲 Ball Reward Game")

ball_emoji = {"Red": "🔴", "Blue": "🔵"}
source_bag = ['Red'] * 4 + ['Blue'] * 2
st.markdown("### 🎒 Transparent Bag (Click Play to draw 4 balls)")
st.markdown(" ".join([ball_emoji[color] for color in source_bag]))

# Select number of games to play
num_games = st.selectbox("🎮 How many games do you want to play?", [5, 10, 15, 20])
entry_fee_per_game = 10
min_required_coins = num_games * entry_fee_per_game

# Initialize games_to_play if not set
if st.session_state.games_to_play == 0:
    st.session_state.games_to_play = num_games

# Provide loan if coins are insufficient
if st.session_state.coins < min_required_coins:
    if not st.session_state.loan_taken:
        st.session_state.coins += min_required_coins
        st.session_state.loan_taken = True
        st.info(f"💰 You've been lent {min_required_coins} coins to start playing.")

# Reset button logic
if st.button("🔁 Reset Game"):
    st.session_state.drawn_balls = []
    st.session_state.games_to_play = num_games  # Re-initialize the number of games
    st.session_state.games_played = 0
    st.session_state.loan_taken = False
    st.session_state.loan_amount = 0
    st.session_state.revenue = 0
    st.session_state.payout = 0
    st.success("✅ Game has been reset. Start a new round!")

# Game logic when Play button is clicked
if st.button("▶️ Play"):
    # Debugging: print session state variables
    st.write(f"Debugging: games_played = {st.session_state.games_played}, games_to_play = {st.session_state.games_to_play}")

    if st.session_state.games_played < st.session_state.games_to_play:
        # Ensure user has enough coins, otherwise lend them more
        if st.session_state.coins < entry_fee_per_game:
            if not st.session_state.loan_taken:
                st.session_state.coins += entry_fee_per_game
                st.session_state.loan_taken = True
                st.session_state.loan_amount += entry_fee_per_game
                st.info(f"💰 Loan granted: {entry_fee_per_game} coins to continue playing.")
        
        # Draw one game's result
        drawn = random.sample(source_bag, 4)
        st.session_state.drawn_balls.append(drawn)

        red = drawn.count('Red')
        blue = drawn.count('Blue')
        reward = 50 if red == 4 else 5 if red in [1, 2, 3] else 0

        # Update stats
        st.session_state.revenue += entry_fee_per_game
        st.session_state.payout += reward
        st.session_state.coins += reward - entry_fee_per_game
        st.session_state.games_played += 1

        # Show this game's result immediately
        st.markdown(f"### 🎯 Game {st.session_state.games_played} Result")
        st.write(" ".join([ball_emoji[color] for color in drawn]))
        st.write(f"🎁 Reward: {'🏆 50 coins' if reward == 50 else '🥈 5 coins' if reward == 5 else '❌ No reward'}")
        st.success(f"💰 Coins: {st.session_state.coins}")
    else:
        st.warning("🎮 You've already played all your games. Click Reset to start over.")

# Show Game Owner Profit Summary
with st.expander("👑 Show Game Owner Profit Summary"):
    st.markdown("### 📊 Profit Summary")
    st.write(f"Total Revenue: {st.session_state.revenue} coins")
    st.write(f"Total Payout: {st.session_state.payout} coins")
    st.write(f"Net Profit: {st.session_state.revenue - st.session_state.payout} coins")
