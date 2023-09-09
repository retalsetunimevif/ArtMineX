# $${\color{gold} ArtMineX }$$

ArtMineX is a social platform for creators and art enthusiasts, allowing users to showcase their works, photos, and art. Users can create profiles, manage groups, browse and like other users' artworks, and leave comments.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Managing Groups](#managing-groups)
4. [Liking and Commenting](#liking-and-commenting)
5. [Visiting User Profiles](#visiting-user-profiles)
6. [License](#license)

## Installation
1. Clone the repository to your local machine:
    ```
    git clone https://github.com/retalsetunimevif/ArtMineX.git
    ```
2. Create and activate a virtual environment (optional but recommended):
    ```
    python -m venv myenv
    source myenv/bin/activate  # On Windows, use 'myenv\Scripts\activate'
    ```
3. Install the required dependencies using pip:
    ```
    pip install -r requirements.txt
    ```
4. Run database migrations to set up the database:
    ```
    python manage.py migrate
    ```

5. To set up the project, create a $${\color{red}"projectSettings.py"}$$ file in the project directory and add the following content:
    ```python
    # ProjectSettings.py
    KEY = ''  # Paste your secret key here.
    USER = ''               # User login for connecting to the database.
    PASSWORD = ''           # Password for the user to connect to the database.
    DATABASE = ''           # Database name here.
    ```

6. For generating the secret key, follow these steps in the command-line or a Python shell:
- $${\color{red}Import \space \color{blue}"get\_random\_secret\_key()"\space \color{red}from \space \color{blue}"django.core.management.utils"}$$.
- Run the following code to generate a new secret key:

    Example:
    ```python
    Python Shell
    1: from django.core.management.utils import get_random_secret_key
    2: print(get_random_secret_key())
    ```

- Copy the generated secret key and paste it into the **"KEY"** variable in your **"projectSettings.py"** file.

    _*This configuration in **"projectSettings.py"** is essential for your Django project to work correctly. Ensure you keep the **"projectSettings.py"** file secure, especially the secret key._

7. Start the development server:
    ```
    python manage.py runserver
    ```
8. Have fun!

## Usage

After installing the application, you can:

- Add your own works, photos and artworks in the form of images.
- Create groups that you manage.
- Join your artworks to groups.
- Browse artworks from other users.
- Like and comment on images.
- Visit other users' profiles.

## Managing Groups

ArtMineX allows you to create and manage groups. You can:

- Create new groups.
- Manage group members.
- Join your artworks to groups.
- Browse artworks from other users within the group.

## Liking and Commenting

Users can like and leave comments on artworks. This allows you to express your opinion on a specific image or photo.

## Visiting User Profiles

You can visit other users' profiles, browse their artworks, and learn more about them.

## License

This project is protected by copyright and all rights are reserved. No part of this project may be reproduced or distributed in any form or by any means without prior written permission from the project owner, [Panek Marcin]. For inquiries, please contact [evilmeryl@gmail.com].