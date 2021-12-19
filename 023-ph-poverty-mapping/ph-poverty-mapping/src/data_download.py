import pandas as pd
import logging
import data_utils
import data_download
import os
import sys
sys.path.insert(0, '../utils')

SEED = 42
print('make sure GEO_AI_API_KEY is set in .env')
print('make sure GEO_AI_SECRET_KEY is set in .env')
# os.environ['GEO_AI_API_KEY'] = os.environ.get('GEO_AI_API_KEY')
# os.environ['GEO_AI_SECRET_KEY'] = os.environ.get('GEO_AI_SECRET_KEY')


def main():
    data_path = '../data/'
    nightlights_bins_file = data_path + 'nightlights_bins.csv'
    satellite_images_dir = data_path + 'images/'
    training_images_dir = data_path + 'train_val/'
    report_dir = data_path + 'report/'
    report_file = report_dir + 'report.csv'

    try:
        data_download.get_satellite_images_with_labels(
            nightlights_bins_file,
            satellite_images_dir,
            report_dir,
            scale=1,
            zoom=17,
            imgsize=(400, 400)
        )
    except:
        logging.debug(
            "Could not download satellite images. Please set your API keys.")
        raise "Could not download satellite images. Please set your API keys."

    # To see how nightlights_bins_file was generated, please refer to
    #    notebooks/01_lights_eda.ipynb
    nightlights = pd.read_csv(nightlights_bins_file)
    report = pd.read_csv(report_file)

    # Initialize train and val sets
    nightlights = nightlights.sample(
        frac=1, random_state=SEED).reset_index(drop=True)
    train, val = data_utils.train_val_split(nightlights, train_size=0.9)
    train_balanced = data_utils.balance_dataset(train, size=30000)

    # Split dataset into training and validation sets
    data_utils.train_val_split_images(
        val, report, training_images_dir, phase='val')
    data_utils.train_val_split_images(
        train_balanced, report, training_images_dir, phase='train')


if __name__ == "__main__":
    main()
