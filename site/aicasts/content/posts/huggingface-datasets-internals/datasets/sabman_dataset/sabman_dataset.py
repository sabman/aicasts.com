# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# TODO: Address all TODOs and remove all explanatory comments
"""Time Series Datasets (TSD) for the SABMAN project."""


import csv
import json
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@misc{misc_electricityloaddiagrams20112014_321,
  author       = {Trindade, Artur},
  title        = {{ElectricityLoadDiagrams20112014}},
  year         = {2015},
  howpublished = {UCI Machine Learning Repository}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This new dataset is designed to do time series forecasting of Electric Demand.
see: https://gist.github.com/czarinacatambing/3819d86538c99b42cd88481f67263f62
"""

_HOMEPAGE = "https://archive-beta.ics.uci.edu/ml/datasets/electricityloaddiagrams20112014"
# "https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLS = {
    "electricity_load": "https://archive.ics.uci.edu/ml/machine-learning-databases/00321/LD2011_2014.txt.zip",
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class NewDataset(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="first_domain", version=VERSION,
                               description="This part of my dataset covers a first domain"),
        datasets.BuilderConfig(name="second_domain", version=VERSION,
                               description="This part of my dataset covers a second domain"),
    ]

    # It's not mandatory to have a default configuration. Just use one if it make sense.
    DEFAULT_CONFIG_NAME = "first_domain"

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        # This is the name of the configuration selected in BUILDER_CONFIGS above
        if self.config.name == "first_domain":
            features = datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "option1": datasets.Value("string"),
                    "answer": datasets.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "option2": datasets.Value("string"),
                    "second_domain_answer": datasets.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            # Here we define them above because they are different between the two configurations
            features=features,
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls = _URLS[self.config.name]
        data_dir = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.jsonl"),
                    "split": "test"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.jsonl"),
                    "split": "dev",
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        with open(filepath, encoding="utf-8") as f:
            for key, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "first_domain":
                    # Yields examples as (key, example) tuples
                    yield key, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "answer": "" if split == "test" else data["answer"],
                    }
                else:
                    yield key, {
                        "sentence": data["sentence"],
                        "option2": data["option2"],
                        "second_domain_answer": "" if split == "test" else data["second_domain_answer"],
                    }
