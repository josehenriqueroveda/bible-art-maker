# 📖 Bible Art-Maker API

[![Bandit](https://github.com/josehenriqueroveda/bible-art-maker/actions/workflows/bandit.yml/badge.svg)](https://github.com/josehenriqueroveda/bible-art-maker/actions/workflows/bandit.yml)
[![Lint](https://github.com/josehenriqueroveda/bible-art-maker/actions/workflows/black.yml/badge.svg)](https://github.com/josehenriqueroveda/bible-art-maker/actions/workflows/black.yml)

API that creates customized images of Bible verses. Ideal for social media, presentations, and personal reflection.

## Installation
To install this API, clone the repository and install the dependencies:
```bash
git clone https://github.com/your-username/bible-art-maker-api.git
cd bible-art-maker-api
pip install -r requirements.txt
```

## Usage
To start the API server, run the following command:
```bash
uvicorn main:app --reload
```
or
```bash
python main.py
```

This will start the API on port 8777 or the configured IP and Port.


## API Endpoints
The following API endpoints are available:
### Bible Books
```http
GET /v1/bible/books
```

**Return**:

Returns a list of all books in the Bible.

```python
["Gênesis", ..., "Apocalipse"]
```

### Bible Verses
```http
POST /v1/bible/verse
```
Retrieves the text of a specific verse or range of verses from the Bible.

Available bible versions:
- `nvi`: Nova Versão Internacional
- `acf`: Almeida Corrigida Fiel
- `aa`: Almeida Atualizada

**Args**:

`verse_request (VerseRequest)`: The request object containing the version, book, chapter, and verse range.

**Return**:

The response object containing the requested verse(s) text.

```json
{
  "version": "nvi",
  "book": "João",
  "chapter": 16,
  "start_verse": 33,
  "end_verse": 33,
  "response": "Eu lhes disse essas coisas para que em mim vocês tenham paz. Neste mundo vocês terão aflições; contudo, tenham ânimo! Eu venci o mundo."
}
```

## Image Maker
```http
POST /v1/image/verse
```
Generates an image with the requested Bible verse.

Available bible versions:
- `nvi`: Nova Versão Internacional
- `acf`: Almeida Corrigida Fiel
- `aa`: Almeida Atualizada

**Args**:

`verse_request (VerseRequest)`: The request object containing the version, book, chapter, verse range and mobile flag.

**Return**:

`FileResponse`: The image file.


### Images created:
**NVI**:

<img src="https://raw.githubusercontent.com/josehenriqueroveda/bible-art-maker/main/app/images/Isa%C3%ADas_54_16-17.jpg" width=720 class="inline"/>

**ACF**:

<img src="https://raw.githubusercontent.com/josehenriqueroveda/bible-art-maker/main/app/images/Deuteron%C3%B4mio_31_8.jpg" width=720 class="inline"/>

**AA**:

<img src="https://raw.githubusercontent.com/josehenriqueroveda/bible-art-maker/main/app/images/Jo%C3%A3o_16_33.jpg" width=720 class="inline"/>


### Image created for mobile:

<img src="https://raw.githubusercontent.com/josehenriqueroveda/bible-art-maker/main/app/images/Filipenses_4_7.jpg" width=320 class="inline"/>


## API Documentation
The API documentation is available at `http://localhost:8777/docs` or `http://localhost:8777/redoc`. You can use the documentation to explore the available endpoints and test them out.

## License
This package is licensed under the GNU License. See the [LICENSE](LICENSE) file for details.

## Contributing
If you find a bug or have a feature request, please open an issue on the repository. If you would like to contribute code, please fork the repository and submit a pull request.

Before submitting a pull request, please make sure that your code adheres to the following guidelines:
 - Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
 - Write docstrings for all functions and classes.
 - Write unit tests for all functions and classes.
 - Make sure that all tests pass by running pytest.
 - Keep the code simple and easy to understand.
