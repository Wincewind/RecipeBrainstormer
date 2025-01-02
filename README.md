# RecipeBrainstormer
An app prototype for searching/generating recipe ideas. Selected recipes will provide tags so that meals using shared ingredients can be searched.
One version of the app uses [TheMealDB](https://www.themealdb.com/api.php) API to provide recipes and the other Google's generative AI models.

## How to setup and run locally (tested in Linux and Windows environments):


To run the app using a GenAI model, you need to get a key to the API. You can find a quickstart guide [here](https://ai.google.dev/gemini-api/docs/quickstart?authuser=1&lang=python).

Once you have an API key, create a `.env` file similarly to the `.env.example`. After this, the calls to the GenAI API should work.

Here's a one-liner to setup and run TheMealDB using version of the app:
For linux:

```bash
git clone https://github.com/Wincewind/RecipeBrainstormer.git; cd RecipeBrainstormer/; python3 -m venv venv; source venv/bin/activate; pip install -r requirements.txt; python3 app.py
```
For Windows:

```bash
git clone https://github.com/Wincewind/RecipeBrainstormer.git; cd RecipeBrainstormer/; python3 -m venv venv; venv/Scripts/activate; pip install -r requirements.txt; python3 app.py
```

1.  Clone the repository or download it as a zip:
```bash
git clone https://github.com/Wincewind/RecipeBrainstormer.git
```

2.  In the project folder, create a virtual environment and activate it
```bash
python -m venv venv
```
```bash
source venv/bin/activate
```
or
```bash
venv/Scripts/activate
```

3.  Install required modules in the virtual env
```bash
pip install -r requirements.txt
```
4.  Run app using **TheMealDB**
```bash
python app.py
```
5.  Run app using a GenAI models
```bash
python ai_app.py
```
