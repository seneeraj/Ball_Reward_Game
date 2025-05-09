import streamlit as st
import pandas as pd
import random

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

    # Ask for game count if not initialized
    if st.session_state.games_to_play == 0:
        st.session_state.games_to_play = st.selectbox("Select number of games to play:", [5, 10, 15, 20])
        st.button("✅ Confirm Games")

    # Play the game
    if st.button("▶️ Play"):
        results = []
        for _ in range(st.session_state.games_to_play):
            if user['coins'] < 10:
                st.error("❌ Insufficient coins! Exiting the game.")
                break  # End game early
            
            # Simulate drawing 6 balls randomly
            balls = random.choices(["Red", "Blue"], weights=[4, 2], k=6)
            red_count = balls.count("Red")
            blue_count = balls.count("Blue")

            if red_count == 4:
                payout = 30  # JACKPOT if exactly 4 reds
                st.balloons()
                results.append(f"🎉 JACKPOT! You got 4 Red balls → Earned {payout} coins!")
            elif blue_count == 4:
                payout = 0  # No reward if 4 blue
                results.append(f"🚫 No reward. You got 4 Blue balls.")
            else:
                payout = 5  # Regular reward
                results.append(f"🎲 You got {red_count} Red & {blue_count} Blue → Earned {payout} coins.")

            user['coins'] += payout - 10  # Deduct entry fee
            st.session_state.owner_profit += 10  # Owner earns entry fee per game

        # Deduct loan at end of game
        if user['coins'] > 50:  
            user['coins'] -= 50  # If loan was granted, deduct from balance

        df.loc[selected_user] = user
        df.to_csv(CSV_FILE)
        st.markdown("\n".join(results))
        st.markdown(f"**New Coin Balance:** {user['coins']}")

    # Quit Game & Save Coins
    if st.button("🚪 Quit Game"):
        df.to_csv(CSV_FILE)
        st.success("✅ Coins saved to your account. See you next time!")
