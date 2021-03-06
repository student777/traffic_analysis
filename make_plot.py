import matplotlib.pyplot as plt
from get_data import traffic_by_hour
import numpy
from gmplot import GoogleMapPlotter
import csv
import os


class myPlotter(GoogleMapPlotter):
    size_min = 100
    size_max = 1000

    def scatter(self, data, colnum_info, color, **kwargs):
        kwargs["color"] = color
        settings = self._process_kwargs(kwargs)
        with open(data, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(reader)  # Skip first row
            size_list = []
            for row in reader:
                size = float(row[colnum_info['size']])
                size_list.append(size)
            x1, x2 = min(size_list), max(size_list)

            csvfile.seek(0)  # reset the file to the beginning
            next(reader)  # Skip first row
            for row in reader:
                lat = float(row[colnum_info['lat']])
                lng = float(row[colnum_info['lng']])
                size = float(row[colnum_info['size']])
                size_adjusted = self.cal_size(size, x1, x2)
                self.circle(lat, lng, size_adjusted, **settings)

    def cal_size(self, size, x1, x2):
        y1, y2 = self.size_min, self.size_max
        size_adjusted = (size - x1) * (y2 - y1) / (x2 - x1) + y1  # Linear transform (x1, x2) -> (y1, y2)
        return size_adjusted


def price_map(month, housing_type):
    gmap = myPlotter.from_geocode('Seoul')
    data = './out/dataframe/price_{}_{}.csv'.format(housing_type, month)
    colnum_info = {'lat': 0, 'lng': 1, 'size': 4}
    color = 'green'
    gmap.scatter(data, colnum_info, color)
    gmap.draw("out/plot/price_{}_{}.html".format(housing_type, month))
    print('price {} at {} successfully finished'.format(housing_type, month))


def traffic_map(month):
    data = './out/dataframe/traffic_{}.csv'.format(month)

    # draw ride traffic
    gmap = myPlotter.from_geocode('Seoul')
    colnum_info = {'lat': 2, 'lng': 3, 'size': 4}
    color = 'blue'
    gmap.scatter(data, colnum_info, color)
    gmap.draw("out/plot/traffic_ride_{}.html".format(month))
    print('ride traffic at {} successfully finished'.format(month))

    # draw alight traffic
    gmap2 = myPlotter.from_geocode('Seoul')
    color = 'red'
    colnum_info = {'lat': 2, 'lng': 3, 'size': 5}
    gmap2.scatter(data, colnum_info, color)
    gmap2.draw("out/plot/traffic_alight_{}.html".format(month))
    print('alight traffic at {} successfully finished'.format(month))


def traffic_grid_map(month):
    data = './out/dataframe/traffic_grid_{}.csv'.format(month)
    gmap = myPlotter.from_geocode('Seoul')
    colnum_info = {'lat': 0, 'lng': 1, 'size': 2}
    color = 'green'
    gmap.size_min = 10
    gmap.size_max = 3000
    gmap.scatter(data, colnum_info, color)
    gmap.draw("out/plot/traffic_grid_{}.html".format(month))
    print('Traffic grid at {} successfully finished'.format(month))


def hourly_traffic(month):
    plot_len = 3
    plot_size = plot_len * plot_len
    traffic_list = traffic_by_hour(month)  # about 380 counts(Seoul)
    fig_num = int(len(traffic_list) / plot_size)
    print('Number of plots to draw: {}'.format(fig_num))

    for i in range(0, fig_num):
        i_from = i * plot_size
        i_to = i_from + plot_size
        traffic_list_sliced = traffic_list[i_from:i_to]
        fig, ax = plt.subplots(plot_len, plot_len, figsize=(16, 12), dpi=80)
        j = 0

        for traffic in traffic_list_sliced:
            j = j + 1
            ax = plt.subplot(plot_len, plot_len, j)
            x_axis = numpy.arange(4.5, 28, 1)
            ax.set_title('%s역 %s' % (traffic['name'], traffic['line_num']))
            ax.plot(x_axis, traffic['ride'], 'c', label='ride')
            ax.plot(x_axis, traffic['alight'], 'm', label='alight')
            ax.set_xlabel('hour')
            ax.set_ylabel('passengers')

        plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
        fig.suptitle('지하철 역별 승차/하차 인원수')
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)

        # make dir
        output_dir = './out/plot/traffic_hourly_{}'.format(month)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        path_to_save = '{}/{}.png'.format(output_dir, "%.2d" % i)
        fig.savefig(path_to_save)
        print('saved %s' % path_to_save)
        plt.close()

    print('hourly traffic at {} finished successfully'.format(month))


if __name__ == '__main__':
    # hourly_traffic('201701')
    # price_map('201701', 'apartment_rent')
    # price_map('201701', 'apartment_trade')
    # price_map('201701', 'multi_trade')
    # price_map('201701', 'multi_rent')
    # price_map('201701', 'multi_trade')
    # price_map('201701', 'officetel_rent')
    # price_map('201701', 'officetel_trade')
    # price_map('201701', 'single_rent')
    # price_map('201701', 'single_trade')
    # traffic_map('201701')
    traffic_grid_map('201701')
