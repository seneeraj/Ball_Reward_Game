import streamlit as st
import random

# ---------- Initialize Session State ----------
if 'users' not in st.session_state:
    st.session_state.users = {
        'user1': {'coins': 100, 'games_to_play': 0, 'games_played': 0,
                  'loan_taken': False, 'loan_amount': 0, 'revenue': 0, 'payout': 0, 'history': []},
        'user2': {'coins': 100, 'games_to_play': 0, 'games_played': 0,
                  'loan_taken': False, 'loan_amount': 0, 'revenue': 0, 'payout': 0, 'history': []},
    }

if 'owner_profit' not in st.session_state:
    st.session_state.owner_profit = 0

# ---------- User Selection ----------
selected_user = st.selectbox("Choose a user:", list(st.session_state.users.keys()))
user = st.session_state.users[selected_user]

st.markdown(f"**💰 Coins:** {user['coins']}")
st.markdown(f"**🎮 Games Played:** {user['games_played']} / {user['games_to_play']}")

# ---------- Game Setup ----------
if user['games_to_play'] == 0 and user['coins'] >= 10:
    num_games = st.selectbox("Select number of games to play:", [5, 10, 15, 20], key=f"{selected_user}_game_select")
    if st.button("✅ Confirm Games"):
        total_fee = num_games * 10
        if user['coins'] < total_fee:
            loan = total_fee - user['coins']
            user['coins'] += loan
            user['loan_taken'] = True
            user['loan_amount'] += loan
            st.warning(f"💸 Loan granted: {loan} coins")

        user['coins'] -= total_fee
        user['games_to_play'] = num_games
        user['games_played'] = 0
        user['revenue'] += total_fee
        user['payout'] = 0
        user['history'] = []
        st.success(f"🎯 Game started for {num_games} rounds!")

# ---------- Game Play ----------
if user['games_to_play'] > 0 and user['games_played'] < user['games_to_play']:
    if user['coins'] < 10:
        st.error("🚫 You have less than 10 coins. Cannot continue. Click Reset to start a new round.")
    else:
        if st.button("▶️ Play"):
            ball = random.randint(1, 10)
            payout = 100 if ball == 7 else 5

            if ball == 7:
                st.balloons()
                st.success("🎉 JACKPOT! You hit 7!")
            else:
                st.info(f"You drew ball: {ball} and earned 5 coins.")

            user['coins'] += payout
            user['payout'] += payout
            user['games_played'] += 1
            user['history'].append(ball)

            st.markdown(f"**New Coin Balance:** {user['coins']}")

            if user['games_played'] == user['games_to_play']:
                profit = user['revenue'] - user['payout']
                st.session_state.owner_profit += profit
                st.warning("🎮 You've played all your games. Click Reset to start again.")

# ---------- Game Over Alert ----------
if user['games_to_play'] > 0 and user['games_played'] >= user['games_to_play']:
    st.warning("🎮 All games completed. Click Reset to play again.")

if user['coins'] < 10 and user['games_to_play'] == 0:
    st.error("🚫 You have less than 10 coins and cannot start a new game.")

# ---------- Reset Button ----------
if st.button("🔁 Reset Game"):
    if user['coins'] < 10:
        user['coins'] += 100
        st.info("💰 You had less than 10 coins. We've credited 100 new coins to your account!")

    user['games_to_play'] = 0
    user['games_played'] = 0
    user['loan_taken'] = False
    user['loan_amount'] = 0
    user['revenue'] = 0
    user['payout'] = 0
    user['history'] = []
    st.success("✅ Game has been reset. You can now start a new round.")
# ---------- Owner Profit Summary ----------
if st.button("📊 Show Owner Profit Summary"):
    st.markdown(f"**💼 Total Profit Earned by Game Owner:** `{st.session_state.owner_profit}` coins")
