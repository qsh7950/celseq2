#!/usr/bin/env python3

'''
Support Spatial Transcriptome Pipeline output

https://github.com/SpatialTranscriptomicsResearch/st_pipeline
'''
import argparse
import pandas as pd


def celseq2stpipeline(celseq2_fpath, spatial_map, out,
                      exclude_empty_spots, exclude_nondetected_genes):
    fhout = open(out, 'w')

    dict_spatial_seq2xy = {}
    with open(spatial_map, 'r') as fin:
        for row in fin:
            if row.startswith('#'):
                continue
            row = row.strip().split()
            dict_spatial_seq2xy[row[0]] = (row[1], row[2])

    if celseq2_fpath.endswith('h5') or celseq2_fpath.endswith('hdf5'):
        expr = pd.read_hdf(celseq2_fpath, 'table')  # genes x cells
    if celseq2_fpath.endswith('csv'):
        expr = pd.read_csv(celseq2_fpath, index_col=0)
    # df.loc[(df.sum(axis=1) != 0), (df.sum(axis=0) != 0)]
    if (exclude_empty_spots) and (exclude_nondetected_genes):
        expr_valid = expr.loc[(expr.sum(axis=1) != 0), (expr.sum(axis=0) != 0)]
    elif (not exclude_empty_spots) and (exclude_nondetected_genes):
        expr_valid = expr.loc[(expr.sum(axis=1) != 0), (expr.sum(axis=0) >= 0)]
    elif (exclude_empty_spots) and (not exclude_nondetected_genes):
        expr_valid = expr.loc[(expr.sum(axis=1) >= 0), (expr.sum(axis=0) != 0)]
    else:
        expr_valid = expr

    genes = map(lambda x: x.replace(' ', '_'), expr_valid.index.values)
    colnames = expr_valid.columns.values
    # fhout.write('{}\t{}\n'.format('', '\t'.join(genes)))  # header
    fhout.write('\t{}\n'.format('\t'.join(genes)))  # header

    for colname in colnames:
        tmp = colname.replace('.', '-') # BC-1-ATGC or ATGC
        spot_seq = tmp.split('-')[-1] # ATGC or ATGC
        spot_expr = expr_valid[colname].values
        spot_xy = dict_spatial_seq2xy.get(spot_seq, None)
        if not spot_xy:
            continue
        spot_xy = 'x'.join(map(str, spot_xy))
        fhout.write('{}\t{}\n'.format(
            spot_xy,
            '\t'.join(map(str, spot_expr))))
        # spot_x, spot_y = spot_xy
        # fhout.write('{}\t{}\t{}\n'.format(
        #     spot_x, spot_y,
        #     '\t'.join(map(str, spot_expr))))

    fhout.close()

    print(out)


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('celseq2', metavar='FILENAME', type=str,
                        help=('File path to expr.hdf5 (expr.h5 or expr.csv) generated by celseq2.'))
    parser.add_argument('spatial_map', metavar='FILENAME', type=str,
                        help='File path to spatial position dictionary.')
    parser.add_argument('out', metavar='FILENAME', type=str,
                        help=('File path to save st_pipeline readable'
                              ' output in tsv.'))
    parser.add_argument('--exclude-empty-spots', action='store_true',
                        help=('Exclude spots without any signals.'))
    parser.add_argument('--exclude-nondetected-genes', action='store_true',
                        help='Exclude genes with no UMIs.')

    args = parser.parse_args()

    celseq2stpipeline(args.celseq2, args.spatial_map, args.out,
                      args.exclude_empty_spots, args.exclude_nondetected_genes)


if __name__ == "__main__":
    main()
