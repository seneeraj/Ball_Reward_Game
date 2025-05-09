import streamlit as st
import pandas as pd
import random
import time  # To simulate real-time results

# ---------- CSV File Handling ----------
CSV_FILE = "user_data.csv"

# Load user data from CSV, create if missing
try:
    df = pd.read_csv(CSV_FILE, index_col="username")
except FileNotFoundError:
    initial_data = {'username': ['user1', 'user2'], 'coins': [100, 100]}
    df = pd.DataFrame(initial_data).set_index("username")
    df.to_csv(CSV_FILE)

# ---------- Session State Initialization ----------
if 'owner_profit' not in st.session_state:
    st.session_state.owner_profit = 0
if 'games_to_play' not in st.session_state:
    st.session_state.games_to_play = 0
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0
if 'jackpot_wins' not in st.session_state:
    st.session_state.jackpot_wins = 0
if 'coins_earned' not in st.session_state:
    st.session_state.coins_earned = 0

# ---------- User Selection ----------
selected_user = st.selectbox("Choose a user:", list(df.index) + ["Game Owner"])

if selected_user == "Game Owner":
    st.markdown("🔒 Profit Summary Access Enabled")
    if st.button("📊 Show Owner Profit Summary"):
        st.markdown(f"**💼 Total Profit Earned by Game Owner:** `{st.session_state.owner_profit}` coins")
else:
    user = df.loc[selected_user]

    # Grant loan if user has zero balance
    if user['coins'] <= 0:
        user['coins'] += 50  # Loan granted
        df.loc[selected_user] = user
        df.to_csv(CSV_FILE)
        st.warning(f"💸 Loan granted: 50 coins")

    st.markdown(f"**💰 Coins:** {user['coins']}")

    # Ask for game count before play
    if st.session_state.games_to_play == 0:
        st.session_state.games_to_play = st.selectbox("How many games do you want to play?", [5, 10, 15, 20])

    # Play the game (one round at a time)
    if st.button("▶️ Play"):
        for _ in range(st.session_state.games_to_play):
            if user['coins'] < 10:
                st.error("❌ Insufficient coins! Exiting the game.")
                break  # End game early
            
            # Simulate drawing 6 balls randomly
            balls = random.choices(["Red", "Blue"], weights=[4, 2], k=6)
            red_count = balls.count("Red")
            blue_count = balls.count("Blue")

            if red_count == 4:
                payout = 30  # JACKPOT
                st.balloons()
                st.success(f"🎉 JACKPOT! You got 4 Red balls → Earned {payout} coins!")
                st.session_state.jackpot_wins += 1
            elif blue_count == 4:
                payout = 0  # No reward
                st.warning(f"🚫 No reward. You got 4 Blue balls.")
            else:
                payout = 5  # Regular reward
                st.info(f"🎲 You got {red_count} Red & {blue_count} Blue → Earned {payout} coins.")

            user['coins'] += payout - 10  # Deduct entry fee
            st.session_state.coins_earned += payout

            st.markdown(f"💰 **Updated Coin Balance:** {user['coins']}")

            time.sleep(1.5)  # Simulate delay for real-time play

        # Deduct loan at end of game
        if user['coins'] > 50:  
            user['coins'] -= 50  # If loan was granted, deduct from balance

        df.loc[selected_user] = user
        df.to_csv(CSV_FILE)

        # Summary at the end of all games
        st.subheader("🎮 Game Summary")
        st.markdown(f"- **Total Games Played:** {st.session_state.games_to_play}")
        st.markdown(f"- **Total Coins Earned:** {st.session_state.coins_earned}")
        st.markdown(f"- **Jackpot Wins:** {st.session_state.jackpot_wins}")
        st.markdown(f"- **Final Coin Balance:** {user['coins']}")

    # Quit Game & Save Coins
    if st.button("🚪 Quit Game"):
        df.to_csv(CSV_FILE)
        st.success("✅ Coins saved to your account. See you next time!")
