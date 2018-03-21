# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import calendar
import datetime

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    coeffs = []
    for each in degs:
        coeffs.append(pylab.polyfit(x, y, each))

    return coeffs

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    return (1 - (sum((y - estimated)**2))/(sum((y - pylab.mean(y))**2)))

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    for model in models:
        model_y = pylab.polyval(model, x)

        pylab.plot(x, y, 'bo', label = 'Observed Data')
        pylab.plot(x, model_y, 'r-', label = 'Model')
        pylab.xlabel('Time (Years)')
        pylab.ylabel('Temperature (Degrees Celsius)')

        degree = len(model) - 1
        rsquared = r_squared(y, model_y)
        if degree == 1:
            standart_error_over_slope = se_over_slope(x, y, model_y, model)
            titlestr = 'Climate Regression Model, Degree {0}\nR-squared: {1:3f}, SE/slope: {2:.3f}'.format(degree, rsquared, standart_error_over_slope)
        else:
            titlestr = 'Climate Regression Model, Degree {0}\nR-squared: {1:.3f}'.format(degree, rsquared)
        pylab.title(titlestr)
        pylab.show()


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # TODO
    cities_avg = list()
    for year in years:
        annual_temp_multi_cities = list()
        for city in multi_cities:
            annual_temp_multi_cities.append(get_city_avg(climate, city, year))
        cities_avg.append(sum(annual_temp_multi_cities)/len(multi_cities))
    return pylab.array(cities_avg)


def get_city_avg(climate, city, year):
    return sum(climate.get_yearly_temp(city, year))/float(get_days(year))

def get_days(year):
    if calendar.isleap(year):
        return 366
    else: return 365

    
    

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    moving_avg = list()
    for i in range(len(y)):
        moving_avg.append(get_moving_avg(i, y,window_length))
    return pylab.array(moving_avg)
        
def get_moving_avg(i, y, window_length):
    if i < window_length:
        return sum( y[0 : i+1])/(i + 1)
    else:
        return sum( y[(i+1 - window_length) : i+1])/window_length

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    return pylab.sqrt(sum((y-estimated)**2)/len(y))

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    multi_cities_std_dev = list()
    for year in years:
        daily_temp = list()
        for day in range(1, get_days(year) + 1):
            tmdate = datetime.datetime(year, 1, 1) + datetime.timedelta(day - 1)
            city_temp = list()
            
            for city in multi_cities:
                city_temp.append(climate.get_daily_temp(city, tmdate.month, tmdate.day, year))
            daily_temp.append(pylab.mean(city_temp))
        multi_cities_std_dev.append(pylab.std(daily_temp))
    return pylab.array(multi_cities_std_dev)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    for model in models:
        modeldata = pylab.polyval(model, x)

        pylab.plot(x, y, 'bo', label = 'Historical Data')
        pylab.plot(x, modeldata, 'r-', label = 'Model Prediction')
        pylab.xlabel('Year')
        pylab.ticklabel_format(useOffset = False)
        pylab.ylabel('Degree Cilsius')

        degree = len(model) -1
        model_rmse = rmse(y, modeldata)
        titlestr = 'Climate Model Prediction, Degree {0}\nRMSE:{1:.3f}'.format(degree, model_rmse)

        pylab.title(titlestr)
        pylab.show()

if __name__ == '__main__':
    pass
   # climatedata = Climate('data.csv')
   # years = pylab.array(TRAINING_INTERVAL)
   # testing_years = pylab.array(TESTING_INTERVAL)


   # # Part A.4
   # # TODO: replace this line with your code
   # 
   # #I
   # jan10th = list()
   # for year in TRAINING_INTERVAL:
   #     jan10th.append(climatedata.get_daily_temp('NEW YORK', 1, 10, year))
   # jan10th = pylab.array(jan10th)
   # modelA = generate_models(years, jan10th, [1])
   # evaluate_models_on_training(years, jan10th, modelA)

   # #II
   # yearavg = list()
   # for year in TRAINING_INTERVAL:
   #     yearavg.append(sum(climatedata.get_yearly_temp('NEW YORK', year))/get_days(year))

   # yearavg = pylab.array(yearavg)
   # modelA2 = generate_models(years, yearavg, [1])
   # evaluate_models_on_training(years, yearavg, modelA2)
   # 
   # # Part B
   # # TODO: replace this line with your code
   # national_average = gen_cities_avg(climatedata, CITIES, years)
   # modelB = generate_models(years, national_average, [1])
   # evaluate_models_on_training(years, national_average, modelB)

   # # Part C
   # # TODO: replace this line with your code
   # national_average = gen_cities_avg(climatedata, CITIES, years)
   # national_average_windowed_5year = moving_average(national_average, 5)
   # modelC = generate_models(years, national_average_windowed_5year, [1])
   # evaluate_models_on_training(years, national_average_windowed_5year, modelC)

   # # Part D.2
   # # TODO: replace this line with your code
   # national_average = gen_cities_avg(climatedata, CITIES, years)
   # national_average_windowed_5year = moving_average(national_average, 5)
   # modelD = generate_models(years, national_average_windowed_5year, [1, 2, 20])
   # evaluate_models_on_training(years, national_average_windowed_5year, modelD)

   # national_average_new = gen_cities_avg(climatedata, CITIES, testing_years)
   # national_average_new_windowed_5year = moving_average(national_average_new, 5)
   # evaluate_models_on_testing(testing_years, national_average_new_windowed_5year, modelD)



   # # Part E
   # # TODO: replace this line with your code
   # national_deviation = gen_std_devs(climatedata, CITIES, years)
   # national_deviation_windowed_5year = moving_average(national_deviation, 5)
   # modelE = generate_models(years, national_deviation, [1])
   # evaluate_models_on_training(years, national_deviation, modelE)
