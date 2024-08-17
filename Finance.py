import matplotlib.pyplot as plt
import numpy as np
import random

MONTHS_IN_YEAR = 12

# ---------------------------
# -- Fill these Variables ---
# ---------------------------

# Assumption - You will invest everything in your StartingNetWorth except your initial payment on mortgage
StartingNetWorth = 144_000                # starting sum in your bank - I.E הון עצמי התחלתי

# Market Growths
PortfolioGrowthAvg   = 8.5   # Average growth of Stocks (12% per year for SP500 dividends included)
Deviation            = 15  # std Deviation for calculating the growth, history shows its about 15
GrowthHouse          = 1                       # increase of house prices per year

# Expenses s.a rent \ mortgage
MoneySpentOnRent        = 0                 # ILS, each month on rent
MonthlyMortgagePayment  = 0             

# Mortgage data - Years \ House Value
YearsOfMortgage             = 30
HouseValueInDateOfPurchase  = 0        # ILS, "obtained" from mortgage - i.e the house value
InitialMortgagePayment      = 0                  # ההון העצמי ששים על משכנתא

# Money you save up and invest each month
ExtraAddedToPortfolioEachMonth = 4500            # ILS, stock purchase each month

# Simulation Variables
SimulationYears = 24                            # total simulation time      

# Unmask one of the two
SimMode = "Average"
# SimMode = "Gaussian"


# -- Ignore --
TotalMoneySpentOnRent = 0
TotalMoneySpentOnMortgage = 0
CurrentHouseValue = HouseValueInDateOfPurchase
MonthsOfMortgageLeft = MONTHS_IN_YEAR*YearsOfMortgage
CurrentPortfolioValue = StartingNetWorth - InitialMortgagePayment
TotalAmountInvestedByPerson = CurrentPortfolioValue

Growths = []
Data = []

FinalNetWorth = CurrentPortfolioValue  + CurrentHouseValue
for year in range(1, SimulationYears + 1):
    
    # For Average Unmask the next line
    if SimMode == "Average":
        Growth = PortfolioGrowthAvg
    elif SimMode == "Gaussian":
        Growth = np.random.default_rng().normal(PortfolioGrowthAvg, Deviation)

    for month in range(1, MONTHS_IN_YEAR + 1):
        Growths.append(Growth)
        
        # -----------------------
        # ---- For logging ------
        # -----------------------

        # Total money added during the years, from the person who saves
        TotalAmountInvestedByPerson   += ExtraAddedToPortfolioEachMonth           
        # you have to pay rent ? - Let log it for to see how much you paid after the sim ends
        TotalMoneySpentOnRent += MoneySpentOnRent
        
        if MonthsOfMortgageLeft > 0:
            TotalMoneySpentOnMortgage += MonthlyMortgagePayment # logging to see how much you've spent 

        # -----------------------
        # --- For simulations ---
        # -----------------------
        # you Invest some $$ each month
        CurrentPortfolioValue += ExtraAddedToPortfolioEachMonth           # Total Money in the portfolio, subject to ריבית דריבית
        
        # you have to pay mortgage untill you're done with this shit
        if MonthsOfMortgageLeft == 0: # No More mortgage - YAY - invest the extra $$$
            CurrentPortfolioValue += MonthlyMortgagePayment     # Total Money in the portfolio, subject to ריבית דריבית
        else: 
            MonthsOfMortgageLeft -= 1
        
        
        # another month has passed and your house is now worth more
        CurrentHouseValue = CurrentHouseValue * (1 + GrowthHouse / 100 / MONTHS_IN_YEAR)

        # your investments are hopefully paying off after this month
        CurrentPortfolioValue = CurrentPortfolioValue * (1 + Growth / 100 / MONTHS_IN_YEAR)

        # Updated NetWorth
        FinalNetWorth = CurrentPortfolioValue  + CurrentHouseValue
        Data.append(FinalNetWorth)


print (" ----------- Simulation results ------------- ")
print("Total Amount invested during the years = ", TotalAmountInvestedByPerson / 1000, " k")
print("Total From Compound interest", (CurrentPortfolioValue - TotalAmountInvestedByPerson) / 1000, " k")
print("Final Sum in the portfolio = ", (CurrentPortfolioValue / 1000), " k")
print (" ------------------------ ")
print("Total Spent On Rent = ", TotalMoneySpentOnRent/1000, "k")
print("Total Spent On Mortgage = ", TotalMoneySpentOnMortgage/1000, "k")
print("House Value = ", CurrentHouseValue/1000, "k")
print (" ------------------------ ")
print("Final Networth = ", (FinalNetWorth / 1000 ), " k")
print (" ------------------------ ")

plt.figure()
plt.title("Growths Vs years")
plt.plot(Growths)

plt.figure()
plt.title("Total Sum Projected Vs Months")
plt.plot(Data)

# Add (x, y) ticks with values on the graph
x_ticks = np.arange(0, len(Data), 12)
y_ticks = [Data[i] for i in x_ticks]

for x, y in zip(x_ticks, y_ticks):
    plt.annotate(f'({x}, {y/1000:.1f}k)', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

plt.xticks(x_ticks)
# plt.yticks(np.arange(0, max(Data), 5000))

plt.show()

