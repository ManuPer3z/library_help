# Personal Library Application

The Personal Library Application is a desktop-based Python application designed to manage personal consultations, incorporating functionalities such as user login, registration, data encryption, and a dynamic search feature. Developed with a focus on simplicity and efficiency, this application uses tkinter for the graphical user interface, cryptography for secure data handling, and PIL for image processing.

## Features

- **User Authentication**: Secure login and registration system to manage personal accounts.
- **Data Encryption**: Utilizes Fernet symmetric encryption to ensure that user data is stored securely.
- **Dynamic Search**: Offers live search suggestions to quickly find consultations within the personal library.
- **Image Handling**: Supports adding and viewing images associated with each consultation entry.
- **Data Persistence**: User data, including consultations and login information, is stored locally in an encrypted JSON file.

## Installation

To run the Personal Library Application, ensure you have Python installed on your system. This application was developed using Python 3.8, but it should be compatible with most Python 3.x versions.

1. Clone the repository to your local machine.
2. Install the required dependencies by running:

```bash
pip install tkinter Pillow cryptography json  
```
Note: tkinter might already be included in your Python installation.

Navigate to the cloned directory and run the application:

```bash

python main.py
```
## Usage
Upon launching the application, you will be greeted with a login screen. If you don't have an account, you can create one by clicking on the "Registrar nuevo usuario" button. After logging in, you can:

Add new consultations with optional images.
Edit or delete existing consultations.
Search through your consultations dynamically.
Encryption Key
The application uses a hardcoded encryption key for demonstration purposes. For actual use, it is highly recommended to generate a new key using Fernet.generate_key() and replace the existing one in the code. Keep this key secret and safe.

## Contributing
Contributions to the Personal Library Application are welcome! Please feel free to fork the repository, make changes, and submit a pull request with your improvements.

## License
This project is open-source and available under the MIT License. See the LICENSE file for more information.

```csharp
Just copy and paste this markdown into your README.md file on GitHub to get started! 
