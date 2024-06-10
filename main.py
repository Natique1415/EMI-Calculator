import streamlit as st
import plotly.graph_objects as go

st.header("Car Loan EMI Calculator")

# User Input
principal_amount = st.number_input("Loan Amount", min_value=0, value=100000)
annual_interest_rate = st.number_input(
    "Annual Interest Rate ( in % )", min_value=0.0, value=8.0
)
years = st.number_input("Loan term ( No. of years )", min_value=1)

# Monthly interest rate
interest_rate_monthly = annual_interest_rate / (12 * 100)
months = years * 12

# Calculate EMI
if interest_rate_monthly > 0:
    emi = (
        principal_amount
        * interest_rate_monthly
        * ((1 + interest_rate_monthly) ** months)
    ) / (((1 + interest_rate_monthly) ** months) - 1)
else:
    emi = principal_amount / months

st.write(f"####  ***EMI = ${emi:,.2f}***")

# Calculate total payment and total interest
total_payment = emi * months
total_interest = total_payment - principal_amount

# Spacing
st.markdown("***")

# Infographic
st.subheader("Infographics")

# Pie chart
labels = ["Principal amount", "Interest amount"]
values = [principal_amount, total_interest]

fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.6)])
fig.update_traces(
    marker=dict(colors=["#FF6F61", "#6B5B95"]),
    textfont=dict(size=17),  # Adjusting text size within the pie chart
)

fig.update_layout(
    title_text="Break-up Of Total Payment",
    title_font=dict(size=20),  # Title font size
)
st.plotly_chart(fig)


# Line Graph
st.write("#### Loan Payment Schedule ( Years )")
principal_per_payment = principal_amount / months  # Assuming equal principal payments
remaining_balance = [principal_amount]

for month in range(1, months + 1):
    # Assuming interest is paid on the remaining balance each month
    interest_payment = remaining_balance[-1] * interest_rate_monthly
    remaining_balance.append(
        remaining_balance[-1] - principal_per_payment - interest_payment
    )

# Convert months to years for x-axis (assuming equal number of months in each year)
years_list = [month / 12 for month in range(months + 1)]

# Create line chart
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=years_list, y=remaining_balance, name="Remaining Loan Balance", mode="lines"
    )
)
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Remaining Balance",
)

st.plotly_chart(fig)
