# 📖 Bible Art-Maker API

This API creates customized images of Bible verses. It handles text justification and splitting across multiple images, making it ideal for social media, presentations, and personal reflection.

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

**Args**:

`verse_request (VerseRequest)`: The request object containing the book, chapter, and verse range.

**Return**:

The response object containing the requested verse(s) text.

```json
{
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
Generates an image with the requested Bible verse

**Args**:

`verse_request (VerseRequest)`: The request object containing the book, chapter, and verse range.

**Return**:

A JSON response with a message indicating that the image generation has been completed.
```json
{
    "message": "Image generation completed."
}
```

Image created:

<img src="https://raw.githubusercontent.com/josehenriqueroveda/bible-art-maker/main/app/assets/Jo%C3%A3o_16_33-33.jpg" width=720 class="inline"/>


## API Documentation
The API documentation is available at `http://localhost:8000/docs` or `http://localhost:8000/redoc`. You can use the documentation to explore the available endpoints and test them out.

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
