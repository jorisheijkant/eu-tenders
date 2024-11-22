# EU tenders

With these scripts we convert EU tenders to a structured format (csv). Afterwards, we try and label them as urgent and/or with irregularities using a Large Language Model (LLM).

## Prerequisites

This script uses python, with pip as a package manager. Install the libraries needed (preferably in a virtual environment like conda) using `pip install -r requirements.txt`.

Moreover, the original script does use a local LLM. In this way, the analysis can be done for free and without sending data to the cloud. In order to get this working, you'll need [Ollama](https://ollama.com/). If you do want to use an API in the cloud, you can easily modify the code to do so.

## Data

This repo does not include the actual tenders to run the analysis on. Download these from the [EU Tender Journal](https://ted.europa.eu/en/). There's two folders in the repo, a `data/known_urgent` folder where you can place tenders that are urgent, in `data/random_tenders` you can place all sorts of tenders. When running the code, these will each have their own csv output. This is just so you can test the prompt and how well it functions.

In the `tenders_sample/` folder you can find a few tender examples, so you don't have to start from scratch. But please do not commit all tender xml's to the repo.

## Running the code

- After installing everything, run `python folders-to-csv.py` to create two csv files, one for the urgent tenders and one for all of them.
- Then run `python label-tenders.py` to start labeling the tenders. This will output two more csv files with labels. N.B.: modify the `limit` parameter according to the amount of tenders you feed into the script!

The labeling script may take quite some time, especially on older pc's that do not have a good graphics card.

## TODO:

- Parse all the necessary values of the XML so they end up in the csv file. [See here](https://docs.python.org/3/library/xml.etree.elementtree.html). This above may also lead to better results using the labeling.
- Make the prompt better! Also I'd suggest using a more capable version of Llama, that also includes better Dutch understanding.
- Include labeling irregularities in the prompt.

## Further hints:

- There seem to be hints in the XML of whether a contract is urgent, see for instance `<cbc:ProcessReasonCode listName="direct-award-justification">urgency</cbc:ProcessReasonCode>`.
