import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random

# Set page configuration
st.set_page_config(
    page_title="SDG 2: Zero Hunger Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E7D32, #4CAF50);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 10px 0;
    }
    .stAlert > div {
        background-color: #e8f5e8;
        border: 1px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data for SDG 2 indicators
@st.cache_data
def generate_sdg2_data():
    # Global hunger data
    years = list(range(2015, 2024))
    regions = ['Sub-Saharan Africa', 'Asia', 'Latin America', 'North America', 'Europe', 'Oceania']
    
    # Undernourishment data (percentage of population)
    undernourishment_data = []
    for region in regions:
        base_rate = {
            'Sub-Saharan Africa': 25,
            'Asia': 12,
            'Latin America': 8,
            'North America': 3,
            'Europe': 2,
            'Oceania': 4
        }
        
        for year in years:
            # Simulate slight improvement over time with some fluctuation
            trend = -0.5 * (year - 2015)  # Slight decrease over time
            noise = random.uniform(-1, 1)
            rate = max(0, base_rate[region] + trend + noise)
            
            undernourishment_data.append({
                'Year': year,
                'Region': region,
                'Undernourishment_Rate': rate
            })
    
    # Food production data
    food_production_data = []
    crops = ['Cereals', 'Fruits', 'Vegetables', 'Meat', 'Dairy', 'Fish']
    
    for crop in crops:
        base_production = random.uniform(100, 500)
        for year in years:
            growth = 1.02 ** (year - 2015)  # 2% annual growth
            noise = random.uniform(0.95, 1.05)
            production = base_production * growth * noise
            
            food_production_data.append({
                'Year': year,
                'Crop': crop,
                'Production': production,
                'Unit': 'Million Tonnes'
            })
    
    # Food security data by country (sample)
    countries = ['Kenya', 'India', 'Brazil', 'Nigeria', 'Bangladesh', 'Ethiopia', 
                'Tanzania', 'Pakistan', 'Afghanistan', 'Madagascar']
    
    food_security_data = []
    for country in countries:
        for year in years:
            # Food security levels (1-4 scale: 1=Minimal, 2=Stressed, 3=Crisis, 4=Emergency)
            base_level = random.uniform(1.5, 3.5)
            trend = -0.05 * (year - 2015)  # Slight improvement
            level = max(1, min(4, base_level + trend + random.uniform(-0.2, 0.2)))
            
            food_security_data.append({
                'Year': year,
                'Country': country,
                'Food_Security_Level': level,
                'Population_Affected': random.uniform(5, 40)  # Millions
            })
    
    # Nutrition data
    nutrition_data = []
    indicators = ['Stunting', 'Wasting', 'Overweight']
    
    for region in regions:
        for indicator in indicators:
            base_rates = {
                'Stunting': {'Sub-Saharan Africa': 35, 'Asia': 25, 'Latin America': 15, 
                           'North America': 5, 'Europe': 3, 'Oceania': 8},
                'Wasting': {'Sub-Saharan Africa': 8, 'Asia': 12, 'Latin America': 4, 
                          'North America': 2, 'Europe': 1, 'Oceania': 3},
                'Overweight': {'Sub-Saharan Africa': 5, 'Asia': 8, 'Latin America': 12, 
                             'North America': 15, 'Europe': 13, 'Oceania': 18}
            }
            
            for year in years:
                trend_direction = -0.3 if indicator != 'Overweight' else 0.2
                trend = trend_direction * (year - 2015)
                noise = random.uniform(-0.5, 0.5)
                rate = max(0, base_rates[indicator][region] + trend + noise)
                
                nutrition_data.append({
                    'Year': year,
                    'Region': region,
                    'Indicator': indicator,
                    'Rate': rate
                })
    
    return (pd.DataFrame(undernourishment_data), 
            pd.DataFrame(food_production_data),
            pd.DataFrame(food_security_data),
            pd.DataFrame(nutrition_data))

# Load data
undernourishment_df, production_df, security_df, nutrition_df = generate_sdg2_data()

# Main header
st.markdown("""
<div class="main-header">
    <h1>🌾 SDG 2: Zero Hunger Dashboard</h1>
    <p>Monitoring progress towards ending hunger, achieving food security and improved nutrition</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.selectbox(
    "Select Analysis View",
    ["Overview", "Hunger & Undernourishment", "Food Production", "Food Security", "Nutrition Status", "Regional Comparison"]
)

# Overview Page
if page == "Overview":
    st.header("🎯 SDG 2 Key Metrics Overview")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        latest_undernourishment = undernourishment_df[undernourishment_df['Year'] == 2023]['Undernourishment_Rate'].mean()
        st.metric(
            "Global Undernourishment Rate",
            f"{latest_undernourishment:.1f}%",
            delta=f"-{abs(latest_undernourishment - 12.5):.1f}% vs 2015"
        )
    
    with col2:
        total_production = production_df[production_df['Year'] == 2023]['Production'].sum()
        st.metric(
            "Total Food Production",
            f"{total_production:.0f}M tonnes",
            delta="↗️ Growing"
        )
    
    with col3:
        crisis_countries = len(security_df[(security_df['Year'] == 2023) & 
                                         (security_df['Food_Security_Level'] >= 3)])
        st.metric(
            "Countries in Crisis",
            f"{crisis_countries}",
            delta="Needs attention"
        )
    
    with col4:
        avg_stunting = nutrition_df[(nutrition_df['Year'] == 2023) & 
                                   (nutrition_df['Indicator'] == 'Stunting')]['Rate'].mean()
        st.metric(
            "Global Stunting Rate",
            f"{avg_stunting:.1f}%",
            delta=f"-{abs(avg_stunting - 25):.1f}% vs 2015"
        )
    
    # Global trends chart
    st.subheader("🌍 Global Hunger Trends (2015-2023)")
    
    global_trend = undernourishment_df.groupby('Year')['Undernourishment_Rate'].mean().reset_index()
    
    fig = px.line(global_trend, x='Year', y='Undernourishment_Rate',
                  title='Global Average Undernourishment Rate',
                  markers=True,
                  line_shape='spline')
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Undernourishment Rate (%)",
        height=400,
        showlegend=False
    )
    fig.update_traces(line_color='#2E7D32', line_width=3, marker_size=8)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # SDG 2 targets progress
    st.subheader("🎯 SDG 2 Targets Progress")
    
    targets = [
        "End hunger and ensure access to safe, nutritious food",
        "End all forms of malnutrition",
        "Double agricultural productivity of small-scale farmers",
        "Ensure sustainable food production systems",
        "Maintain genetic diversity of crops and livestock"
    ]
    
    progress_values = [65, 58, 72, 45, 67]  # Sample progress percentages
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = go.Figure(go.Bar(
            y=targets,
            x=progress_values,
            orientation='h',
            marker_color=['#FF6B6B' if x < 50 else '#FFA726' if x < 70 else '#4CAF50' for x in progress_values],
            text=[f"{x}%" for x in progress_values],
            textposition="inside"
        ))
        
        fig.update_layout(
            title="SDG 2 Targets Progress",
            xaxis_title="Progress (%)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Regional comparison pie chart
        regional_data = undernourishment_df[undernourishment_df['Year'] == 2023]
        fig = px.pie(regional_data, values='Undernourishment_Rate', names='Region',
                     title='Undernourishment by Region (2023)')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

# Hunger & Undernourishment Page
elif page == "Hunger & Undernourishment":
    st.header("🍽️ Hunger & Undernourishment Analysis")
    
    # Time series by region
    fig = px.line(undernourishment_df, x='Year', y='Undernourishment_Rate', 
                  color='Region', title='Undernourishment Trends by Region',
                  markers=True)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Regional comparison for latest year
    col1, col2 = st.columns(2)
    
    with col1:
        latest_data = undernourishment_df[undernourishment_df['Year'] == 2023]
        fig = px.bar(latest_data, x='Region', y='Undernourishment_Rate',
                     title='Undernourishment Rate by Region (2023)',
                     color='Undernourishment_Rate',
                     color_continuous_scale='Reds')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Heatmap of undernourishment over time
        pivot_data = undernourishment_df.pivot(index='Region', columns='Year', values='Undernourishment_Rate')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Reds',
            showscale=True
        ))
        
        fig.update_layout(
            title='Undernourishment Rate Heatmap',
            xaxis_title='Year',
            yaxis_title='Region',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("📊 Detailed Data")
    selected_region = st.selectbox("Select Region for Details", undernourishment_df['Region'].unique())
    filtered_data = undernourishment_df[undernourishment_df['Region'] == selected_region]
    st.dataframe(filtered_data, use_container_width=True)

# Food Production Page
elif page == "Food Production":
    st.header("🌾 Food Production Analysis")
    
    # Production trends by crop type
    fig = px.line(production_df, x='Year', y='Production', color='Crop',
                  title='Food Production Trends by Crop Type',
                  markers=True)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Production by crop type (latest year)
        latest_production = production_df[production_df['Year'] == 2023]
        fig = px.pie(latest_production, values='Production', names='Crop',
                     title='Production Share by Crop Type (2023)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Growth rate calculation
        growth_rates = []
        for crop in production_df['Crop'].unique():
            crop_data = production_df[production_df['Crop'] == crop]
            first_year = crop_data[crop_data['Year'] == 2015]['Production'].iloc[0]
            last_year = crop_data[crop_data['Year'] == 2023]['Production'].iloc[0]
            growth_rate = ((last_year / first_year) ** (1/8) - 1) * 100
            growth_rates.append({'Crop': crop, 'Growth_Rate': growth_rate})
        
        growth_df = pd.DataFrame(growth_rates)
        fig = px.bar(growth_df, x='Crop', y='Growth_Rate',
                     title='Annual Growth Rate by Crop (2015-2023)',
                     color='Growth_Rate',
                     color_continuous_scale='RdYlGn')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Production efficiency metrics
    st.subheader("📈 Production Efficiency")
    
    # Simulate productivity data
    productivity_data = []
    for year in range(2015, 2024):
        base_productivity = 100
        growth = 1.03 ** (year - 2015)  # 3% annual growth
        productivity = base_productivity * growth
        productivity_data.append({'Year': year, 'Productivity_Index': productivity})
    
    productivity_df = pd.DataFrame(productivity_data)
    
    fig = px.bar(productivity_df, x='Year', y='Productivity_Index',
                 title='Agricultural Productivity Index',
                 color='Productivity_Index',
                 color_continuous_scale='Greens')
    st.plotly_chart(fig, use_container_width=True)

# Food Security Page
elif page == "Food Security":
    st.header("🛡️ Food Security Analysis")
    
    # Food security levels by country
    latest_security = security_df[security_df['Year'] == 2023]
    
    fig = px.scatter(latest_security, x='Country', y='Food_Security_Level',
                     size='Population_Affected', color='Food_Security_Level',
                     title='Food Security Status by Country (2023)',
                     color_continuous_scale='RdYlGn_r',
                     size_max=30)
    fig.update_xaxes(tickangle=45)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution of food security levels
        security_counts = latest_security.groupby('Food_Security_Level').size().reset_index()
        security_counts.columns = ['Food_Security_Level', 'Count']
        security_counts['Level_Name'] = security_counts['Food_Security_Level'].map({
            1: 'Minimal', 2: 'Stressed', 3: 'Crisis', 4: 'Emergency'
        })
        
        fig = px.pie(security_counts, values='Count', names='Level_Name',
                     title='Distribution of Food Security Levels',
                     color_discrete_map={'Minimal': '#4CAF50', 'Stressed': '#FFC107',
                                       'Crisis': '#FF9800', 'Emergency': '#F44336'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Timeline of food security for selected country
        selected_country = st.selectbox("Select Country", security_df['Country'].unique())
        country_data = security_df[security_df['Country'] == selected_country]
        
        fig = px.line(country_data, x='Year', y='Food_Security_Level',
                      title=f'Food Security Trend - {selected_country}',
                      markers=True)
        fig.update_layout(yaxis_title="Food Security Level (1-4)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Population affected analysis
    st.subheader("👥 Population Impact Analysis")
    
    total_affected = security_df.groupby('Year')['Population_Affected'].sum().reset_index()
    
    fig = px.area(total_affected, x='Year', y='Population_Affected',
                  title='Total Population Affected by Food Insecurity',
                  color_discrete_sequence=['#FF6B6B'])
    fig.update_layout(yaxis_title="Population Affected (Millions)")
    st.plotly_chart(fig, use_container_width=True)

# Nutrition Status Page
elif page == "Nutrition Status":
    st.header("🥗 Nutrition Status Analysis")
    
    # Multi-indicator nutrition trends
    fig = px.line(nutrition_df, x='Year', y='Rate', color='Indicator',
                  facet_col='Region', facet_col_wrap=3,
                  title='Nutrition Indicators by Region',
                  markers=True)
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Current nutrition status comparison
    st.subheader("📊 Current Nutrition Status (2023)")
    
    latest_nutrition = nutrition_df[nutrition_df['Year'] == 2023]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stunting rates by region
        stunting_data = latest_nutrition[latest_nutrition['Indicator'] == 'Stunting']
        fig = px.bar(stunting_data, x='Region', y='Rate',
                     title='Child Stunting Rates by Region',
                     color='Rate',
                     color_continuous_scale='Reds')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # All indicators comparison
        avg_by_indicator = latest_nutrition.groupby('Indicator')['Rate'].mean().reset_index()
        fig = px.bar(avg_by_indicator, x='Indicator', y='Rate',
                     title='Global Average Nutrition Indicators',
                     color='Indicator',
                     color_discrete_map={'Stunting': '#FF6B6B', 'Wasting': '#FFA726', 'Overweight': '#42A5F5'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Nutrition heatmap
    st.subheader("🔥 Nutrition Status Heatmap")
    
    nutrition_pivot = latest_nutrition.pivot(index='Region', columns='Indicator', values='Rate')
    
    fig = go.Figure(data=go.Heatmap(
        z=nutrition_pivot.values,
        x=nutrition_pivot.columns,
        y=nutrition_pivot.index,
        colorscale='RdYlBu_r',
        showscale=True,
        text=np.round(nutrition_pivot.values, 1),
        texttemplate="%{text}%",
        textfont={"size":12}
    ))
    
    fig.update_layout(
        title='Nutrition Indicators Heatmap by Region (2023)',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Progress tracking
    st.subheader("📈 Progress Tracking")
    
    progress_data = []
    for indicator in nutrition_df['Indicator'].unique():
        indicator_data = nutrition_df[nutrition_df['Indicator'] == indicator]
        start_value = indicator_data[indicator_data['Year'] == 2015]['Rate'].mean()
        end_value = indicator_data[indicator_data['Year'] == 2023]['Rate'].mean()
        
        if indicator == 'Overweight':
            change = end_value - start_value  # For overweight, increase is bad
            target_direction = "Decrease"
        else:
            change = start_value - end_value  # For stunting/wasting, decrease is good
            target_direction = "Decrease"
        
        progress_data.append({
            'Indicator': indicator,
            'Change': change,
            'Direction': 'Improving' if change > 0 else 'Worsening',
            'Target': target_direction
        })
    
    progress_df = pd.DataFrame(progress_data)
    st.dataframe(progress_df, use_container_width=True)

# Regional Comparison Page
elif page == "Regional Comparison":
    st.header("🌐 Regional Comparison Analysis")
    
    # Multi-metric dashboard
    selected_year = st.slider("Select Year", 2015, 2023, 2023)
    
    # Prepare comparison data
    year_undernourishment = undernourishment_df[undernourishment_df['Year'] == selected_year]
    year_nutrition = nutrition_df[nutrition_df['Year'] == selected_year]
    
    stunting_data = year_nutrition[year_nutrition['Indicator'] == 'Stunting'][['Region', 'Rate']]
    stunting_data = stunting_data.rename(columns={'Rate': 'Stunting_Rate'})
    
    comparison_data = year_undernourishment.merge(stunting_data, on='Region')
    
    # Scatter plot comparison
    fig = px.scatter(comparison_data, x='Undernourishment_Rate', y='Stunting_Rate',
                     size=[100]*len(comparison_data), color='Region',
                     title=f'Undernourishment vs Stunting by Region ({selected_year})',
                     hover_data=['Region'],
                     size_max=20)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Regional performance radar chart
    st.subheader("📡 Regional Performance Radar")
    
    selected_regions = st.multiselect(
        "Select Regions for Comparison",
        year_undernourishment['Region'].tolist(),
        default=['Sub-Saharan Africa', 'Asia', 'Europe']
    )
    
    if selected_regions:
        fig = go.Figure()
        
        categories = ['Undernourishment', 'Stunting', 'Food Security', 'Production Growth']
        
        for region in selected_regions:
            # Get values for each category (normalized to 0-100 scale)
            undernourishment_val = 100 - year_undernourishment[year_undernourishment['Region'] == region]['Undernourishment_Rate'].iloc[0] * 3
            stunting_val = 100 - year_nutrition[(year_nutrition['Region'] == region) & (year_nutrition['Indicator'] == 'Stunting')]['Rate'].iloc[0] * 2
            
            # Mock values for other categories
            food_security_val = np.random.uniform(60, 95)
            production_val = np.random.uniform(70, 90)
            
            values = [undernourishment_val, stunting_val, food_security_val, production_val]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=region
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Regional Performance Comparison (Higher is Better)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Ranking table
    st.subheader("🏆 Regional Rankings")
    
    ranking_data = year_undernourishment.copy()
    ranking_data['Undernourishment_Rank'] = ranking_data['Undernourishment_Rate'].rank()
    
    stunting_ranks = year_nutrition[year_nutrition['Indicator'] == 'Stunting'].copy()
    stunting_ranks['Stunting_Rank'] = stunting_ranks['Rate'].rank()
    stunting_ranks = stunting_ranks[['Region', 'Stunting_Rank']]
    
    final_ranking = ranking_data.merge(stunting_ranks, on='Region')
    final_ranking['Overall_Score'] = (final_ranking['Undernourishment_Rank'] + final_ranking['Stunting_Rank']) / 2
    final_ranking = final_ranking.sort_values('Overall_Score')
    
    st.dataframe(final_ranking[['Region', 'Undernourishment_Rate', 'Undernourishment_Rank', 
                               'Stunting_Rank', 'Overall_Score']], use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🌾 SDG 2: Zero Hunger Dashboard | Data visualization for sustainable development</p>
    <p>Target: End hunger, achieve food security and improved nutrition, and promote sustainable agriculture by 2030</p>
</div>
""", unsafe_allow_html=True)
 