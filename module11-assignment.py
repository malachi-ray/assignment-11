# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8
            
            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise
            
            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80
    
    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)
        
        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], 
                                     p=[0.3, 0.5, 0.2])
        
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----
# TODO 1: Time Series Visualization - Sales Trends
# 1.1 Create a line chart showing overall quarterly sales trends
# REQUIRED: Function must create and return a matplotlib figure
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    # Your code here
    grouped_sales = sales_df.groupby('Quarter')['Sales'].sum()
    fig, ax = plt.subplots()
    ax.plot(grouped_sales.index, grouped_sales.values)
    ax.set_title("Sales by Quarter")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales")
    ax.grid(True, linestyle='--', alpha=0.6)
    return(fig)
    

# 1.2 Create a multi-line chart comparing sales trends across locations
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, ax = plt.subplots()
    for i in locations:
        location_frame = sales_df[sales_df['Location'] == i]
        grouped_loc_sales = location_frame.groupby('Quarter')['Sales'].sum()
        ax.plot(grouped_loc_sales.index, grouped_loc_sales.values, label=i.title())
    ax.set_title("Sales by Quarter for each Location")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    return(fig)

# TODO 2: Categorical Comparison - Product Performance by Location
# 2.1 Create a grouped bar chart comparing category performance by location
# REQUIRED: Function must create and return a matplotlib figure
x = np.arange(4)
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, ax = plt.subplots()
    
    for i in locations:
        elec_frame = sales_df[sales_df['Category'] == 'Electronics']
        elec_sales = elec_frame.groupby('Location')['Sales'].sum()
        ax.bar(x-0.24, elec_sales.values, color='green',label='Electronics',width=.12)
        cloth_frame = sales_df[sales_df['Category'] == 'Clothing']
        cloth_sales = cloth_frame.groupby('Location')['Sales'].sum()
        ax.bar(x-0.12, cloth_sales.values, color='red',label="Clothing",width=.12)
        hg_frame = sales_df[sales_df['Category'] == 'Home Goods']
        hg_sales = hg_frame.groupby('Location')['Sales'].sum()
        ax.bar(x, hg_sales.values, color='blue',label="Home Goods",width=.12)
        sg_frame = sales_df[sales_df['Category'] == 'Sporting Goods']
        sg_sales = sg_frame.groupby('Location')['Sales'].sum()
        ax.bar(x+.12, sg_sales.values, color='yellow',label="Sporting Goods",width=.12)
        bt_frame = sales_df[sales_df['Category'] == 'Beauty']
        bt_sales = bt_frame.groupby('Location')['Sales'].sum()
        ax.bar(x+.24, bt_sales.values, color='purple',label="Beauty",width=.12)
    
    ax.set_title("Category Sales by Location")
    ax.set_xlabel("Location")
    ax.set_ylabel("Total Sales (in 100,000s)")
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(x, ['Tampa', 'Miami', 'Orlando', 'Jacksonville'])
    ax.legend(['Electronics','Clothing','Home Goods','Sporting Goods','Beauty'])
    fig.tight_layout()
    return(fig)

# 2.2 Create a stacked bar chart showing the composition of sales in each location
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, ax = plt.subplots()
    bottom = np.zeros(4)
    for i in categories:
        cat_frame = sales_df[sales_df['Category'] == i]
        cat_sales = cat_frame.groupby('Location')['Sales'].sum()
        ax.bar(cat_sales.index, cat_sales.values, bottom=bottom, label = i)
        bottom+=cat_sales.values
    ax.set_title("Category Sales Composition by Location")
    ax.set_xlabel("Location")
    ax.set_ylabel("Total Sales (in 100,000s)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    return(fig)


# TODO 3: Relationship Analysis - Advertising and Sales
# 3.1 Create a scatter plot to examine the relationship between ad spend and sales
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, ax = plt.subplots()
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'], c=sales_df['AdSpend'], alpha=0.7)
    plt.title("Advertising Spend vs. Sales")
    plt.xlabel("Advertising Spend ($)")
    plt.ylabel("Sales ($)")
    plt.grid(True, linestyle='--', alpha=0.5)
    return(fig)

# 3.2 Create a line chart showing sales per dollar spent on advertising over time
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    # Your code here
    grouped_spds = sales_df.groupby('Quarter')['SalesPerDollarSpent'].mean()
    fig, ax = plt.subplots()
    ax.plot(grouped_spds.index, grouped_spds.values)
    ax.set_title("Avg Sales per Advertising $ Spent by Quarter")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Avg Sales per Advertising $ Spent")
    ax.grid(True, linestyle='--', alpha=0.6)
    return(fig)


# TODO 4: Distribution Analysis - Customer Demographics
# 4.1 Create histograms of customer age distribution
# REQUIRED: Function must create and return a matplotlib figure with subplots
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, axs = plt.subplots(2)
    axs[0].hist(customer_df['Age'], bins = 6,edgecolor="black")
    
    bins = np.linspace(customer_df['Age'].min(), customer_df['Age'].max(), 7)

    for i in locations:
        axs[1].hist(customer_df[customer_df['Location'] ==i]['Age'], label=i, bins = bins, alpha = 0.6,edgecolor='black')
    axs[0].set_title("Customer Ages Distribution")
    axs[0].set_xlabel("Customer Age Bins")
    axs[0].set_ylabel("Count")
    axs[1].set_title("Customer Ages Distribution by Location")
    axs[1].set_xlabel("Customer Age Bins")
    axs[1].set_ylabel("Count")
    axs[1].legend()
    fig.tight_layout()
    return(fig)

# 4.2 Create box plots comparing purchase amounts by age groups
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, ax = plt.subplots()
    young_amt = customer_df[customer_df['Age']<=25]['PurchaseAmount']
    midyoung_amt = customer_df[(customer_df['Age']>25)&(customer_df['Age']<=40)]["PurchaseAmount"]
    midold_amt = customer_df[(customer_df['Age']>40)&(customer_df['Age']<=55)]["PurchaseAmount"]
    old_amt = customer_df[(customer_df['Age']>55)&(customer_df['Age']<=70)]["PurchaseAmount"]
    vold_amt = customer_df[(customer_df['Age']>70)]["PurchaseAmount"]
    ax.boxplot([young_amt, midyoung_amt,midold_amt,old_amt,vold_amt], labels=['18-25',"26-40",'41-55','56-70','70+'])
    ax.set_title("Purchase Amount Distribution by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Purchase Amount")
    ax.grid(True, linestyle='--', alpha=0.6)
    return(fig)


# TODO 5: Sales Distribution - Pricing Tiers
# 5.1 Create a histogram of purchase amounts
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, ax = plt.subplots()
    ax.hist(customer_df['PurchaseAmount'],bins=15,edgecolor='Black')
    ax.set_title("Purchase Amount Distribution")
    ax.set_ylabel("Purchase Amount")
    ax.grid(True, linestyle='--', alpha=0.6)
    return(fig)

# 5.2 Create a pie chart showing sales breakdown by price tier
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    # Your code here
    vals_list = []
    labels_list = []
    for i in customer_df['PriceTier'].unique():
        tier_frame = customer_df[customer_df['PriceTier'] == i]
        tier_sales = tier_frame['PurchaseAmount'].sum()
        vals_list.append(tier_sales)
        labels_list.append(i)
    fig, ax = plt.subplots()
    ax.pie(vals_list,
    labels=labels_list,
    autopct='%1.1f%%',
    startangle=90,
    colors=['red','blue','green','orange']
    )
    ax.set_title("Sales Proportion by Price Tier")
    return(fig)


# TODO 6: Market Share Analysis
# 6.1 Create a pie chart showing sales breakdown by category
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, ax = plt.subplots()
    vals_list = []
    labels_list = []
    for i in categories:
        cat_frame = sales_df[sales_df['Category'] == i]
        cat_sales = cat_frame['Sales'].sum()
        vals_list.append(cat_sales)
        labels_list.append(i)
    ax.pie(vals_list,
    labels=labels_list,
    autopct='%1.1f%%',
    startangle=90,
    colors=['red','blue','green','orange', 'indigo']
    )
    ax.set_title("Sales Proportion by Category")
    return(fig)

# 6.2 Create a pie chart showing sales breakdown by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig, ax = plt.subplots()
    vals_list = []
    labels_list = []
    for i in locations:
        loc_frame = sales_df[sales_df['Location'] == i]
        loc_sales = loc_frame['Sales'].sum()
        vals_list.append(loc_sales)
        labels_list.append(i)
    ax.pie(vals_list,
    labels=labels_list,
    autopct='%1.1f%%',
    startangle=90,
    colors=['red','blue','green','orange']
    )
    ax.set_title("Sales Proportion by Category")
    return(fig)


# TODO 7: Comprehensive Dashboard
# REQUIRED: Function must create and return a matplotlib figure with at least 4 subplots
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    # Your code here
    fig, axs = plt.subplots(2,2,figsize=(12,8))
    for i in locations:
        elec_frame = sales_df[sales_df['Category'] == 'Electronics']
        elec_sales = elec_frame.groupby('Location')['Sales'].sum()
        axs[0,0].bar(x-0.24, elec_sales.values, color='green',label='Electronics',width=.12)
        cloth_frame = sales_df[sales_df['Category'] == 'Clothing']
        cloth_sales = cloth_frame.groupby('Location')['Sales'].sum()
        axs[0,0].bar(x-0.12, cloth_sales.values, color='red',label="Clothing",width=.12)
        hg_frame = sales_df[sales_df['Category'] == 'Home Goods']
        hg_sales = hg_frame.groupby('Location')['Sales'].sum()
        axs[0,0].bar(x, hg_sales.values, color='blue',label="Home Goods",width=.12)
        sg_frame = sales_df[sales_df['Category'] == 'Sporting Goods']
        sg_sales = sg_frame.groupby('Location')['Sales'].sum()
        axs[0,0].bar(x+.12, sg_sales.values, color='yellow',label="Sporting Goods",width=.12)
        bt_frame = sales_df[sales_df['Category'] == 'Beauty']
        bt_sales = bt_frame.groupby('Location')['Sales'].sum()
        axs[0,0].bar(x+.24, bt_sales.values, color='purple',label="Beauty",width=.12)
    
    axs[0,0].set_title("Category Sales by Location")
    axs[0,0].set_xlabel("Location")
    axs[0,0].set_ylabel("Total Sales (in 100,000s)")
    axs[0,0].grid(True, linestyle='--', alpha=0.6)
    plt.xticks(x, ['Tampa', 'Miami', 'Orlando', 'Jacksonville'])
    axs[0,0].legend(['Electronics','Clothing','Home Goods','Sporting Goods','Beauty'])
    
    young_amt = customer_df[customer_df['Age']<=25]['PurchaseAmount']
    midyoung_amt = customer_df[(customer_df['Age']>25)&(customer_df['Age']<=40)]["PurchaseAmount"]
    midold_amt = customer_df[(customer_df['Age']>40)&(customer_df['Age']<=55)]["PurchaseAmount"]
    old_amt = customer_df[(customer_df['Age']>55)&(customer_df['Age']<=70)]["PurchaseAmount"]
    vold_amt = customer_df[(customer_df['Age']>70)]["PurchaseAmount"]
    axs[0,1].boxplot([young_amt, midyoung_amt,midold_amt,old_amt,vold_amt], labels=['18-25',"26-40",'41-55','56-70','70+'])
    axs[0,1].set_title("Purchase Amount Distribution by Age Group")
    axs[0,1].set_xlabel("Age Group")
    axs[0,1].set_ylabel("Purchase Amount")
    axs[0,1].grid(True, linestyle='--', alpha=0.6)
    
    grouped_spds = sales_df.groupby('Quarter')['SalesPerDollarSpent'].mean()
    axs[1,0].plot(grouped_spds.index, grouped_spds.values)
    axs[1,0].set_title("Avg Sales per Advertising $ Spent by Quarter")
    axs[1,0].set_xlabel("Quarter")
    axs[1,0].set_ylabel("Avg Sales per Advertising $ Spent")
    axs[1,0].grid(True, linestyle='--', alpha=0.6)
    
    grouped_sales = sales_df.groupby('Quarter')['Sales'].sum()
    axs[1,1].plot(grouped_sales.index, grouped_sales.values)
    axs[1,1].set_title("Sales by Quarter")
    axs[1,1].set_xlabel("Quarter")
    axs[1,1].set_ylabel("Total Sales")
    axs[1,1].grid(True, linestyle='--', alpha=0.6)
    
    fig.tight_layout()
    return(fig)


# Main function to execute all visualizations
# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)
    
    # REQUIRED: Call all visualization functions and store figures
    # Store each figure in a variable for potential saving/display
    
    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    
    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    
    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    
    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    
    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    
    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    
    # Comprehensive Dashboard
    fig13 = create_business_dashboard()
    
    # REQUIRED: Add business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    # Your insights here based on the visualizations
    
    # Display all figures
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()