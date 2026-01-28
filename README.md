# megagigawhat-engine

# Mega Giga What Project

## Overview
The Mega Giga What project is a Python-based application that combines backend and frontend technologies to provide a seamless user experience. The project includes features such as IP information retrieval, data transfer time calculations, and static content pages for blogs, contact information, privacy policies, and terms of service.

## Features
- **Backend**:
  - FastAPI for handling API endpoints.
  - IP information retrieval via `ip_info_backend.py`.
  - Data transfer time calculations via `transfer_backend.py`.
- **Frontend**:
  - Streamlit for interactive web pages.
  - Static content pages for blog, contact, privacy, and terms.
- **Static Assets**:
  - CSS and HTML files for styling and layout.

## Project Structure
```
mega_giga_what/
├── ip_info_backend.py       # Backend for IP-related API endpoints
├── pages/                  # Streamlit pages and static content
│   ├── app.py              # Main Streamlit app
│   ├── transfer_time.py    # Data transfer time calculations
│   ├── blog.md             # Blog page content
│   ├── contact.md          # Contact page content
│   ├── privacy.md          # Privacy policy content
│   ├── terms.md            # Terms of service content
├── static/                 # Static assets
│   ├── css/                # CSS files
│   ├── html/               # HTML files
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd mega_giga_what
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Start the FastAPI backend:
   ```bash
   python ip_info_backend.py
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run pages/app.py
   ```
3. Open your browser and navigate to the provided URL to access the application.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- Python community for providing excellent libraries and frameworks.
- Streamlit and FastAPI teams for their amazing tools.
