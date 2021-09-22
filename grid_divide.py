import pickle
import json
import utility as util
import pandas as pd


def main(df):
    # divide into grids
    dict = {}
    grid_size = 3.05
    count = 0
    final_grids = []

    for y in range(0, 10):
        y_cor = grid_size * (10 - y)
        # print('X cor: %.2f' % x_cor)
        # Get all the x related values
        ydf = df[(df['y'] < y_cor) & (df['y'] > (y_cor - grid_size))]
        for x in range(1, 21):
            x_cor = x * (grid_size)
            xdf = ydf[(ydf['x'] > (x_cor - grid_size))
                      & (ydf['x'] < x_cor)].copy()
            # print('(%.2f, %.2f)' % (x_cor, y_cor), end='\t')
            print(count, end='\t')
            if not xdf.empty:
                # dict['[%s] %.2f, %.2f' % (count, x_cor, y_cor)] = xdf
                # dict[count] = xdf
                xdf['grid'] = count
                final_grids.append(xdf)
            count += 1
        print()
    return pd.concat(final_grids)

# if loc.x < x and loc.y < y


if __name__ == '__main__':
    df = pd.read_csv('book.csv')
    new_d = main(df)
    new_d.to_csv('book_with_grids.csv')

    print(df[~df['device_id'].isin(new_d['device_id'])])
