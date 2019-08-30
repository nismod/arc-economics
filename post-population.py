"""Create GVA per capita

After running `simim` to provide population scenarios
"""
import glob
import os
import sys

import pandas


def main(base_path):
    print("Start")
    data_path = os.path.join(base_path, 'data_as_provided')
    output_path = os.path.join(base_path, 'data_processed')

    pop_filenames = glob.glob(os.path.join(data_path, 'arc_population__*.csv'))

    for pop_filename in pop_filenames:
        print("Processing", pop_filename)
        key = os.path.basename(pop_filename).replace(
            'arc_population__', '').replace('.csv', '')

        # HACK hard-code match for economics scenarios against 23k dwellings scenarios
        if "new-cities" in key:
            econ_key = "1-new-cities"
        elif key == "4-expansion23":
            econ_key = "2-expansion"
        else:
            econ_key = key

        econ_filename = os.path.join(output_path, 'arc_gva__{}.csv'.format(econ_key))

        gvapc = process_to_per_head(pop_filename, econ_filename)
        gvapc.to_csv(
            os.path.join(output_path, 'arc_gva_per_head__{}.csv'.format(key)), index=False)


def process_to_per_head(pop_filename, econ_filename):
    pop = pandas.read_csv(pop_filename)
    gva = pandas.read_csv(econ_filename)

    gvapc = gva.merge(pop, on=['timestep', 'lad_uk_2016'])
    gvapc['gva_per_head'] = gvapc.gva / gvapc.population
    gvapc = gvapc[['timestep', 'lad_uk_2016', 'gva_per_head']]
    return gvapc


if __name__ == '__main__':
    try:
        BASE_PATH = sys.argv[1]
    except:
        print("Usage: python {} <base_path>".format(__file__))
        exit(-1)

    main(BASE_PATH)
