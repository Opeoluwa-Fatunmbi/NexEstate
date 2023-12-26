# NexEstate

NexEstate is a Django-based real estate listing web application that allows users to browse and search for properties, view property details, and contact property owners or agents.

## Features

- User Registration and Authentication: Users can create an account, log in, and manage their profile.
- Property Listings: Users can view a list of available properties, filter them based on criteria such as location, price, and property type.
- Property Details: Users can view detailed information about a particular property, including images, description, amenities, and contact information.
- Property Search: Users can search for properties based on specific criteria such as location, price range, property type, and more.
- Contact Property Owner/Agent: Users can send inquiries or contact property owners or agents directly through the application.
- Admin Dashboard: Admin users have access to a dashboard where they can manage property listings, user accounts, and system settings.

## Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/Opeoluwa-Fatunmbi/NexEstate.git
    ```

2. Navigate to the project directory:

    ```shell
    cd NexEstate
    ```

3. Create a virtual environment:

    ```shell
    python -m venv venv
    ```

4. Activate the virtual environment:

    - For Windows:

      ```shell
      venv\Scripts\activate
      ```

    - For macOS and Linux:

      ```shell
      source venv/bin/activate
      ```

5. Install the required dependencies:

    ```shell
    pip install -r requirements.txt
    ```

6. Run database migrations:

    ```shell
    python manage.py migrate
    ```

7. Start the development server:

    ```shell
    python manage.py runserver
    ```

8. Open your web browser and visit `http://localhost:8000` to access the NexEstate application.
