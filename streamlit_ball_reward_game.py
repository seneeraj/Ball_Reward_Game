import streamlit as st
import random

# --- Initialize session state ---
if 'coins' not in st.session_state:
    st.session_state.coins = 0
if 'loan_taken' not in st.session_state:
    st.session_state.loan_taken = False
if 'loan_amount' not in st.session_state:
    st.session_state.loan_amount = 0
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

# --- Game Setup ---
st.title("🎲 Ball Reward Game")

ball_emoji = {"Red": "🔴", "Blue": "🔵"}
source_bag = ['Red'] * 4 + ['Blue'] * 2

st.markdown("### 🎒 Transparent Bag")
st.markdown(" ".join([ball_emoji[color] for color in source_bag]))

# Game selection
if st.session_state.games_to_play == 0:
    num_games = st.selectbox("🎮 How many games do you want to play?", [5, 10, 15, 20])
    entry_fee_per_game = 10
    min_required_coins = num_games * entry_fee_per_game

    if st.button("✅ Confirm & Start"):
        if st.session_state.coins < min_required_coins:
            st.session_state.loan_taken = True
            st.session_state.loan_amount = min_required_coins
            st.session_state.coins += min_required_coins
            st.info(f"💰 You've been lent {min_required_coins} coins to start playing.")
        st.session_state.games_to_play = num_games
        st.success(f"✅ Ready to play {num_games} games!")

# --- Game Play ---
if st.session_state.games_to_play > 0 and st.session_state.games_played < st.session_state.games_to_play:
    st.markdown(f"### Game {st.session_state.games_played + 1} of {st.session_state.games_to_play}")
    
    if st.button("▶️ Play This Round"):
        # Force loan if user has 0 coins
        if st.session_state.coins < 10:
            st.session_state.coins += 10
            st.session_state.loan_taken = True
            st.session_state.loan_amount += 10
            st.warning("💸 You were low on coins. A 10-coin loan was issued for this round.")

        # Deduct entry fee
        st.session_state.coins -= 10
        st.session_state.revenue += 10

        # Draw balls
        drawn = random.sample(source_bag, 4)
        red = drawn.count('Red')
        blue = drawn.count('Blue')

        reward = 0
        if red == 4:
            reward = 50
        elif red in [1, 2, 3]:
            reward = 5

        # Update state
        st.session_state.payout += reward
        st.session_state.coins += reward
        st.session_state.drawn_balls.append(drawn)
        st.session_state.games_played += 1

        # Show result
        st.success(f"🎯 Drawn Balls: {' '.join([ball_emoji[color] for color in drawn])}")
        st.info(f"🏆 Reward: {reward} coins")
        st.write(f"💰 Coins left: {st.session_state.coins}")

# --- Results After All Games ---
if st.session_state.games_played == st.session_state.games_to_play and st.session_state.games_to_play > 0:
    st.markdown("## 🧾 Game Summary")

    for i, balls in enumerate(st.session_state.drawn_balls, 1):
        red = balls.count("Red")
        reward_str = (
            "🏆 50 coins" if red == 4 else
            "🥈 5 coins" if red in [1, 2, 3] else
            "❌ No reward"
        )
        st.write(f"Game {i}: {' '.join([ball_emoji[c] for c in balls])} → {reward_str}")

    st.success(f"💰 Final Coin Balance: {st.session_state.coins}")

    # Optional: Loan repayment summary
    if st.session_state.loan_taken:
        st.warning(f"💳 You were lent a total of {st.session_state.loan_amount} coins.")

    # Reset button
    if st.button("🔁 Reset Game"):
        keys_to_clear = [
            'drawn_balls', 'games_to_play', 'games_played',
            'loan_taken', 'loan_amount', 'revenue', 'payout'
        ]
        for key in keys_to_clear:
            st.session_state[key] = 0 if isinstance(st.session_state[key], int) else False
        st.success("✅ Game has been reset. Start a new round!")

# --- Profit Summary ---
with st.expander("👑 Show Game Owner Profit Summary"):
    st.markdown("### 📊 Profit Summary")
    st.write(f"Total Revenue: {st.session_state.revenue} coins")
    st.write(f"Total Payout: {st.session_state.payout} coins")
    st.write(f"Net Profit: {st.session_state.revenue - st.session_state.payout} coins")
