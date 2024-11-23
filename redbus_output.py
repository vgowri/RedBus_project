import streamlit as st
import pandas as pd
import pymysql
import time

data = pd.read_csv('cleaned_bus_routes.csv')

def get_connection():
    return pymysql.connect(host='127.0.0.1', 
                            user ='root', 
                            password='1991', 
                            database='redbus_project')

def fetch_route_names(data, starting_letter):
    route_names = data[data['Route_Name'].str.startswith(starting_letter.upper())]['Route_Name'].unique()
    return route_names


def fetch_data(data, route_name, price_sort_order, star_rating_filter,selected_bus_type =None):
    # Ensure the data types are correct for sorting
    data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce')
    data['Fare'] = pd.to_numeric(data['Fare'], errors='coerce')
    data['Bus_Type'] = pd.to_numeric(data['Bus_Type'], errors='coerce')

    # Sort data by price ,bus_type and rating
    sorted_data = data[data['Route_Name'] == route_name].sort_values(by=['Rating', 'Fare','Bus_Type'], ascending=[False, price_sort_order == "Low to High"])
    
    # Filter by star rating if specified
    if star_rating_filter:
        sorted_data = sorted_data[sorted_data['Rating'].isin(star_rating_filter)]
    
    return sorted_data 

def filter_data(data, star_ratings, bus_types):
    filtered_data = data[data['Rating'].isin(star_ratings) & data['Bus_Type'].isin(bus_types)]
    return filtered_data

# Main app
def main():
    # Load the cleaned dataset
    data = pd.read_csv('cleaned_bus_routes.csv')
    
    # Display image and header
    st.image(r'C:\Users\admin\Desktop\redbus logo\rdc-redbus-logo.webp')
    st.header('India\'s No. 1 Online Bus Ticket Booking Site')

    # Page navigation
    page = st.selectbox("Choose a page", ["Search Bus Routes", "View Data"])

    if page == "Search Bus Routes":
        # Search page
        starting_letter = st.text_input('Enter starting letter of Route Name', 'A')

        if starting_letter:
            route_names = fetch_route_names(data, starting_letter.upper())

            if route_names.size > 0:
                # Route Name selection
                selected_route = st.selectbox('Select Route Name', route_names)

                if selected_route:
                    # Price sorting
                    price_sort_order = st.selectbox('Sort by Price', ['Low to High', 'High to Low'])

                    # Star Rating filter
                    star_ratings = data['Rating'].unique().tolist()
                    selected_ratings = st.multiselect('Filter by Rating', star_ratings)

                    bus_type = data['Bus_Type'].unique().tolist()
                    selected_bus_type = st.multiselect('Filter by bus type', bus_type)

                    search_button = st.button('Search')

                    if search_button:
                        # Fetch data based on selected Route_Name, price sort order, and selected star ratings
                        data = fetch_data(data, selected_route, price_sort_order, selected_ratings)

                        if not data.empty:
                            # Store data in session state for later use
                            st.session_state.data = data
                            st.session_state.selected_route = selected_route
                            st.session_state.price_sort_order = price_sort_order

                            st.success(f"Data for route {selected_route} has been fetched. Go to 'View Data' to see the details.")
                        else:
                            st.write(f"No data found for Route: {selected_route} with the specified price sort order and ratings.")
            else:
                st.write("No routes found starting with the letter:", starting_letter)

    elif page == "View Data":
        # Data page
        if 'data' in st.session_state:
            data = st.session_state.data
            selected_route = st.session_state.selected_route
            price_sort_order = st.session_state.price_sort_order

            st.write(f"### Data for Route: {selected_route}")
            st.write(data)  # Display the full DataFrame

            # Show available seats and ratings
            st.write(f"### Available Seats and Ratings")
            st.write(f"Total Available Seats: {data['Seat_Available'].sum()}")
            st.write(f"Average Star Rating: {data['Rating'].mean()}")

            star_ratings = data['Rating'].unique().tolist()
            selected_ratings = st.multiselect('Filter by Star Rating', star_ratings)

            
            bus_types = data['Bus_Type'].unique().tolist()  
            selected_bus_types = st.multiselect('Filter by Bus Type', bus_types)  


            if selected_ratings and selected_bus_types:
                filtered_data = filter_data(data, selected_ratings, selected_bus_types)
                
                st.write(filtered_data)
        else:
            st.write("No data available. Please fetch data from the 'Search Bus Routes' page first.")

if __name__ == '__main__':
    main()
